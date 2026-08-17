import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getSamhitaBooks, getSamhitaBook } from '@/lib/markdown';
import { Scroll, BookOpen, Clock, ChevronRight, ArrowLeft } from 'lucide-react';

interface BookPageProps {
  params: {
    bookSlug: string;
  };
}

export async function generateStaticParams() {
  const books = getSamhitaBooks();
  return books.map((book) => ({
    bookSlug: book.book_slug,
  }));
}

export async function generateMetadata({ params }: BookPageProps): Promise<Metadata> {
  const book = getSamhitaBook(params.bookSlug);
  if (!book) return { title: 'Book Not Found | AyurShakti' };

  return {
    title: `${book.title} - Complete Chapters & Table of Contents | AyurShakti`,
    description: `Browse all ${book.total_chapters} chapters of ${book.title}. Translated by ${book.author} with detailed Ayurvedic therapeutics.`,
    alternates: {
      canonical: `https://ayurshakti.shop/samhitas/${book.book_slug}`,
    },
  };
}

export default function BookTOCPage({ params }: BookPageProps) {
  const book = getSamhitaBook(params.bookSlug);
  if (!book) notFound();

  // Group chapters by section / sthana
  const sectionsMap = new Map<string, typeof book.chapters>();
  for (const ch of book.chapters) {
    const secName = ch.section || 'General';
    if (!sectionsMap.has(secName)) {
      sectionsMap.set(secName, []);
    }
    sectionsMap.get(secName)!.push(ch);
  }

  return (
    <main className="min-h-screen bg-ayur-bg pb-20">
      {/* Header Banner */}
      <section className="bg-gradient-to-b from-ayur-forest via-ayur-forest/95 to-ayur-bg text-white py-12 sm:py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <Link
            href="/samhitas"
            className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-ayur-gold hover:underline mb-6"
          >
            <ArrowLeft className="w-4 h-4" /> Back to All Samhitas
          </Link>

          <h1 className="font-serif text-3xl sm:text-5xl font-bold tracking-tight text-white mb-4">
            {book.title}
          </h1>

          <p className="text-sm font-semibold text-ayur-gold uppercase tracking-wider mb-4">
            Translated by {book.author} &bull; {book.total_chapters} Chapters
          </p>

          <p className="text-sm sm:text-base text-ayur-sand/90 max-w-3xl leading-relaxed">
            {book.description}
          </p>
        </div>
      </section>

      {/* Sections & Chapters List */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
        <div className="space-y-12">
          {Array.from(sectionsMap.entries()).map(([sectionName, chapters]) => (
            <div key={sectionName} className="glass-panel p-6 sm:p-8 rounded-3xl border border-ayur-gold/30 bg-white">
              <div className="flex items-center gap-3 mb-6 pb-4 border-b border-ayur-border/40">
                <Scroll className="w-6 h-6 text-ayur-gold" />
                <h2 className="font-serif text-2xl font-bold text-ayur-forest">
                  {sectionName}
                </h2>
                <span className="ml-auto text-xs font-semibold px-3 py-1 rounded-full bg-ayur-sand text-ayur-forest">
                  {chapters.length} Chapters
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {chapters.map((ch, idx) => (
                  <Link
                    key={ch.slug}
                    href={`/samhitas/${book.book_slug}/${ch.slug}`}
                    className="p-4 rounded-2xl border border-ayur-border/60 bg-ayur-bg/50 hover:bg-white hover:border-ayur-emerald hover:shadow-md transition-all duration-200 group flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-center justify-between text-xs text-ayur-gold font-bold mb-2">
                        <span>Chapter {ch.chapter_number || idx + 1}</span>
                        {ch.reading_time && (
                          <span className="flex items-center gap-1 text-ayur-sage font-normal">
                            <Clock className="w-3 h-3" /> {ch.reading_time} min
                          </span>
                        )}
                      </div>
                      <h3 className="font-serif text-sm sm:text-base font-bold text-ayur-forest group-hover:text-ayur-emerald transition-colors line-clamp-2">
                        {ch.title}
                      </h3>
                    </div>

                    <div className="mt-4 pt-2 border-t border-ayur-border/20 flex items-center justify-end text-xs font-bold text-ayur-emerald">
                      Read Chapter <ChevronRight className="w-3.5 h-3.5 ml-1" />
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
