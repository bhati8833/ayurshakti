import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH  = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def search_pubmed(query, retmax=5):
    params = urllib.parse.urlencode({
        "db": "pubmed", "term": query, "retmax": retmax, "retmode": "json"
    })
    req = urllib.request.Request(f"{ESEARCH}?{params}",
        headers={"User-Agent": "ayurshakti/1.0"})
    data = json.loads(urllib.request.urlopen(req).read())
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_details(pmids):
    if not pmids:
        return []
    params = urllib.parse.urlencode({
        "db": "pubmed", "id": ",".join(pmids),
        "retmode": "xml", "rettype": "abstract"
    })
    req = urllib.request.Request(f"{EFETCH}?{params}",
        headers={"User-Agent": "ayurshakti/1.0"})
    xml_data = urllib.request.urlopen(req).read()
    root = ET.fromstring(xml_data)
    results = []
    for article in root.findall(".//PubmedArticle"):
        medline = article.find(".//MedlineCitation")
        art = medline.find(".//Article")
        title = art.findtext("ArticleTitle", "")
        journal = art.find(".//Journal/Title")
        journal = journal.text if journal is not None else ""
        year = art.findtext(".//PubDate/Year", "")
        authors = []
        for author in art.findall(".//Author"):
            ln = author.findtext("LastName", "")
            fn = author.findtext("ForeName", "")
            if ln:
                authors.append(f"{ln} {fn}".strip())
        pmid = medline.findtext("PMID", "")
        doi = ""
        for eid in article.findall(".//ArticleId"):
            if eid.get("IdType") == "doi":
                doi = eid.text or ""
        results.append({
            "pmid": pmid, "title": title, "journal": journal,
            "year": year, "authors": authors, "doi": doi
        })
    return results

def format_markdown(results):
    lines = []
    for r in results:
        author_str = ", ".join(r["authors"][:3])
        if len(r["authors"]) > 3:
            author_str += " et al."
        cite = f"{author_str} ({r['year']}). {r['title']}. *{r['journal']}*."
        link = f"https://pubmed.ncbi.nlm.nih.gov/{r['pmid']}/"
        doi_link = f"https://doi.org/{r['doi']}" if r['doi'] else ""
        lines.append(f"- {cite} PMID: {r['pmid']}.")
        if r['doi']:
            lines.append(f"  DOI: {doi_link}")
    return "\n".join(lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/pubmed-cite.py '<search query>' [count]")
        print("Example: python3 scripts/pubmed-cite.py 'ashwagandha cortisol randomized trial' 3")
        sys.exit(1)
    query = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    pmids = search_pubmed(query, count)
    if not pmids:
        print(f"No results for: {query}")
        sys.exit(0)
    results = fetch_details(pmids)
    print(f"## PubMed Citations: {query}\n")
    print("Copy-paste these into your article:\n")
    print(format_markdown(results))