import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getSamhitaBooks, getSamhitaBook, getSamhitaChapter } from '@/lib/markdown';
import { Scroll, Clock, ArrowLeft, ArrowRight, ShieldCheck, User } from 'lucide-react';

interface ChapterPageProps {
  params: {
    bookSlug: string;
    chapterSlug: string;
  };
}

export async function generateStaticParams() {
  const books = getSamhitaBooks();
  const paramsList: Array<{ bookSlug: string; chapterSlug: string }> = [];

  for (const book of books) {
    for (const ch of book.chapters) {
      if (ch.slug) {
        paramsList.push({
          bookSlug: book.book_slug,
          chapterSlug: ch.slug,
        });
      }
    }
  }

  return paramsList;
}

export async function generateMetadata({ params }: ChapterPageProps): Promise<Metadata> {
  const chapter = getSamhitaChapter(params.bookSlug, params.chapterSlug);
  if (!chapter) return { title: 'Chapter Not Found | AyurShakti' };

  return {
    title: `${chapter.title} | ${chapter.book} | AyurShakti`,
    description: `Read ${chapter.title} from ${chapter.book} (${chapter.section}). Unabridged English translation with classical Ayurvedic principles.`,
    alternates: {
      canonical: `/samhitas/${params.bookSlug}/${params.chapterSlug}`,
    },
  };
}

export default function ChapterViewPage({ params }: ChapterPageProps) {
  const chapter = getSamhitaChapter(params.bookSlug, params.chapterSlug);
  if (!chapter) notFound();

  const book = getSamhitaBook(params.bookSlug);
  const prevChapter = chapter.prev_chapter ? getSamhitaChapter(params.bookSlug, chapter.prev_chapter) : null;
  const nextChapter = chapter.next_chapter ? getSamhitaChapter(params.bookSlug, chapter.next_chapter) : null;

  // MedicalWebPage Schema
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'MedicalWebPage',
    name: chapter.title,
    isPartOf: {
      '@type': 'Book',
      name: chapter.book,
      author: {
        '@type': 'Person',
        name: chapter.author,
      },
    },
    author: {
      '@type': 'Person',
      name: 'Suresh Bhati',
      url: 'https://ayurshakti.shop',
    },
    publisher: {
      '@type': 'Organization',
      name: 'AyurShakti',
      logo: 'https://ayurshakti.shop/public/images/logo.png',
    },
    inLanguage: 'en',
    about: {
      '@type': 'MedicalCode',
      code: 'Ayurveda',
      codingSystem: 'Traditional Indian Medicine',
    },
  };

  return (
    <main className="min-h-screen bg-ayur-bg pb-24">
      {/* Schema Injection */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      {/* Breadcrumb Navigation */}
      <nav aria-label="Breadcrumb" className="bg-ayur-forest/5 border-b border-ayur-border/40 py-3">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-xs font-semibold text-ayur-sage flex items-center gap-2 overflow-x-auto whitespace-nowrap">
          <Link href="/" className="hover:text-ayur-emerald transition-colors">Home</Link>
          <span>/</span>
          <Link href="/samhitas" className="hover:text-ayur-emerald transition-colors">Samhitas</Link>
          <span>/</span>
          <Link href={`/samhitas/${params.bookSlug}`} className="hover:text-ayur-emerald transition-colors">{chapter.book}</Link>
          <span>/</span>
          <span className="text-ayur-forest truncate">{chapter.title}</span>
        </div>
      </nav>

      {/* Hero Header */}
      <header className="bg-gradient-to-b from-ayur-forest via-ayur-forest/95 to-ayur-bg text-white py-12 sm:py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <span className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-ayur-gold/20 text-ayur-gold border border-ayur-gold/30 text-xs font-bold uppercase tracking-wider mb-4">
            <Scroll className="w-3.5 h-3.5" /> {chapter.section} &bull; Chapter {chapter.chapter_number}
          </span>

          <h1 className="font-serif text-3xl sm:text-5xl font-bold tracking-tight text-white mb-6 leading-tight">
            {chapter.title}
          </h1>

          <div className="flex flex-wrap items-center justify-center gap-6 text-xs text-ayur-sand/90 font-medium">
            <span className="flex items-center gap-1.5">
              <User className="w-4 h-4 text-ayur-gold" /> By {chapter.author}
            </span>
            <span className="flex items-center gap-1.5">
              <Clock className="w-4 h-4 text-ayur-gold" /> {chapter.reading_time} min read
            </span>
            <span className="flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-ayur-gold" /> Unabridged Classical Text
            </span>
          </div>
        </div>
      </header>

      {/* Main Chapter Content Body */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-10">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-10">
          
          {/* Main Reading Column */}
          <article className="lg:col-span-3 glass-panel p-6 sm:p-12 rounded-3xl border border-ayur-gold/20 bg-white shadow-xs">
            <div
              className="prose prose-lg max-w-none text-ayur-forest leading-relaxed font-sans
                prose-headings:font-serif prose-headings:font-bold prose-headings:text-ayur-forest prose-headings:tracking-tight
                prose-h1:text-3xl prose-h2:text-2xl prose-h3:text-xl prose-h2:border-b prose-h2:border-ayur-gold/20 prose-h2:pb-2 prose-h2:mt-8
                prose-a:text-ayur-emerald prose-a:font-semibold hover:prose-a:underline
                prose-blockquote:border-l-4 prose-blockquote:border-ayur-gold prose-blockquote:bg-ayur-sand/30 prose-blockquote:py-2 prose-blockquote:px-4 prose-blockquote:rounded-r-xl
                prose-strong:text-ayur-forest prose-strong:font-bold"
              dangerouslySetInnerHTML={{ __html: chapter.htmlContent }}
            />

            {/* Next / Previous Pagination Footer */}
            <div className="mt-12 pt-8 border-t border-ayur-border/60 grid grid-cols-1 sm:grid-cols-2 gap-4">
              {prevChapter ? (
                <Link
                  href={`/samhitas/${params.bookSlug}/${prevChapter.chapter_slug}`}
                  className="p-4 rounded-2xl border border-ayur-border hover:border-ayur-emerald hover:bg-ayur-sand/30 transition-all flex items-center gap-3 group"
                >
                  <ArrowLeft className="w-5 h-5 text-ayur-gold group-hover:-translate-x-1 transition-transform" />
                  <div>
                    <div className="text-[10px] uppercase font-bold text-ayur-sage">Previous Chapter</div>
                    <div className="text-sm font-serif font-bold text-ayur-forest line-clamp-1">{prevChapter.title}</div>
                  </div>
                </Link>
              ) : <div />}

              {nextChapter ? (
                <Link
                  href={`/samhitas/${params.bookSlug}/${nextChapter.chapter_slug}`}
                  className="p-4 rounded-2xl border border-ayur-border hover:border-ayur-emerald hover:bg-ayur-sand/30 transition-all flex items-center justify-end gap-3 text-right group ml-auto w-full"
                >
                  <div>
                    <div className="text-[10px] uppercase font-bold text-ayur-sage">Next Chapter</div>
                    <div className="text-sm font-serif font-bold text-ayur-forest line-clamp-1">{nextChapter.title}</div>
                  </div>
                  <ArrowRight className="w-5 h-5 text-ayur-gold group-hover:translate-x-1 transition-transform" />
                </Link>
              ) : <div />}
            </div>
          </article>

          {/* Sticky Sidebar Navigation */}
          <aside className="space-y-6">
            <div className="sticky top-24 glass-panel p-6 rounded-3xl border border-ayur-gold/30 bg-white">
              <h3 className="font-serif font-bold text-lg text-ayur-forest mb-4 pb-2 border-b border-ayur-border/40">
                Book Table of Contents
              </h3>
              
              <p className="text-xs text-ayur-sage mb-4">
                Currently reading <strong>{chapter.section}</strong> of {chapter.book}.
              </p>

              <div className="space-y-3">
                <Link
                  href={`/samhitas/${params.bookSlug}`}
                  className="w-full py-2.5 px-4 rounded-xl bg-ayur-forest text-white text-xs font-bold uppercase tracking-wider hover:bg-ayur-emerald transition-colors flex items-center justify-center gap-2"
                >
                  <Scroll className="w-4 h-4" /> All {book?.total_chapters} Chapters
                </Link>

                <Link
                  href="/dosha-quiz"
                  className="w-full py-2.5 px-4 rounded-xl border border-ayur-gold text-ayur-forest text-xs font-bold uppercase tracking-wider hover:bg-ayur-sand transition-colors flex items-center justify-center gap-2"
                >
                  Take Dosha Assessment
                </Link>
              </div>
            </div>
          </aside>

        </div>
      </div>
    </main>
  );
}
