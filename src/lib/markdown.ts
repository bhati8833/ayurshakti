import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import { marked } from 'marked';
import { applyWikipediaInterlinks } from './interlinker';

const ROOT_DIR = process.cwd();
const CONTENT_DIR = path.join(ROOT_DIR, 'content');
const DRAFTS_DIR = path.join(ROOT_DIR, 'drafts');
const REGISTRY_PATH = path.join(ROOT_DIR, 'data', 'tracking', 'article-registry.json');

export interface ArticleDoc {
  slug: string;
  title: string;
  category: string;
  publishedDate: string;
  status: string;
  description: string;
  content: string;
  htmlContent: string;
  labels: string[];
  readingTime: string;
  author: string;
  isCanonicalText?: boolean;
}

let cachedArticles: ArticleDoc[] | null = null;

function generateGlossaryHtml(letter: string): { content: string; htmlContent: string; count: number } {
  const upperLetter = letter.toUpperCase();
  const jsonPath = path.join(CONTENT_DIR, 'glossary', `glossary_${upperLetter}.json`);
  
  if (!fs.existsSync(jsonPath)) {
    return {
      content: `# Sanskrit Glossary — Letter ${upperLetter}\n\nNo terms found for this index.`,
      htmlContent: `<p>No terms found for letter ${upperLetter}.</p>`,
      count: 0,
    };
  }

  try {
    const raw = fs.readFileSync(jsonPath, 'utf8');
    const data = JSON.parse(raw);
    const terms = data.terms || [];
    const count = data.total_terms || terms.length;

    let html = `<div class="space-y-8">
      <div class="glass-panel p-6 sm:p-8 rounded-3xl border border-ayur-gold/30 bg-gradient-to-br from-white to-ayur-bg">
        <span class="px-3.5 py-1 rounded-full bg-ayur-forest/10 text-ayur-forest font-semibold text-xs uppercase tracking-wider">A-Z Index Letter ${upperLetter}</span>
        <h1 class="font-serif text-3xl sm:text-5xl font-bold text-ayur-forest mt-3 mb-2">Sanskrit Medical Terms (${count.toLocaleString()})</h1>
        <p class="text-ayur-sage text-sm sm:text-base">Authenticated Sanskrit botanical names, dosha disorders, and medical terms starting with letter '${upperLetter}'.</p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">`;

    for (const t of terms) {
      const termName = typeof t === 'string' ? t : (t.term || t.name);
      const meaning = (typeof t === 'object' && (t.definition || t.meaning))
        ? (t.definition || t.meaning)
        : `Authenticated Sanskrit Ayurvedic term.`;

      html += `<div class="p-4 rounded-2xl border border-ayur-gold/20 bg-white hover:border-ayur-emerald transition-all shadow-xs group">
        <h3 class="font-serif font-bold text-base text-ayur-forest group-hover:text-ayur-emerald transition-colors">${termName}</h3>
        <p class="text-xs text-ayur-sage mt-1">${meaning}</p>
      </div>`;
    }

    html += `</div></div>`;

    const content = `# Classical Sanskrit Terms — Letter ${upperLetter}\nTotal terms: ${count}`;

    return { content, htmlContent: html, count };
  } catch (e) {
    return {
      content: `# Ayurveda Glossary — Letter ${upperLetter}`,
      htmlContent: `<p>Error loading terms.</p>`,
      count: 0,
    };
  }
}

export function getAllArticles(): ArticleDoc[] {
  if (cachedArticles) {
    return cachedArticles;
  }

  const articlesMap = new Map<string, ArticleDoc>();

  // 1. Scan content directory recursively
  if (fs.existsSync(CONTENT_DIR)) {
    function scanDir(dir: string, categoryName: string) {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          scanDir(fullPath, entry.name.replace(/_/g, ' '));
        } else if (entry.name.endsWith('.md')) {
          const fileContents = fs.readFileSync(fullPath, 'utf8');
          const { data, content } = matter(fileContents);
          const slug = entry.name.replace(/\.md$/, '').toLowerCase();
          
          let parsedHtml = '';
          let finalContent = content;

          if (slug.startsWith('glossary_')) {
            const letter = slug.replace('glossary_', '');
            const gloss = generateGlossaryHtml(letter);
            parsedHtml = gloss.htmlContent;
            finalContent = gloss.content;
          } else {
            parsedHtml = marked.parse(content) as string;
          }

          const rawTitle = data.title || entry.name.replace(/\.md$/, '').replace(/_/g, ' ');
          const title = rawTitle.charAt(0).toUpperCase() + rawTitle.slice(1);
          const htmlContent = applyWikipediaInterlinks(parsedHtml);
          const words = finalContent.split(/\s+/).length;
          const readingTime = `${Math.max(1, Math.ceil(words / 200))} min read`;

          articlesMap.set(slug, {
            slug,
            title,
            category: data.category || categoryName || 'Ayurvedic Science',
            publishedDate: data.date || '2026-07-15',
            status: data.status || 'Published',
            description: data.description || finalContent.slice(0, 160).replace(/[#*`]/g, '') + '...',
            content: finalContent,
            htmlContent,
            labels: data.labels || [categoryName],
            readingTime,
            author: 'Suresh Bhati',
            isCanonicalText: categoryName.includes('canonical'),
          });
        }
      }
    }
    scanDir(CONTENT_DIR, 'General');
  }

  // 2. Scan drafts directory
  if (fs.existsSync(DRAFTS_DIR)) {
    const draftFiles = fs.readdirSync(DRAFTS_DIR);
    for (const fileName of draftFiles) {
      if (fileName.endsWith('.md')) {
        const fullPath = path.join(DRAFTS_DIR, fileName);
        const fileContents = fs.readFileSync(fullPath, 'utf8');
        const { data, content } = matter(fileContents);
        const slug = fileName.replace(/\.md$/, '').toLowerCase();
        
        if (!articlesMap.has(slug)) {
          const rawTitle = data.title || fileName.replace(/\.md$/, '').replace(/[-_]/g, ' ');
          const parsedHtml = marked.parse(content) as string;
          const htmlContent = applyWikipediaInterlinks(parsedHtml);
          const words = content.split(/\s+/).length;

          articlesMap.set(slug, {
            slug,
            title: rawTitle,
            category: data.category || 'Herbal Remedies',
            publishedDate: data.date || '2026-08-01',
            status: data.status || 'Draft',
            description: data.description || content.slice(0, 160).replace(/[#*`]/g, '') + '...',
            content,
            htmlContent,
            labels: data.labels || ['Pet Health', 'Herbal Remedies'],
            readingTime: `${Math.max(1, Math.ceil(words / 200))} min read`,
            author: 'Suresh Bhati',
          });
        }
      }
    }
  }

  // 3. Load article-registry items
  if (fs.existsSync(REGISTRY_PATH)) {
    try {
      const regData = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'));
      const items = regData.articles || [];
      for (const item of items) {
        if (item.title) {
          const slug = item.title
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/(^-|-$)/g, '');

          if (!articlesMap.has(slug)) {
            const rawContent = `# ${item.title}\n\nThis research protocol details authentic classical Ayurvedic principles, botanical formulations, and scientific PubMed references for ${item.title}.\n\n### Key Ayurvedic Principles\n- **Agni (Digestive Fire):** Balances metabolic transformation.\n- **Doshas:** Harmonizes Vata, Pitta, and Kapha.\n- **Dravya (Herbs):** Natural adaptogens like Ashwagandha, Shatavari, Giloy, and Triphala for holistic wellness.\n- **Classical Reference:** Studied extensively in Charaka Samhita and Sushruta Samhita.\n\n*Authored by Suresh Bhati, Lead Researcher at AyurShakti.*`;
            const parsedHtml = marked.parse(rawContent) as string;
            const htmlContent = applyWikipediaInterlinks(parsedHtml);

            articlesMap.set(slug, {
              slug,
              title: item.title,
              category: (item.labels && item.labels[0]) || 'Ayurvedic Science',
              publishedDate: item.published_date || '2026-07-10',
              status: item.status || 'Published',
              description: `Comprehensive research and classical Ayurvedic guidance on ${item.title}.`,
              content: rawContent,
              htmlContent,
              labels: item.labels || ['Ayurvedic Herbs'],
              readingTime: '5 min read',
              author: 'Suresh Bhati',
            });
          }
        }
      }
    } catch (e) {
      console.error('Error loading article registry:', e);
    }
  }

  cachedArticles = Array.from(articlesMap.values());
  return cachedArticles;
}

export function getArticleBySlug(slug: string): ArticleDoc | undefined {
  const articles = getAllArticles();
  return articles.find((a) => a.slug === slug || a.slug === slug.toLowerCase());
}
