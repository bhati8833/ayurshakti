import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { BookOpen, ArrowRight } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Sanskrit & Ayurvedic Medical Directory (A-Z) | AyurShakti',
  description: 'Explore over 21,000 authenticated Sanskrit medical terms, botanical plant names, and classical Ayurvedic disease taxonomies.',
  alternates: {
    canonical: '/glossary',
  },
};

const ALPHABET = 'abcdefghijklmnopqrstuvwxyz'.split('');

export default function GlossaryPage() {
  const totalTermsCount = 21499;

  return (
    <div className="py-16 bg-ayur-bg min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        
        {/* Hero Section */}
        <div className="text-center max-w-3xl mx-auto space-y-4">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white text-ayur-forest border border-ayur-gold/40 text-xs font-semibold uppercase tracking-widest shadow-sm">
            <BookOpen className="w-4 h-4 text-ayur-emerald" />
            {totalTermsCount.toLocaleString()} Authenticated Sanskrit Terms
          </span>
          <h1 className="font-serif text-4xl sm:text-6xl font-bold text-ayur-forest">
            Sanskrit & Ayurvedic Medical Directory
          </h1>
          <p className="text-ayur-sage text-base sm:text-lg">
            Explore our comprehensive A–Z medical dictionary of classical Sanskrit botanical names, dosha disorders, and ancient therapeutic terms. Select any letter below to browse terms.
          </p>
        </div>

        {/* Quick A-Z Alphabet Strip */}
        <div className="flex flex-wrap justify-center gap-2 max-w-4xl mx-auto p-4 rounded-2xl bg-white border border-ayur-gold/30 shadow-xs">
          {ALPHABET.map((letter) => (
            <Link
              key={letter}
              href={`/glossary/${letter}`}
              className="w-9 h-9 rounded-lg font-serif font-bold text-sm flex items-center justify-center text-ayur-forest hover:bg-ayur-forest hover:text-ayur-gold transition-colors uppercase"
              title={`Browse letter ${letter.toUpperCase()}`}
            >
              {letter}
            </Link>
          ))}
        </div>

        {/* A-Z Alphabet Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {ALPHABET.map((letter) => {
            const letterUpper = letter.toUpperCase();
            return (
              <Link
                key={letter}
                href={`/glossary/${letter}`}
                className="glass-panel rounded-2xl p-6 border border-ayur-gold/20 hover:border-ayur-emerald/40 hover:shadow-card-hover transition-all group flex items-center justify-between"
              >
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-xl bg-ayur-forest text-ayur-gold flex items-center justify-center font-serif font-bold text-xl shadow-sm group-hover:scale-105 transition-transform">
                    {letterUpper}
                  </div>
                  <div>
                    <h3 className="font-serif font-bold text-lg text-ayur-forest group-hover:text-ayur-emerald transition-colors">
                      Glossary Directory {letterUpper}
                    </h3>
                    <p className="text-xs text-ayur-sage">Sanskrit terms starting with '{letterUpper}'</p>
                  </div>
                </div>
                <ArrowRight className="w-4 h-4 text-ayur-gold group-hover:translate-x-1 transition-transform" />
              </Link>
            );
          })}
        </div>

      </div>
    </div>
  );
}
