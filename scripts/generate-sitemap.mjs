import fs from 'fs';
import path from 'path';

const ROOT_DIR = process.cwd();
const CONTENT_DIR = path.join(ROOT_DIR, 'content');
const PUBLIC_DIR = path.join(ROOT_DIR, 'public');
const BASE_URL = 'https://ayurshakti.shop';
const CURRENT_DATE = new Date().toISOString().split('T')[0];

const urls = [];

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
  { path: '', priority: '1.0', changefreq: 'daily' },
  { path: '/about', priority: '0.8', changefreq: 'monthly' },
  { path: '/dosha-quiz', priority: '0.9', changefreq: 'monthly' },
  { path: '/articles', priority: '0.9', changefreq: 'daily' },
  { path: '/herbs', priority: '0.9', changefreq: 'weekly' },
  { path: '/pet-health', priority: '0.9', changefreq: 'weekly' },
  { path: '/research', priority: '0.9', changefreq: 'weekly' },
  { path: '/samhitas', priority: '0.9', changefreq: 'weekly' },
  { path: '/canonical-texts', priority: '0.8', changefreq: 'monthly' },
  { path: '/glossary', priority: '0.8', changefreq: 'monthly' },
];

for (const page of staticPages) {
  addUrl(`${BASE_URL}${page.path}`, page.priority, page.changefreq);
}

// 2. Herbs Silo
const herbsDir = path.join(CONTENT_DIR, 'herbs');
if (fs.existsSync(herbsDir)) {
  const files = fs.readdirSync(herbsDir).filter(f => f.endsWith('.md'));
  for (const f of files) {
    const slug = f.replace(/\.md$/, '');
    addUrl(`${BASE_URL}/herbs/${slug}`, '0.8', 'weekly');
  }
}

// 3. Pet Health Silo
const petDir = path.join(CONTENT_DIR, 'pet-health');
if (fs.existsSync(petDir)) {
  const files = fs.readdirSync(petDir).filter(f => f.endsWith('.md'));
  for (const f of files) {
    const slug = f.replace(/\.md$/, '');
    addUrl(`${BASE_URL}/pet-health/${slug}`, '0.8', 'weekly');
  }
}

// 4. Research Silo
const researchDir = path.join(CONTENT_DIR, 'research');
if (fs.existsSync(researchDir)) {
  const files = fs.readdirSync(researchDir).filter(f => f.endsWith('.md'));
  for (const f of files) {
    const slug = f.replace(/\.md$/, '');
    addUrl(`${BASE_URL}/research/${slug}`, '0.8', 'weekly');
  }
}

// 5. Samhitas Books & Chapters
const samhitasDir = path.join(CONTENT_DIR, 'samhitas');
if (fs.existsSync(samhitasDir)) {
  const books = fs.readdirSync(samhitasDir, { withFileTypes: true });
  for (const bookDir of books) {
    if (bookDir.isDirectory()) {
      const bookSlug = bookDir.name;
      addUrl(`${BASE_URL}/samhitas/${bookSlug}`, '0.8', 'weekly');
      
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
      if (art.url) {
        // Extract slug from URL if present
        const urlMatch = art.url.match(/\/([^\/]+)\.html$/);
        const slug = urlMatch ? urlMatch[1] : art.slug;
        if (slug) {
          addUrl(`${BASE_URL}/articles/${slug}`, '0.8', 'weekly', art.published_date || CURRENT_DATE);
        }
      } else if (art.slug) {
        addUrl(`${BASE_URL}/articles/${art.slug}`, '0.8', 'weekly', art.published_date || CURRENT_DATE);
      }
    }
  } catch (e) {
    console.error('Error reading article registry for sitemap:', e);
  }
}

const sitemapXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.join('\n')}
</urlset>`;

if (!fs.existsSync(PUBLIC_DIR)) {
  fs.mkdirSync(PUBLIC_DIR, { recursive: true });
}

fs.writeFileSync(path.join(PUBLIC_DIR, 'sitemap.xml'), sitemapXml, 'utf8');
console.log(`[SITEMAP BUILD] Successfully generated sitemap.xml with ${urls.length} URLs in public/sitemap.xml`);
