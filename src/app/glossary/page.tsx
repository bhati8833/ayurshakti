import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { BookOpen, ArrowRight, Sparkles, ShieldCheck, Search } from 'lucide-react';
import GlossarySearch, { GlossaryTerm } from '@/components/GlossarySearch';
import fs from 'fs';
import path from 'path';

export const metadata: Metadata = {
  title: 'Sanskrit & Ayurvedic Medical Directory (A-Z) | AyurShakti',
  description: 'Explore over 21,499 authenticated Sanskrit medical terms, botanical plant names, dosha taxonomies, and therapeutic protocols with English definitions.',
  alternates: {
    canonical: '/glossary',
  },
};

const ALPHABET = 'abcdefghijklmnopqrstuvwxyz'.split('');

function getCuratedGlobalTerms(): GlossaryTerm[] {
  const glossaryDir = path.join(process.cwd(), 'content', 'glossary');
  const featuredTerms: GlossaryTerm[] = [];
  
  if (!fs.existsSync(glossaryDir)) return [];

  // Pick top terms across letters
  for (const letter of ['A', 'B', 'C', 'D', 'G', 'H', 'K', 'M', 'N', 'P', 'R', 'S', 'T', 'V']) {
    const jsonPath = path.join(glossaryDir, `glossary_${letter}.json`);
    if (fs.existsSync(jsonPath)) {
      try {
        const raw = fs.readFileSync(jsonPath, 'utf8');
        const data = JSON.parse(raw);
        const terms: GlossaryTerm[] = data.terms || [];
        // Take first 30 terms of each letter plus any term with link or specific category
        for (const t of terms) {
          if (t.link || t.dosha || featuredTerms.length < 500) {
            featuredTerms.push(t);
          }
        }
      } catch (e) {
        console.error(`Error reading ${jsonPath}:`, e);
      }
    }
  }

  return featuredTerms;
}

export default function GlossaryPage() {
  const totalTermsCount = 21499;
  const initialTerms = getCuratedGlobalTerms();

  // Schema.org Structured Data
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'DefinedTermSet',
    'name': 'AyurShakti Classical Sanskrit Medical Lexicon',
    'description': 'Comprehensive A–Z Ayurvedic medical dictionary of 21,499 authenticated Sanskrit botanical terms, dosha disorders, and clinical procedures.',
    'url': 'https://ayurshakti.shop/glossary',
    'author': {
      '@type': 'Person',
      'name': 'Suresh Bhati',
      'jobTitle': 'Ayurvedic Researcher & Health Writer',
      'url': 'https://ayurshakti.shop/about',
    },
    'publisher': {
      '@type': 'Organization',
      'name': 'AyurShakti',
      'url': 'https://ayurshakti.shop',
    },
  };

  return (
    <div className="py-12 bg-ayur-bg min-h-screen">
      
      {/* Schema.org Structured Data */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        
        {/* Hero Header */}
        <div className="text-center max-w-3xl mx-auto space-y-4">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white text-ayur-forest border border-ayur-gold/40 text-xs font-semibold uppercase tracking-widest shadow-sm">
            <BookOpen className="w-4 h-4 text-ayur-emerald" />
            {totalTermsCount.toLocaleString()} Authenticated Sanskrit Medical Terms
          </span>
          <h1 className="font-serif text-4xl sm:text-6xl font-bold text-ayur-forest">
            Sanskrit & Ayurvedic Medical Lexicon
          </h1>
          <p className="text-ayur-sage text-base sm:text-lg">
            Search our comprehensive A–Z dictionary of classical Sanskrit botanical names, dosha disorders, and clinical procedures curated by <span className="font-semibold text-ayur-forest">Suresh Bhati</span>.
          </p>
        </div>

        {/* Global Live Instant Search */}
        <GlossarySearch
          initialTerms={initialTerms}
          totalCount={totalTermsCount}
          showAlphabetBar={true}
        />

        {/* A-Z Alphabet Cards Grid */}
        <div className="space-y-6 pt-8">
          <div className="text-center space-y-2">
            <h2 className="font-serif text-2xl font-bold text-ayur-forest">Browse Lexicon by Letter (A–Z)</h2>
            <p className="text-xs text-ayur-sage uppercase tracking-wider font-semibold">Select any letter to explore all authenticated terms</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 max-w-6xl mx-auto">
            {ALPHABET.map((letter) => {
              const letterUpper = letter.toUpperCase();
              return (
                <Link
                  key={letter}
                  href={`/glossary/${letter}`}
                  className="glass-panel rounded-2xl p-5 border border-ayur-gold/20 hover:border-ayur-emerald/40 hover:shadow-card-hover transition-all group flex items-center justify-between bg-white"
                >
                  <div className="flex items-center gap-3.5">
                    <div className="w-10 h-10 rounded-xl bg-ayur-forest text-ayur-gold flex items-center justify-center font-serif font-bold text-lg shadow-sm group-hover:scale-105 transition-transform">
                      {letterUpper}
                    </div>
                    <div>
                      <h3 className="font-serif font-bold text-base text-ayur-forest group-hover:text-ayur-emerald transition-colors">
                        Letter {letterUpper}
                      </h3>
                      <p className="text-[11px] text-ayur-sage">Explore '{letterUpper}' Directory</p>
                    </div>
                  </div>
                  <ArrowRight className="w-4 h-4 text-ayur-gold group-hover:translate-x-1 transition-transform" />
                </Link>
              );
            })}
          </div>
        </div>

      </div>
    </div>
  );
}
