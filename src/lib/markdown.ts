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

export interface SamhitaChapterMeta {
  title: string;
  book: string;
  book_slug: string;
  author: string;
  silo: string;
  section: string;
  chapter_number: number;
  chapter_slug: string;
  reading_time: number;
  prev_chapter: string;
  next_chapter: string;
  content: string;
  htmlContent: string;
}

export interface SamhitaBookInfo {
  title: string;
  book_slug: string;
  author: string;
  total_chapters: number;
  silo: string;
  description: string;
  chapters: Array<{
    chapter_number?: number;
    title: string;
    section?: string;
    slug: string;
    reading_time?: number;
  }>;
}

export interface SiloDoc {
  title: string;
  slug: string;
  silo: 'herbs' | 'pet-health' | 'research' | 'samhitas';
  category: string;
  content: string;
  htmlContent: string;
  description: string;
  readingTime: string;
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

// ----------------------------------------------------
// Samhitas (Classical Texts Silo) Functions
// ----------------------------------------------------

export function getSamhitaBooks(): SamhitaBookInfo[] {
  const samhitasDir = path.join(CONTENT_DIR, 'samhitas');
  if (!fs.existsSync(samhitasDir)) return [];

  const books: SamhitaBookInfo[] = [];
  const entries = fs.readdirSync(samhitasDir, { withFileTypes: true });

  for (const entry of entries) {
    if (entry.isDirectory()) {
      const infoPath = path.join(samhitasDir, entry.name, 'book-info.json');
      if (fs.existsSync(infoPath)) {
        try {
          const infoData = JSON.parse(fs.readFileSync(infoPath, 'utf8'));
          books.push(infoData);
        } catch (e) {
          console.error(`Error reading ${infoPath}:`, e);
        }
      }
    }
  }

  return books;
}

export function getSamhitaBook(bookSlug: string): SamhitaBookInfo | null {
  const infoPath = path.join(CONTENT_DIR, 'samhitas', bookSlug, 'book-info.json');
  if (!fs.existsSync(infoPath)) return null;
  try {
    return JSON.parse(fs.readFileSync(infoPath, 'utf8'));
  } catch (e) {
    return null;
  }
}

export function getSamhitaChapter(bookSlug: string, chapterSlug: string): SamhitaChapterMeta | null {
  const filePath = path.join(CONTENT_DIR, 'samhitas', bookSlug, `${chapterSlug}.md`);
  if (!fs.existsSync(filePath)) return null;

  const raw = fs.readFileSync(filePath, 'utf8');
  const { data, content } = matter(raw);

  const parsedHtml = marked.parse(content) as string;
  const htmlContent = applyWikipediaInterlinks(parsedHtml);

  return {
    title: data.title || chapterSlug.replace(/-/g, ' '),
    book: data.book || 'Classical Text',
    book_slug: data.book_slug || bookSlug,
    author: data.author || 'Suresh Bhati',
    silo: 'samhitas',
    section: data.section || 'General',
    chapter_number: data.chapter_number || 1,
    chapter_slug: chapterSlug,
    reading_time: data.reading_time || 5,
    prev_chapter: data.prev_chapter || '',
    next_chapter: data.next_chapter || '',
    content,
    htmlContent,
  };
}

// ----------------------------------------------------
// Herbs Silo Functions
// ----------------------------------------------------

export function getHerbDocs(): SiloDoc[] {
  const dir = path.join(CONTENT_DIR, 'herbs');
  if (!fs.existsSync(dir)) return [];

  const docs: SiloDoc[] = [];
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.md'));

  for (const f of files) {
    const raw = fs.readFileSync(path.join(dir, f), 'utf8');
    const { data, content } = matter(raw);
    const slug = f.replace(/\.md$/, '');
    const parsedHtml = marked.parse(content) as string;

    docs.push({
      title: data.title || slug.replace(/-/g, ' ').toUpperCase(),
      slug,
      silo: 'herbs',
      category: data.category || 'Ayurvedic Dravyaguna',
      content,
      htmlContent: applyWikipediaInterlinks(parsedHtml),
      description: data.description || content.slice(0, 160).replace(/[#*`]/g, '') + '...',
      readingTime: `${Math.max(1, Math.ceil(content.split(/\s+/).length / 200))} min read`,
    });
  }

  return docs;
}

export function getHerbBySlug(slug: string): SiloDoc | null {
  const filePath = path.join(CONTENT_DIR, 'herbs', `${slug}.md`);
  if (!fs.existsSync(filePath)) return null;

  const raw = fs.readFileSync(filePath, 'utf8');
  const { data, content } = matter(raw);
  const parsedHtml = marked.parse(content) as string;

  return {
    title: data.title || slug.replace(/-/g, ' ').toUpperCase(),
    slug,
    silo: 'herbs',
    category: data.category || 'Ayurvedic Dravyaguna',
    content,
    htmlContent: applyWikipediaInterlinks(parsedHtml),
    description: data.description || content.slice(0, 160).replace(/[#*`]/g, '') + '...',
    readingTime: `${Math.max(1, Math.ceil(content.split(/\s+/).length / 200))} min read`,
  };
}

// ----------------------------------------------------
// Pet Health & Research Silo Functions
// ----------------------------------------------------

export function getSiloDocs(siloName: 'pet-health' | 'research'): SiloDoc[] {
  const dir = path.join(CONTENT_DIR, siloName);
  if (!fs.existsSync(dir)) return [];

  const docs: SiloDoc[] = [];
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.md'));

  for (const f of files) {
    const raw = fs.readFileSync(path.join(dir, f), 'utf8');
    const { data, content } = matter(raw);
    const slug = f.replace(/\.md$/, '');
    const parsedHtml = marked.parse(content) as string;

    docs.push({
      title: data.title || slug.replace(/-/g, ' ').toUpperCase(),
      slug,
      silo: siloName,
      category: data.category || 'Ayurvedic Studies',
      content,
      htmlContent: applyWikipediaInterlinks(parsedHtml),
      description: data.description || content.slice(0, 160).replace(/[#*`]/g, '') + '...',
      readingTime: `${Math.max(1, Math.ceil(content.split(/\s+/).length / 200))} min read`,
    });
  }

  return docs;
}

export function getSiloDocBySlug(siloName: 'pet-health' | 'research', slug: string): SiloDoc | null {
  const filePath = path.join(CONTENT_DIR, siloName, `${slug}.md`);
  if (!fs.existsSync(filePath)) return null;

  const raw = fs.readFileSync(filePath, 'utf8');
  const { data, content } = matter(raw);
  const parsedHtml = marked.parse(content) as string;

  return {
    title: data.title || slug.replace(/-/g, ' ').toUpperCase(),
    slug,
    silo: siloName,
    category: data.category || 'Ayurvedic Studies',
    content,
    htmlContent: applyWikipediaInterlinks(parsedHtml),
    description: data.description || content.slice(0, 160).replace(/[#*`]/g, '') + '...',
    readingTime: `${Math.max(1, Math.ceil(content.split(/\s+/).length / 200))} min read`,
  };
}

// Legacy Article loader fallback
export function getAllArticles(): ArticleDoc[] {
  if (cachedArticles) return cachedArticles;
  const articlesMap = new Map<string, ArticleDoc>();

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

  cachedArticles = Array.from(articlesMap.values());
  return cachedArticles;
}

export function getArticleBySlug(slug: string): ArticleDoc | undefined {
  const articles = getAllArticles();
  return articles.find((a) => a.slug === slug || a.slug === slug.toLowerCase());
}
