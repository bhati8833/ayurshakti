import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { ArrowLeft, BookOpen } from 'lucide-react';
import GlossarySearch, { GlossaryTerm } from '@/components/GlossarySearch';
import fs from 'fs';
import path from 'path';

const ALPHABET = 'abcdefghijklmnopqrstuvwxyz'.split('');

interface LetterPageProps {
  params: {
    letter: string;
  };
}

export async function generateStaticParams() {
  return ALPHABET.map((letter) => ({
    letter,
  }));
}

export async function generateMetadata({ params }: LetterPageProps): Promise<Metadata> {
  const letter = params.letter.toUpperCase();
  return {
    title: `Sanskrit Terms Starting with ${letter} | Ayurvedic Medical Glossary | AyurShakti`,
    description: `Browse classical Sanskrit medical terms, herbal botanical names, and Ayurvedic clinical definitions starting with the letter ${letter}. Curated by Suresh Bhati.`,
    alternates: {
      canonical: `/glossary/${params.letter.toLowerCase()}`,
    },
  };
}

function getTermsForLetter(letter: string): { terms: GlossaryTerm[]; totalTerms: number } {
  const upperLetter = letter.toUpperCase();
  const jsonPath = path.join(process.cwd(), 'content', 'glossary', `glossary_${upperLetter}.json`);

  if (!fs.existsSync(jsonPath)) {
    return { terms: [], totalTerms: 0 };
  }

  try {
    const raw = fs.readFileSync(jsonPath, 'utf8');
    const data = JSON.parse(raw);
    return {
      terms: data.terms || [],
      totalTerms: data.total_terms || (data.terms ? data.terms.length : 0),
    };
  } catch (e) {
    console.error(`Error reading ${jsonPath}:`, e);
    return { terms: [], totalTerms: 0 };
  }
}

export default function GlossaryLetterPage({ params }: LetterPageProps) {
  const letter = params.letter.toLowerCase();
  
  if (!ALPHABET.includes(letter)) {
    notFound();
  }

  const { terms, totalTerms } = getTermsForLetter(letter);
  const letterUpper = letter.toUpperCase();

  // Schema.org Structured Data
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'DefinedTermSet',
    'name': `Ayurvedic Medical Lexicon — Letter ${letterUpper}`,
    'description': `Collection of ${totalTerms} authenticated Sanskrit medical terms starting with letter ${letterUpper}.`,
    'url': `https://ayurshakti.shop/glossary/${letter}`,
    'author': {
      '@type': 'Person',
      'name': 'Suresh Bhati',
    },
  };

  return (
    <div className="py-12 bg-ayur-bg min-h-screen">
      
      {/* Schema.org JSON-LD */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        
        {/* Back Navigation & Breadcrumb */}
        <div className="flex items-center justify-between">
          <Link
            href="/glossary"
            className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-ayur-forest hover:text-ayur-emerald transition-colors"
          >
            <ArrowLeft className="w-4 h-4 text-ayur-gold" />
            Back to Glossary Main Directory
          </Link>
          <span className="text-xs text-ayur-sage font-medium">
            AyurShakti Medical Directory / Letter {letterUpper}
          </span>
        </div>

        {/* Header Title */}
        <div className="bg-white rounded-3xl p-8 sm:p-10 border border-ayur-gold/30 shadow-xs space-y-3">
          <div className="flex items-center gap-3">
            <span className="w-12 h-12 rounded-2xl bg-ayur-forest text-ayur-gold flex items-center justify-center font-serif font-bold text-2xl shadow-sm">
              {letterUpper}
            </span>
            <div>
              <h1 className="font-serif text-2xl sm:text-4xl font-bold text-ayur-forest">
                Sanskrit Terms Starting with '{letterUpper}'
              </h1>
              <p className="text-xs text-ayur-sage mt-1 font-medium">
                {totalTerms.toLocaleString()} authenticated terms compiled from classical Samhitas and Nighantus
              </p>
            </div>
          </div>
        </div>

        {/* Live Search & Paginated Grid Component */}
        <GlossarySearch
          initialTerms={terms}
          currentLetter={letter}
          totalCount={totalTerms}
          showAlphabetBar={true}
        />

      </div>
    </div>
  );
}
