import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { getSamhitaBooks } from '@/lib/markdown';
import { Scroll, BookOpen, Sparkles, ChevronRight, ShieldCheck, Layers } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Classical Ayurvedic Samhitas | Authentic Sanskrit Texts | AyurShakti',
  description: 'Explore full English translations and Sanskrit verses of Charaka Samhita, Sushruta Samhita, and classical Ayurvedic scriptures with chapter-by-chapter navigation.',
  alternates: {
    canonical: 'https://ayurshakti.shop/samhitas',
  },
};

export default function SamhitasSiloPage() {
  const books = getSamhitaBooks();

  return (
    <main className="min-h-screen bg-ayur-bg pb-20">
      {/* Hero Header */}
      <section className="relative py-16 sm:py-24 bg-gradient-to-b from-ayur-forest via-ayur-forest/95 to-ayur-bg text-white overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="max-w-3xl">
            <span className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-ayur-gold/20 text-ayur-gold border border-ayur-gold/30 text-xs font-semibold uppercase tracking-wider mb-6">
              <Scroll className="w-4 h-4" /> Canonical Ayurvedic Texts
            </span>
            <h1 className="font-serif text-4xl sm:text-6xl font-bold tracking-tight text-white mb-6 leading-tight">
              Classical Sanskrit Samhitas
            </h1>
            <p className="text-lg sm:text-xl text-ayur-sand/90 font-sans leading-relaxed mb-8">
              Complete, chapter-by-chapter English translations of classical Ayurvedic treatises—including Charaka Samhita internal therapeutics and Sushruta Samhita surgical wisdom.
            </p>
            
            <div className="flex flex-wrap gap-4 text-xs font-semibold text-ayur-sand/80">
              <span className="flex items-center gap-1.5 bg-white/10 px-3 py-1.5 rounded-lg backdrop-blur-xs">
                <Layers className="w-4 h-4 text-ayur-gold" /> 360+ Chapter Pages
              </span>
              <span className="flex items-center gap-1.5 bg-white/10 px-3 py-1.5 rounded-lg backdrop-blur-xs">
                <ShieldCheck className="w-4 h-4 text-ayur-gold" /> 100% Unabridged Text
              </span>
              <span className="flex items-center gap-1.5 bg-white/10 px-3 py-1.5 rounded-lg backdrop-blur-xs">
                <Sparkles className="w-4 h-4 text-ayur-gold" /> Authenticated Bylines
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* Books Listing Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-10 relative z-20">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {books.map((book) => (
            <div
              key={book.book_slug}
              className="glass-panel p-8 rounded-3xl border border-ayur-gold/30 bg-white hover:shadow-xl transition-all duration-300 flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="px-3 py-1 rounded-full bg-ayur-forest/10 text-ayur-forest text-xs font-bold uppercase tracking-wider">
                    {book.total_chapters} Chapters
                  </span>
                  <BookOpen className="w-6 h-6 text-ayur-gold group-hover:scale-110 transition-transform" />
                </div>
                
                <h2 className="font-serif text-2xl sm:text-3xl font-bold text-ayur-forest mb-3 group-hover:text-ayur-emerald transition-colors">
                  {book.title}
                </h2>
                
                <p className="text-xs font-semibold text-ayur-gold uppercase tracking-wider mb-4">
                  Translated by {book.author}
                </p>

                <p className="text-sm text-ayur-sage leading-relaxed mb-6">
                  {book.description}
                </p>
              </div>

              <div className="pt-6 border-t border-ayur-border/40 flex items-center justify-between">
                <span className="text-xs font-medium text-ayur-sage">
                  Complete Sthanas & Therapeutics
                </span>
                <Link
                  href={`/samhitas/${book.book_slug}`}
                  className="px-5 py-2.5 rounded-full bg-ayur-forest text-white text-xs font-bold uppercase tracking-wider hover:bg-ayur-emerald transition-colors flex items-center gap-2"
                >
                  Browse Chapters <ChevronRight className="w-4 h-4" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
