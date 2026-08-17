import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import { marked } from 'marked';
import { applyWikipediaInterlinks } from './interlinker';

const ROOT_DIR = process.cwd();
const CONTENT_DIR = path.join(ROOT_DIR, 'content');
const DRAFTS_DIR = path.join(ROOT_DIR, 'drafts');
const REGISTRY_PATH = path.join(ROOT_DIR, 'data', 'tracking', 'article-registry.json');

export function sanitizeMarkdownContent(raw: string): string {
  if (!raw) return '';
  let text = raw;
  text = text.replace(/^\s*\*\*Author\s*\/\s*Source:\*\*\s*by\s*.*$/gmi, '');
  text = text.replace(/^\s*\*\*Total\s+Chapters\/Sections:\*\*\s*\d+$/gmi, '');
  text = text.replace(/Total\s+Chapters\/Sections:\s*\d+/gi, '');
  text = text.replace(/^\s*by\s+[A-Za-z\s.]+\|\s*\d{4}\s*\|\s*[\d,]+\s*words\s*$/gmi, '');
  text = text.replace(/.*?\|\s*\d{4}\s*\|\s*[\d,]+\s*words.*/gi, '');
  text = text.replace(/^\s*This page relates [‘'"\'].*?[’'"\'] found in the study on diseases and remedies found in the Atharvaveda and Charaka-samhita\..*?taken up for study\.\s*$/gmi, '');
  text = text.replace(/This page relates [‘'"\'].*?[’'"\'] found in the study on diseases and remedies found in the Atharvaveda and Charaka-samhita\..*?for study\./gi, '');
  text = text.replace(/^\s*Go\s+directly\s+to:\s*\n?\s*Footnotes\.*$/gmi, '');
  text = text.replace(/Go\s+directly\s+to:\s*.*?Footnotes\.*/gi, '');
  text = text.replace(/^\s*Footnotes\s+and\s+references:\s*\n?\s*\[back to top\]\s*$/gmi, '');
  text = text.replace(/^\s*\[back to top\]\s*$/gmi, '');
  text = text.replace(/^\s*\([A-Za-z\s.]+\)\s*\n?\s*Research\s+Scholar\s*$/gmi, '');
  text = text.replace(/^\s*Atharvaveda and Charaka Samhita\s*$/gm, '');
  text = text.replace(/\n{3,}/g, '\n\n');
  return text.trim();
}

export function addHeadingIdsToHtml(html: string): string {
  if (!html) return '';
  const headingCounts = new Map<string, number>();
  return html.replace(/<h([23])([^>]*)>(.*?)<\/h[23]>/gi, (match, level, attrs, content) => {
    if (attrs.includes('id=')) return match;
    const textContent = content.replace(/<[^>]+>/g, '').trim();
    let slug = textContent
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/[\s-]+/g, '-')
      .replace(/^-+|-+$/g, '');
    if (!slug) slug = `section-${level}`;
    
    const count = headingCounts.get(slug) || 0;
    headingCounts.set(slug, count + 1);
    const finalId = count > 0 ? `${slug}-${count}` : slug;
    
    return `<h${level}${attrs} id="${finalId}">${content}</h${level}>`;
  });
}


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

function generateGlossaryHtml(letter: string, mdContent?: string): { content: string; htmlContent: string; count: number } {
  const upperLetter = letter.toUpperCase();
  const jsonPath = path.join(CONTENT_DIR, 'glossary', `glossary_${upperLetter}.json`);
  
  let terms: any[] = [];
  let count = 0;

  if (fs.existsSync(jsonPath)) {
    try {
      const raw = fs.readFileSync(jsonPath, 'utf8');
      const data = JSON.parse(raw);
      terms = data.terms || [];
      count = data.total_terms || terms.length;
    } catch (e) {
      console.error(`Error reading ${jsonPath}:`, e);
    }
  }

  let overviewHtml = '';
  if (mdContent) {
    overviewHtml = marked.parse(mdContent) as string;
  }

  let termsHtml = `<div class="mt-8 space-y-6">
    <div class="glass-panel p-6 sm:p-8 rounded-3xl border border-ayur-gold/30 bg-gradient-to-br from-white to-ayur-bg">
      <span class="px-3.5 py-1 rounded-full bg-ayur-forest/10 text-ayur-forest font-semibold text-xs uppercase tracking-wider">A-Z Index Letter ${upperLetter}</span>
      <h2 class="font-serif text-2xl sm:text-4xl font-bold text-ayur-forest mt-3 mb-2">Authenticated Sanskrit Terms (${count.toLocaleString()})</h2>
      <p class="text-ayur-sage text-sm sm:text-base">Authenticated Sanskrit botanical names, dosha disorders, and medical terms starting with letter '${upperLetter}'.</p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">`;

  for (const t of terms) {
    const termName = typeof t === 'string' ? t : (t.term || t.name);
    const meaning = (typeof t === 'object' && (t.definition || t.meaning))
      ? (t.definition || t.meaning)
      : `Authenticated Sanskrit Ayurvedic term.`;

    termsHtml += `<div class="p-4 rounded-2xl border border-ayur-gold/20 bg-white hover:border-ayur-emerald transition-all shadow-xs group">
      <h3 class="font-serif font-bold text-base text-ayur-forest group-hover:text-ayur-emerald transition-colors">${termName}</h3>
      <p class="text-xs text-ayur-sage mt-1">${meaning}</p>
    </div>`;
  }

  termsHtml += `</div></div>`;

  const finalHtml = overviewHtml ? `${overviewHtml}\n${termsHtml}` : termsHtml;
  const content = mdContent || `# Classical Sanskrit Terms — Letter ${upperLetter}\nTotal terms: ${count}`;

  return { content, htmlContent: finalHtml, count };
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

  const cleanContent = sanitizeMarkdownContent(content);
  const parsedHtml = marked.parse(cleanContent) as string;
  const htmlContent = applyWikipediaInterlinks(addHeadingIdsToHtml(parsedHtml));

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
    const slug = f.replace(/\.md$/, '');
    const doc = getHerbDocBySlug(slug);
    if (doc) docs.push(doc);
  }

  return docs;
}

export function getHerbDocBySlug(slug: string): SiloDoc | null {
  const filePath = path.join(CONTENT_DIR, 'herbs', `${slug}.md`);
  if (!fs.existsSync(filePath)) return null;

  const raw = fs.readFileSync(filePath, 'utf8');
  const { data, content } = matter(raw);
  const cleanContent = sanitizeMarkdownContent(content);
  const parsedHtml = marked.parse(cleanContent) as string;

  return {
    title: data.title || slug.replace(/-/g, ' ').toUpperCase(),
    slug,
    silo: 'herbs',
    category: data.category || 'Herb Profile',
    content,
    htmlContent: applyWikipediaInterlinks(addHeadingIdsToHtml(parsedHtml)),
    description: data.description || content.slice(0, 160).replace(/[#*`]/g, '') + '...',
    readingTime: `${Math.max(1, Math.ceil(content.split(/\s+/).length / 200))} min read`,
  };
}

export const getHerbBySlug = getHerbDocBySlug;

// ----------------------------------------------------
// Research Silo Functions
// ----------------------------------------------------

export interface ResearchChapterMeta {
  title: string;
  paper_title: string;
  paper_slug: string;
  chapter_title: string;
  chapter_slug: string;
  chapter_number: number;
  author: string;
  original_scholar: string;
  silo: string;
  reading_time: number;
  prev_chapter: string;
  next_chapter: string;
  content: string;
  htmlContent: string;
}

export interface ResearchPaperInfo {
  title: string;
  paper_slug: string;
  author: string;
  original_scholar: string;
  total_chapters: number;
  silo: string;
  description: string;
  chapters: Array<{
    chapter_number: number;
    title: string;
    clean_title: string;
    slug: string;
    reading_time: number;
    word_count: number;
  }>;
}

export function getResearchPapers(): ResearchPaperInfo[] {
  const researchDir = path.join(CONTENT_DIR, 'research');
  if (!fs.existsSync(researchDir)) return [];

  const papers: ResearchPaperInfo[] = [];
  const entries = fs.readdirSync(researchDir, { withFileTypes: true });

  for (const entry of entries) {
    if (entry.isDirectory()) {
      const infoPath = path.join(researchDir, entry.name, 'paper-info.json');
      if (fs.existsSync(infoPath)) {
        try {
          const infoData = JSON.parse(fs.readFileSync(infoPath, 'utf8'));
          papers.push(infoData);
        } catch (e) {
          console.error(`Error reading ${infoPath}:`, e);
        }
      }
    }
  }

  return papers;
}

export function getResearchPaper(paperSlug: string): ResearchPaperInfo | null {
  const infoPath = path.join(CONTENT_DIR, 'research', paperSlug, 'paper-info.json');
  if (!fs.existsSync(infoPath)) return null;
  try {
    return JSON.parse(fs.readFileSync(infoPath, 'utf8'));
  } catch (e) {
    return null;
  }
}

export function getResearchChapter(paperSlug: string, chapterSlug: string): ResearchChapterMeta | null {
  const filePath = path.join(CONTENT_DIR, 'research', paperSlug, `${chapterSlug}.md`);
  if (!fs.existsSync(filePath)) return null;

  const raw = fs.readFileSync(filePath, 'utf8');
  const { data, content } = matter(raw);

  const cleanContent = sanitizeMarkdownContent(content);
  const parsedHtml = marked.parse(cleanContent) as string;
  const htmlContent = applyWikipediaInterlinks(addHeadingIdsToHtml(parsedHtml));

  return {
    title: data.title || chapterSlug.replace(/-/g, ' '),
    paper_title: data.paper_title || paperSlug.replace(/-/g, ' '),
    paper_slug: data.paper_slug || paperSlug,
    chapter_title: data.chapter_title || data.title || chapterSlug,
    chapter_slug: chapterSlug,
    chapter_number: data.chapter_number || 1,
    author: data.author || 'Suresh Bhati',
    original_scholar: data.original_scholar || 'Classical Ayurvedic Scholar',
    silo: 'research',
    reading_time: data.reading_time || 5,
    prev_chapter: data.prev_chapter || '',
    next_chapter: data.next_chapter || '',
    content,
    htmlContent,
  };
}

// ----------------------------------------------------
// Generic Silo Reader (pet-health, research fallback)
// ----------------------------------------------------

export function getSiloDocs(siloName: 'pet-health' | 'research'): SiloDoc[] {
  const dir = path.join(CONTENT_DIR, siloName);
  if (!fs.existsSync(dir)) return [];

  const docs: SiloDoc[] = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    if (entry.isFile() && entry.name.endsWith('.md')) {
      const slug = entry.name.replace(/\.md$/, '');
      const doc = getSiloDocBySlug(siloName, slug);
      if (doc) docs.push(doc);
    } else if (entry.isDirectory()) {
      const indexFile = path.join(dir, entry.name, 'index.md');
      if (fs.existsSync(indexFile)) {
        const doc = getSiloDocBySlug(siloName, `${entry.name}/index`);
        if (doc) {
          doc.slug = entry.name;
          docs.push(doc);
        }
      }
    }
  }

  return docs;
}

export function getSiloDocBySlug(siloName: 'pet-health' | 'research', slug: string): SiloDoc | null {
  let filePath = path.join(CONTENT_DIR, siloName, `${slug}.md`);
  if (!fs.existsSync(filePath)) {
    filePath = path.join(CONTENT_DIR, siloName, slug, 'index.md');
  }
  if (!fs.existsSync(filePath)) return null;

  const raw = fs.readFileSync(filePath, 'utf8');
  const { data, content } = matter(raw);
  const cleanContent = sanitizeMarkdownContent(content);
  const parsedHtml = marked.parse(cleanContent) as string;

  return {
    title: data.title || slug.replace(/-/g, ' ').toUpperCase(),
    slug,
    silo: siloName,
    category: data.category || 'Ayurvedic Studies',
    content,
    htmlContent: applyWikipediaInterlinks(addHeadingIdsToHtml(parsedHtml)),
    description: data.description || content.slice(0, 160).replace(/[#*`]/g, '') + '...',
    readingTime: `${Math.max(1, Math.ceil(content.split(/\s+/).length / 200))} min read`,
  };
}

let cachedArticleSummaries: ArticleDoc[] | null = null;

// Lightweight article loader for list pages, cards, and metadata (omits 19MB heavy HTML payload)
export function getAllArticleSummaries(): ArticleDoc[] {
  if (cachedArticleSummaries) return cachedArticleSummaries;
  const summariesMap = new Map<string, ArticleDoc>();

  if (fs.existsSync(CONTENT_DIR)) {
    const EXCLUDED_SILOS = new Set(['samhitas', 'herbs', 'herbs_draft', 'pet-health', 'research', 'glossary']);
    function scanDir(dir: string, categoryName: string) {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          if (!EXCLUDED_SILOS.has(entry.name)) {
            scanDir(fullPath, entry.name.replace(/_/g, ' '));
          }
        } else if (entry.name.endsWith('.md')) {
          const slug = entry.name.replace(/\.md$/, '').toLowerCase();
          if (slug.startsWith('glossary_')) continue;

          const fileContents = fs.readFileSync(fullPath, 'utf8');
          const { data, content } = matter(fileContents);
          
          const rawTitle = data.title || entry.name.replace(/\.md$/, '').replace(/_/g, ' ');
          const title = rawTitle.charAt(0).toUpperCase() + rawTitle.slice(1);
          const words = content.split(/\s+/).length;
          const readingTime = `${Math.max(1, Math.ceil(words / 200))} min read`;
          const description = data.description || content.slice(0, 160).replace(/[#*`]/g, '') + '...';

          summariesMap.set(slug, {
            slug,
            title,
            category: data.category || categoryName || 'Ayurvedic Science',
            publishedDate: data.date || '2026-07-15',
            status: data.status || 'Published',
            description,
            content: '', // Omit heavy content payload for index/card lists
            htmlContent: '', // Omit heavy htmlContent payload
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

  cachedArticleSummaries = Array.from(summariesMap.values());
  return cachedArticleSummaries;
}

export function getAllArticles(): ArticleDoc[] {
  return getAllArticleSummaries();
}

export function getArticleBySlug(slug: string): ArticleDoc | undefined {
  const lowerSlug = slug.toLowerCase();
  if (lowerSlug.startsWith('glossary_')) return undefined;
  
  // Find single article file on demand
  if (fs.existsSync(CONTENT_DIR)) {
    const EXCLUDED_SILOS = new Set(['samhitas', 'herbs', 'herbs_draft', 'pet-health', 'research', 'glossary']);
    function findFileInDir(dir: string, categoryName: string): ArticleDoc | null {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          if (!EXCLUDED_SILOS.has(entry.name)) {
            const found = findFileInDir(fullPath, entry.name.replace(/_/g, ' '));
            if (found) return found;
          }
        } else if (entry.name.endsWith('.md')) {
          const fileSlug = entry.name.replace(/\.md$/, '').toLowerCase();
          if (fileSlug === lowerSlug) {
            const fileContents = fs.readFileSync(fullPath, 'utf8');
            const { data, content } = matter(fileContents);
            
            let parsedHtml = '';
            let finalContent = sanitizeMarkdownContent(content);

            if (fileSlug.startsWith('glossary_')) {
              const letter = fileSlug.replace('glossary_', '');
              const gloss = generateGlossaryHtml(letter, content);
              parsedHtml = gloss.htmlContent;
              finalContent = gloss.content;
            } else {
              parsedHtml = marked.parse(finalContent) as string;
            }

            const rawTitle = data.title || entry.name.replace(/\.md$/, '').replace(/_/g, ' ');
            const title = rawTitle.charAt(0).toUpperCase() + rawTitle.slice(1);
            const htmlContent = applyWikipediaInterlinks(addHeadingIdsToHtml(parsedHtml));
            const words = finalContent.split(/\s+/).length;
            const readingTime = `${Math.max(1, Math.ceil(words / 200))} min read`;

            return {
              slug: fileSlug,
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
            };
          }
        }
      }
      return null;
    }
    const found = findFileInDir(CONTENT_DIR, 'General');
    if (found) return found;
  }

  return undefined;
}
