#!/usr/bin/env python3
"""
Ayurveda WisdomLib Scraper
Scrapes Canonical texts, Essays & Studies, Other works, and A-Z Glossary from https://www.wisdomlib.org/ayurveda
Saves output structured inside content/ directory.
"""

import os
import re
import json
import time
import string
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("wisdomlib_scraper.log", encoding="utf-8")
    ]
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(BASE_DIR, "content")
CANONICAL_DIR = os.path.join(CONTENT_DIR, "canonical_texts")
ESSAYS_DIR = os.path.join(CONTENT_DIR, "essays_and_studies")
OTHER_DIR = os.path.join(CONTENT_DIR, "other_works")
GLOSSARY_DIR = os.path.join(CONTENT_DIR, "glossary")

for d in [CONTENT_DIR, CANONICAL_DIR, ESSAYS_DIR, OTHER_DIR, GLOSSARY_DIR]:
    os.makedirs(d, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

def get_session():
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=2.0,
        status_forcelist=[429, 500, 502, 503, 504, 522],
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update(HEADERS)
    return session

SESSION = get_session()

def fetch_url(url, timeout=30, retries=5):
    for attempt in range(retries):
        try:
            r = SESSION.get(url, timeout=timeout)
            if r.status_code == 200:
                return r.text
            elif r.status_code == 403:
                wait_time = 4.0 * (attempt + 1)
                logging.warning(f"Status 403 (Rate Limited) for URL: {url}. Backing off {wait_time}s... (Attempt {attempt+1}/{retries})")
                time.sleep(wait_time)
            else:
                logging.warning(f"Status {r.status_code} for URL: {url} (Attempt {attempt+1}/{retries})")
        except Exception as e:
            logging.warning(f"Error fetching {url}: {e} (Attempt {attempt+1}/{retries})")
            time.sleep(2.0 * (attempt + 1))
    return None

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')

def parse_wisdomlib_portal():
    url = "https://www.wisdomlib.org/ayurveda"
    html = fetch_url(url)
    if not html:
        logging.error("Failed to fetch portal main page")
        return {}

    soup = BeautifulSoup(html, 'html.parser')
    categorized_items = {
        "canonical_texts": [],
        "essays_and_studies": [],
        "other_works": []
    }

    group = soup.find('div', class_='list-group')
    if not group:
        logging.error("Could not find div.list-group on wisdomlib ayurveda page")
        return categorized_items

    current_cat = "canonical_texts"

    for elem in group.children:
        if getattr(elem, 'name', None) in ['h2', 'h3', 'h4']:
            h_text = elem.text.strip()
            if 'Canonical texts (with English translation)' in h_text or 'Canonical texts (in original language)' in h_text:
                current_cat = "canonical_texts"
            elif 'Essays, Studies' in h_text:
                current_cat = "essays_and_studies"
            elif 'Other works' in h_text:
                current_cat = "other_works"
        elif getattr(elem, 'name', None) == 'div' and 'list-group-item' in elem.get('class', []):
            a = elem.find('a', class_='title-l')
            if a:
                title = a.text.strip().replace('\n', ' ')
                href = urljoin("https://www.wisdomlib.org", a['href'])
                author = ""
                author_span = a.find('span', class_='author')
                if author_span:
                    author = author_span.text.strip()

                categorized_items[current_cat].append({
                    "title": title,
                    "author": author,
                    "url": href,
                    "slug": slugify(title[:60])
                })

    return categorized_items

def parse_publication(item, target_dir):
    slug = item["slug"]
    json_path = os.path.join(target_dir, f"{slug}.json")
    md_path = os.path.join(target_dir, f"{slug}.md")

    if os.path.exists(json_path) and os.path.exists(md_path):
        if os.path.getsize(json_path) > 200:
            logging.info(f"Skipping already scraped publication: {item['title']}")
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)

    logging.info(f"Scraping publication: {item['title']} ({item['url']})")
    html = fetch_url(item["url"])
    if not html:
        return None

    soup = BeautifulSoup(html, 'html.parser')
    
    meta_info = ""
    meta_div = soup.find('div', class_='author') or soup.find('small')
    if meta_div:
        meta_info = meta_div.text.strip()

    toc_links = []
    seen_links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/d/doc' in href and href not in seen_links:
            seen_links.add(href)
            toc_links.append({
                "title": a.text.strip(),
                "url": urljoin(item["url"], href)
            })

    publication_data = {
        "title": item["title"],
        "author": item["author"],
        "meta_info": meta_info,
        "source_url": item["url"],
        "total_chapters": len(toc_links),
        "chapters": []
    }

    if not toc_links:
        main_content = soup.find('div', id='content') or soup.find('article') or soup.find('div', class_='col-12')
        text_content = ""
        if main_content:
            for tag in main_content(['header', 'footer', 'nav', 'script', 'style', 'iframe', 'ins', 'form']):
                tag.decompose()
            text_content = main_content.get_text('\n\n', strip=True)

        publication_data["chapters"].append({
            "title": item["title"],
            "url": item["url"],
            "content": text_content
        })
    else:
        logging.info(f"Fetching {len(toc_links)} chapters for '{item['title']}'...")
        
        def fetch_chapter(ch):
            time.sleep(0.4)
            ch_html = fetch_url(ch["url"], timeout=25, retries=5)
            if not ch_html:
                return {"title": ch["title"], "url": ch["url"], "content": ""}
            
            ch_soup = BeautifulSoup(ch_html, 'html.parser')
            for tag in ch_soup(['header', 'footer', 'nav', 'script', 'style', 'iframe', 'ins', 'form']):
                tag.decompose()
            
            main_block = ch_soup.find('div', id='content') or ch_soup.find('article') or ch_soup.find('div', class_='col-12')
            if main_block:
                lines = []
                for p in main_block.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'blockquote', 'li']):
                    txt = p.get_text().strip()
                    if txt and not txt.startswith('Buy now') and 'wisdomlib' not in txt.lower():
                        lines.append(txt)
                content_text = '\n\n'.join(lines)
            else:
                content_text = ""
            
            return {
                "title": ch["title"],
                "url": ch["url"],
                "content": content_text
            }

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(fetch_chapter, ch) for ch in toc_links]
            for future in as_completed(futures):
                res = future.result()
                publication_data["chapters"].append(res)

    # Save JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(publication_data, f, indent=2, ensure_ascii=False)

    # Save Markdown
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f"# {publication_data['title']}\n\n")
        if publication_data['author']:
            f.write(f"**Author / Source:** {publication_data['author']}\n\n")
        f.write(f"**Source URL:** {publication_data['source_url']}\n\n")
        f.write(f"**Total Chapters/Sections:** {len(publication_data['chapters'])}\n\n")
        f.write("---\n\n")

        for idx, ch in enumerate(publication_data["chapters"], 1):
            f.write(f"## {idx}. {ch['title']}\n\n")
            f.write(f"*Source: {ch['url']}*\n\n")
            f.write(ch['content'] + "\n\n")
            f.write("---\n\n")

    logging.info(f"Successfully saved {slug}.json and {slug}.md")
    return publication_data

def scrape_glossary_letter(letter):
    letter_upper = letter.upper()
    json_path = os.path.join(GLOSSARY_DIR, f"glossary_{letter_upper}.json")
    md_path = os.path.join(GLOSSARY_DIR, f"glossary_{letter_upper}.md")

    if os.path.exists(json_path) and os.path.exists(md_path):
        if os.path.getsize(json_path) > 200:
            logging.info(f"Glossary letter {letter_upper} already exists. Skipping.")
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)

    url = f"https://www.wisdomlib.org/ayurveda/glossary/{letter}"
    logging.info(f"Scraping Glossary Letter: {letter_upper} from {url}")
    
    html = fetch_url(url, timeout=30, retries=5)
    if not html:
        logging.error(f"Failed to fetch glossary for letter {letter_upper}")
        return None

    soup = BeautifulSoup(html, 'html.parser')
    def_links = soup.select('a[href*="/definition/"]') or soup.select('div.col-12 a')
    
    terms = []
    seen = set()

    for a in def_links:
        href = a.get('href', '')
        term_name = a.text.strip()
        if not term_name or href in seen:
            continue
        seen.add(href)
        
        full_url = urljoin("https://www.wisdomlib.org", href)
        terms.append({
            "term": term_name,
            "url": full_url,
            "letter": letter_upper
        })

    glossary_data = {
        "letter": letter_upper,
        "total_terms": len(terms),
        "source_url": url,
        "terms": terms
    }

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(glossary_data, f, indent=2, ensure_ascii=False)

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f"# Ayurveda Glossary - Letter {letter_upper}\n\n")
        f.write(f"**Total Terms:** {len(terms)}\n")
        f.write(f"**Source URL:** {url}\n\n")
        f.write("---\n\n")

        for idx, t in enumerate(terms, 1):
            f.write(f"{idx}. **{t['term']}** - [View Definition]({t['url']})\n")

    logging.info(f"Saved Glossary {letter_upper} with {len(terms)} terms.")
    return glossary_data

def main():
    logging.info("Starting WisdomLib Ayurveda Full Scrape...")

    categorized = parse_wisdomlib_portal()
    logging.info(f"Parsed Portal Items: Canonical ({len(categorized['canonical_texts'])}), Essays ({len(categorized['essays_and_studies'])}), Other ({len(categorized['other_works'])})")

    manifest = {
        "canonical_texts": [],
        "essays_and_studies": [],
        "other_works": [],
        "glossary_summary": {}
    }

    logging.info("=== Phase 1: Canonical Texts ===")
    for item in categorized["canonical_texts"]:
        data = parse_publication(item, CANONICAL_DIR)
        if data:
            manifest["canonical_texts"].append({
                "title": data["title"],
                "author": data["author"],
                "total_chapters": data["total_chapters"],
                "file": f"canonical_texts/{item['slug']}.json"
            })

    logging.info("=== Phase 2: Essays & Academic Publications ===")
    for item in categorized["essays_and_studies"]:
        data = parse_publication(item, ESSAYS_DIR)
        if data:
            manifest["essays_and_studies"].append({
                "title": data["title"],
                "author": data["author"],
                "total_chapters": data["total_chapters"],
                "file": f"essays_and_studies/{item['slug']}.json"
            })

    logging.info("=== Phase 3: Other Works ===")
    for item in categorized["other_works"]:
        data = parse_publication(item, OTHER_DIR)
        if data:
            manifest["other_works"].append({
                "title": data["title"],
                "author": data["author"],
                "total_chapters": data["total_chapters"],
                "file": f"other_works/{item['slug']}.json"
            })

    logging.info("=== Phase 4: A-Z Glossary ===")
    total_glossary_terms = 0
    for letter in string.ascii_lowercase:
        g_data = scrape_glossary_letter(letter)
        if g_data:
            manifest["glossary_summary"][letter.upper()] = g_data["total_terms"]
            total_glossary_terms += g_data["total_terms"]

    manifest["total_glossary_terms"] = total_glossary_terms

    index_path = os.path.join(CONTENT_DIR, "index.json")
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    logging.info(f"FULL SCRAPE COMPLETE! All resources saved in {CONTENT_DIR}")

if __name__ == "__main__":
    main()
