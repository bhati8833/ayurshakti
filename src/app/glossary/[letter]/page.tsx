import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getArticleBySlug } from '@/lib/markdown';
import { ArrowLeft, BookOpen, Search, Tag, ShieldCheck } from 'lucide-react';

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
    title: `Sanskrit Terms Starting with ${letter} | Ayurvedic Glossary | AyurShakti`,
    description: `Browse classical Sanskrit medical terms, herbal botanical names, and Ayurvedic clinical definitions starting with the letter ${letter}.`,
    alternates: {
      canonical: `/glossary/${params.letter.toLowerCase()}`,
    },
  };
}

export default function GlossaryLetterPage({ params }: LetterPageProps) {
  const letter = params.letter.toLowerCase();
  
  if (!ALPHABET.includes(letter)) {
    notFound();
  }

  const slug = `glossary_${letter}`;
  const article = getArticleBySlug(slug);

  if (!article) {
    notFound();
  }

  return (
    <article className="py-12 bg-ayur-bg min-h-screen">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        
        {/* Back Button Navigation */}
        <div>
          <Link
            href="/glossary"
            className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-ayur-forest hover:text-ayur-emerald transition-colors"
          >
            <ArrowLeft className="w-4 h-4 text-ayur-gold" />
            Back to Glossary Directory
          </Link>
        </div>

        {/* A-Z Alphabet Bar */}
        <div className="flex flex-wrap justify-center gap-2 p-4 rounded-2xl bg-white border border-ayur-gold/30 shadow-xs">
          {ALPHABET.map((l) => {
            const isActive = l === letter;
            return (
              <Link
                key={l}
                href={`/glossary/${l}`}
                className={`w-9 h-9 rounded-lg font-serif font-bold text-sm flex items-center justify-center transition-colors ${
                  isActive
                    ? 'bg-ayur-forest text-ayur-gold shadow-sm'
                    : 'text-ayur-forest hover:bg-ayur-forest/10'
                }`}
                title={`Browse letter ${l.toUpperCase()}`}
              >
                {l.toUpperCase()}
              </Link>
            );
          })}
        </div>

        {/* Glossary Terms Content */}
        <div
          className="prose-ayur bg-white rounded-3xl p-8 sm:p-12 border border-ayur-border shadow-sm mx-auto"
          dangerouslySetInnerHTML={{ __html: article.htmlContent }}
        />

      </div>
    </article>
  );
}
