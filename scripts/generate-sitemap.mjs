import fs from 'fs';
import path from 'path';

const ROOT_DIR = process.cwd();
const CONTENT_DIR = path.join(ROOT_DIR, 'content');
const PUBLIC_DIR = path.join(ROOT_DIR, 'public');
const BASE_URL = 'https://ayurshakti.shop';
const CURRENT_DATE = new Date().toISOString().split('T')[0];

const urls = [];
const llmsLinks = {
  core: [],
  herbs: [],
  petHealth: [],
  research: [],
  samhitas: [],
  articles: [],
};

function addUrl(loc, priority = '0.8', changefreq = 'weekly', lastmod = CURRENT_DATE) {
  urls.push(`  <url>
    <loc>${loc}</loc>
    <lastmod>${lastmod}</lastmod>
    <changefreq>${changefreq}</changefreq>
    <priority>${priority}</priority>
  </url>`);
}

// 1. Static Core Pages
const staticPages = [
  { path: '', priority: '1.0', changefreq: 'daily', name: 'Home Landing Page' },
  { path: '/about', priority: '0.8', changefreq: 'monthly', name: 'About AyurShakti & Suresh Bhati' },
  { path: '/dosha-quiz', priority: '0.9', changefreq: 'monthly', name: 'Interactive Dosha Assessment' },
  { path: '/articles', priority: '0.9', changefreq: 'daily', name: 'Articles & Evidence-Based Protocols' },
  { path: '/herbs', priority: '0.9', changefreq: 'weekly', name: 'Herbal Botanical Library' },
  { path: '/pet-health', priority: '0.9', changefreq: 'weekly', name: 'Veterinary Ayurveda & Pet Health' },
  { path: '/research', priority: '0.9', changefreq: 'weekly', name: 'PubMed Research Protocols' },
  { path: '/samhitas', priority: '0.9', changefreq: 'weekly', name: 'Classical Sanskrit Samhitas' },
  { path: '/canonical-texts', priority: '0.8', changefreq: 'monthly', name: 'Canonical Ayurvedic Manuscripts' },
  { path: '/glossary', priority: '0.8', changefreq: 'monthly', name: 'Sanskrit Ayurvedic Glossary' },
];

for (const page of staticPages) {
  const fullUrl = `${BASE_URL}${page.path}`;
  addUrl(fullUrl, page.priority, page.changefreq);
  llmsLinks.core.push(`- [${page.name}](${fullUrl})`);
}

// 2. Herbs Silo
const herbsDir = path.join(CONTENT_DIR, 'herbs');
if (fs.existsSync(herbsDir)) {
  const files = fs.readdirSync(herbsDir).filter(f => f.endsWith('.md'));
  for (const f of files) {
    const slug = f.replace(/\.md$/, '');
    const fullUrl = `${BASE_URL}/herbs/${slug}`;
    addUrl(fullUrl, '0.8', 'weekly');
    const readableTitle = slug.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    llmsLinks.herbs.push(`- [${readableTitle}](${fullUrl})`);
  }
}

// 3. Pet Health Silo
const petDir = path.join(CONTENT_DIR, 'pet-health');
if (fs.existsSync(petDir)) {
  const files = fs.readdirSync(petDir).filter(f => f.endsWith('.md'));
  for (const f of files) {
    const slug = f.replace(/\.md$/, '');
    const fullUrl = `${BASE_URL}/pet-health/${slug}`;
    addUrl(fullUrl, '0.8', 'weekly');
    const readableTitle = slug.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    llmsLinks.petHealth.push(`- [${readableTitle}](${fullUrl})`);
  }
}

// 4. Research Silo
const researchDir = path.join(CONTENT_DIR, 'research');
if (fs.existsSync(researchDir)) {
  const files = fs.readdirSync(researchDir).filter(f => f.endsWith('.md'));
  for (const f of files) {
    const slug = f.replace(/\.md$/, '');
    const fullUrl = `${BASE_URL}/research/${slug}`;
    addUrl(fullUrl, '0.8', 'weekly');
    const readableTitle = slug.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    llmsLinks.research.push(`- [${readableTitle}](${fullUrl})`);
  }
}

// 5. Samhitas Books & Chapters
const samhitasDir = path.join(CONTENT_DIR, 'samhitas');
if (fs.existsSync(samhitasDir)) {
  const books = fs.readdirSync(samhitasDir, { withFileTypes: true });
  for (const bookDir of books) {
    if (bookDir.isDirectory()) {
      const bookSlug = bookDir.name;
      const fullUrl = `${BASE_URL}/samhitas/${bookSlug}`;
      addUrl(fullUrl, '0.8', 'weekly');
      const readableTitle = bookSlug.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
      llmsLinks.samhitas.push(`- [${readableTitle}](${fullUrl})`);

      const bookPath = path.join(samhitasDir, bookSlug);
      const chapters = fs.readdirSync(bookPath).filter(f => f.endsWith('.md'));
      for (const ch of chapters) {
        const chSlug = ch.replace(/\.md$/, '');
        addUrl(`${BASE_URL}/samhitas/${bookSlug}/${chSlug}`, '0.7', 'monthly');
      }
    }
  }
}

// 6. Glossary Letters A-Z
const letters = 'abcdefghijklmnopqrstuvwxyz'.split('');
for (const letter of letters) {
  addUrl(`${BASE_URL}/glossary/${letter}`, '0.6', 'monthly');
}

// 7. Articles Registry
const registryPath = path.join(ROOT_DIR, 'data', 'tracking', 'article-registry.json');
if (fs.existsSync(registryPath)) {
  try {
    const rawData = JSON.parse(fs.readFileSync(registryPath, 'utf8'));
    const registry = Array.isArray(rawData) ? rawData : (rawData.articles || []);
    for (const art of registry) {
      let slug = art.slug;
      if (art.url) {
        const urlMatch = art.url.match(/\/([^\/]+)\.html$/);
        if (urlMatch) slug = urlMatch[1];
      }
      if (slug) {
        const fullUrl = `${BASE_URL}/articles/${slug}`;
        addUrl(fullUrl, '0.8', 'weekly', art.published_date || CURRENT_DATE);
        llmsLinks.articles.push(`- [${art.title || slug}](${fullUrl})`);
      }
    }
  } catch (e) {
    console.error('Error reading article registry for sitemap:', e);
  }
}

// Generate sitemap.xml
const sitemapXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.join('\n')}
</urlset>`;

// Generate llms.txt
const llmsTxt = `# AyurShakti — Authentic Ayurvedic Wisdom & Science-Backed Protocols

> AyurShakti is an evidence-based Ayurvedic medical knowledge base providing Sanskrit canonical text analysis, herbal profiles, veterinary remedies, and PubMed peer-reviewed protocols. Authored by Suresh Bhati.

## Core Hubs & Navigation
${llmsLinks.core.join('\n')}

## Botanical Herbal Profiles
${llmsLinks.herbs.join('\n')}

## Veterinary Ayurveda & Pet Health
${llmsLinks.petHealth.join('\n')}

## PubMed Research Protocols & Studies
${llmsLinks.research.join('\n')}

## Classical Sanskrit Samhitas
${llmsLinks.samhitas.join('\n')}

## Evidence-Based Articles & Guides
${llmsLinks.articles.slice(0, 30).join('\n')}

## System & Metadata Specifications
- XML Sitemap: ${BASE_URL}/sitemap.xml
- LLM Index: ${BASE_URL}/llms.txt
- Author: Suresh Bhati (Ayurvedic Practitioner & Researcher)
- Organization: AyurShakti (https://ayurshakti.shop)
`;

if (!fs.existsSync(PUBLIC_DIR)) {
  fs.mkdirSync(PUBLIC_DIR, { recursive: true });
}

fs.writeFileSync(path.join(PUBLIC_DIR, 'sitemap.xml'), sitemapXml, 'utf8');
fs.writeFileSync(path.join(PUBLIC_DIR, 'llms.txt'), llmsTxt, 'utf8');

console.log(`[SITEMAP & LLMS BUILD] Successfully generated public/sitemap.xml (${urls.length} URLs) and public/llms.txt`);
