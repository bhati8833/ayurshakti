import { MetadataRoute } from 'next';
import {
  getAllArticles,
  getHerbDocs,
  getSiloDocs,
  getSamhitaBooks,
  getSamhitaBook,
} from '@/lib/markdown';

const BASE_URL = 'https://ayurshakti.shop';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const sitemapEntries: MetadataRoute.Sitemap = [];
  const currentDate = new Date().toISOString().split('T')[0];

  // 1. Static Core Hub Pages
  const staticPages = [
    { url: `${BASE_URL}`, priority: 1.0, changeFrequency: 'daily' as const },
    { url: `${BASE_URL}/about`, priority: 0.8, changeFrequency: 'monthly' as const },
    { url: `${BASE_URL}/dosha-quiz`, priority: 0.9, changeFrequency: 'monthly' as const },
    { url: `${BASE_URL}/articles`, priority: 0.9, changeFrequency: 'daily' as const },
    { url: `${BASE_URL}/herbs`, priority: 0.9, changeFrequency: 'weekly' as const },
    { url: `${BASE_URL}/pet-health`, priority: 0.9, changeFrequency: 'weekly' as const },
    { url: `${BASE_URL}/research`, priority: 0.9, changeFrequency: 'weekly' as const },
    { url: `${BASE_URL}/samhitas`, priority: 0.9, changeFrequency: 'weekly' as const },
    { url: `${BASE_URL}/canonical-texts`, priority: 0.8, changeFrequency: 'monthly' as const },
    { url: `${BASE_URL}/glossary`, priority: 0.8, changeFrequency: 'monthly' as const },
  ];

  for (const page of staticPages) {
    sitemapEntries.push({
      url: page.url,
      lastModified: currentDate,
      changeFrequency: page.changeFrequency,
      priority: page.priority,
    });
  }

  // 2. Articles
  const articles = getAllArticles();
  for (const art of articles) {
    sitemapEntries.push({
      url: `${BASE_URL}/articles/${art.slug}`,
      lastModified: art.publishedDate || currentDate,
      changeFrequency: 'weekly',
      priority: 0.8,
    });
  }

  // 3. Herb Profiles
  const herbs = getHerbDocs();
  for (const herb of herbs) {
    sitemapEntries.push({
      url: `${BASE_URL}/herbs/${herb.slug}`,
      lastModified: currentDate,
      changeFrequency: 'weekly',
      priority: 0.8,
    });
  }

  // 4. Pet Health Silo
  const petHealthDocs = getSiloDocs('pet-health');
  for (const doc of petHealthDocs) {
    sitemapEntries.push({
      url: `${BASE_URL}/pet-health/${doc.slug}`,
      lastModified: currentDate,
      changeFrequency: 'weekly',
      priority: 0.8,
    });
  }

  // 5. Research Silo
  const researchDocs = getSiloDocs('research');
  for (const doc of researchDocs) {
    sitemapEntries.push({
      url: `${BASE_URL}/research/${doc.slug}`,
      lastModified: currentDate,
      changeFrequency: 'weekly',
      priority: 0.8,
    });
  }

  // 6. Samhitas Books & Chapters
  const books = getSamhitaBooks();
  for (const book of books) {
    sitemapEntries.push({
      url: `${BASE_URL}/samhitas/${book.book_slug}`,
      lastModified: currentDate,
      changeFrequency: 'weekly',
      priority: 0.8,
    });

    const fullBook = getSamhitaBook(book.book_slug);
    if (fullBook && fullBook.chapters) {
      for (const ch of fullBook.chapters) {
        sitemapEntries.push({
          url: `${BASE_URL}/samhitas/${book.book_slug}/${ch.slug}`,
          lastModified: currentDate,
          changeFrequency: 'monthly',
          priority: 0.7,
        });
      }
    }
  }

  // 7. Glossary Letters A-Z
  const letters = 'abcdefghijklmnopqrstuvwxyz'.split('');
  for (const letter of letters) {
    sitemapEntries.push({
      url: `${BASE_URL}/glossary/${letter}`,
      lastModified: currentDate,
      changeFrequency: 'monthly',
      priority: 0.6,
    });
  }

  return sitemapEntries;
}
