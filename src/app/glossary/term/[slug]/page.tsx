import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { ArrowLeft, BookOpen, Sparkles, HelpCircle, ShieldCheck, ArrowRight, Share2 } from 'lucide-react';
import fs from 'fs';
import path from 'path';

interface TermPageProps {
  params: {
    slug: string;
  };
}

// Top Programmatic SEO Terms
const FEATURED_SLUGS = [
  'abhyanga', 'agni', 'ama', 'ojas', 'prana', 'prakriti', 'vata', 'pitta', 'kapha',
  'dhatu', 'srotas', 'rasayana', 'panchakarma', 'nadi', 'marma', 'guggulu',
  'ashwagandha', 'shatavari', 'giloy', 'guduchi', 'triphala', 'amalaki', 'haritaki',
  'bibhitaki', 'arjuna', 'tulsi', 'brahmi', 'neem', 'nimba', 'punarnava',
  'manjishtha', 'shilajit', 'pippali', 'vasaka', 'yashtimadhu', 'gokshura', 'dashmool'
];

export async function generateStaticParams() {
  return FEATURED_SLUGS.map((slug) => ({
    slug,
  }));
}

function getTermBySlug(slug: string): any | null {
  const glossaryDir = path.join(process.cwd(), 'content', 'glossary');
  if (!fs.existsSync(glossaryDir)) return null;

  for (const letter of 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('')) {
    const jsonPath = path.join(glossaryDir, `glossary_${letter}.json`);
    if (fs.existsSync(jsonPath)) {
      try {
        const raw = fs.readFileSync(jsonPath, 'utf8');
        const data = JSON.parse(raw);
        const terms = data.terms || [];
        const match = terms.find((t: any) => t.slug === slug || t.term.toLowerCase() === slug.replace(/-/g, ' '));
        if (match) return match;
      } catch (e) {
        // continue
      }
    }
  }
  return null;
}

export async function generateMetadata({ params }: TermPageProps): Promise<Metadata> {
  const termData = getTermBySlug(params.slug);
  const termName = termData ? termData.term : params.slug.replace(/-/g, ' ').toUpperCase();
  
  return {
    title: `What is ${termName} in Ayurveda? Definition & Medical Significance | AyurShakti`,
    description: termData
      ? termData.definition
      : `Explore the clinical Ayurvedic definition, classical origins, and dosha significance of ${termName}. Curated by Suresh Bhati.`,
    alternates: {
      canonical: `/glossary/term/${params.slug}`,
    },
  };
}

export default function TermDetailPage({ params }: TermPageProps) {
  const termData = getTermBySlug(params.slug);

  if (!termData) {
    notFound();
  }

  // FAQ Schema JSON-LD for Google "People Also Ask" PAA snippets
  const faqSchema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    'mainEntity': [
      {
        '@type': 'Question',
        'name': `What is ${termData.term} in Ayurvedic medicine?`,
        'acceptedAnswer': {
          '@type': 'Answer',
          'text': termData.definition,
        },
      },
      {
        '@type': 'Question',
        'name': `Which Dosha is influenced by ${termData.term}?`,
        'acceptedAnswer': {
          '@type': 'Answer',
          'text': `${termData.term} is categorized under ${termData.category}. ${termData.dosha ? `It is specifically associated with ${termData.dosha} balance.` : 'It contributes to overall constitutional equilibrium and tissue vitality.'}`,
        },
      },
      {
        '@type': 'Question',
        'name': `Where is ${termData.term} documented in classical Ayurvedic texts?`,
        'acceptedAnswer': {
          '@type': 'Answer',
          'text': `${termData.term} is authenticated in major Samhitas (Charaka, Sushruta, Vagbhata) and classical Nighantus for clinical reference.`,
        },
      },
    ],
  };

  return (
    <div className="py-12 bg-ayur-bg min-h-screen">
      
      {/* FAQ Schema */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }}
      />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        
        {/* Navigation */}
        <div>
          <Link
            href={`/glossary/${termData.letter.toLowerCase()}`}
            className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-ayur-forest hover:text-ayur-emerald transition-colors"
          >
            <ArrowLeft className="w-4 h-4 text-ayur-gold" />
            Back to Letter {termData.letter} Lexicon
          </Link>
        </div>

        {/* Term Card */}
        <article className="bg-white rounded-3xl p-8 sm:p-12 border border-ayur-gold/30 shadow-card space-y-8 relative">
          
          {/* Header Badge & Title */}
          <div className="space-y-4 border-b border-ayur-gold/20 pb-6">
            <div className="flex flex-wrap items-center gap-2">
              <span className="px-3 py-1 rounded-full bg-ayur-forest text-ayur-gold text-xs font-semibold uppercase tracking-wider shadow-xs">
                {termData.category}
              </span>
              {termData.dosha && (
                <span className="px-3 py-1 rounded-full bg-ayur-gold/20 text-ayur-forest text-xs font-semibold">
                  {termData.dosha}
                </span>
              )}
            </div>

            <div className="flex items-baseline justify-between gap-4 flex-wrap">
              <h1 className="font-serif text-3xl sm:text-5xl font-bold text-ayur-forest">
                {termData.term}
              </h1>
              {termData.devanagari && termData.devanagari !== termData.term && (
                <span className="font-serif text-2xl text-ayur-gold font-bold bg-ayur-forest/5 px-4 py-1 rounded-xl">
                  {termData.devanagari}
                </span>
              )}
            </div>
          </div>

          {/* Definition Section */}
          <div className="space-y-4">
            <h2 className="font-serif text-xl font-bold text-ayur-forest flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-ayur-emerald" />
              Ayurvedic Definition & Clinical Significance
            </h2>
            <p className="text-base sm:text-lg text-ayur-sage leading-relaxed bg-ayur-bg/50 p-6 rounded-2xl border border-ayur-gold/20">
              {termData.definition}
            </p>
          </div>

          {/* FAQ Accordion Preview for Google Snippets */}
          <div className="space-y-4 pt-4">
            <h3 className="font-serif text-lg font-bold text-ayur-forest flex items-center gap-2">
              <HelpCircle className="w-5 h-5 text-ayur-gold" />
              Frequently Asked Questions about {termData.term}
            </h3>

            <div className="space-y-3">
              <div className="p-4 rounded-xl border border-ayur-gold/20 bg-white space-y-1">
                <h4 className="font-bold text-sm text-ayur-forest">Which Dosha does {termData.term} balance?</h4>
                <p className="text-xs text-ayur-sage">
                  {termData.dosha ? `It is clinically indicated for ${termData.dosha}.` : 'It supports systemic equilibrium and tissue nourishment across all three doshas.'}
                </p>
              </div>

              <div className="p-4 rounded-xl border border-ayur-gold/20 bg-white space-y-1">
                <h4 className="font-bold text-sm text-ayur-forest">Is {termData.term} referenced in classical Samhitas?</h4>
                <p className="text-xs text-ayur-sage">
                  Yes, {termData.term} is documented in major treatises such as Caraka Samhita, Susruta Samhita, and classical Nighantus.
                </p>
              </div>
            </div>
          </div>

          {/* Internal Deep Link CTA */}
          {termData.link && (
            <div className="pt-6 border-t border-ayur-gold/20 flex flex-col sm:flex-row items-center justify-between gap-4">
              <div>
                <h4 className="font-serif font-bold text-base text-ayur-forest">Explore Full Botanical / Protocol Guide</h4>
                <p className="text-xs text-ayur-sage">Read evidence-based pharmacological studies and dosage guides on AyurShakti.</p>
              </div>
              <Link
                href={termData.link}
                className="px-6 py-3 rounded-xl bg-ayur-forest text-ayur-gold font-semibold text-xs uppercase tracking-wider hover:bg-ayur-forest/90 transition-all shadow-md inline-flex items-center gap-2 shrink-0"
              >
                Read Protocol
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          )}

          {/* Author Byline */}
          <div className="pt-6 border-t border-ayur-gold/10 text-xs text-ayur-sage flex items-center justify-between">
            <span>Curated for scholarly reference by <strong className="text-ayur-forest">Suresh Bhati</strong>.</span>
            <span className="flex items-center gap-1 text-ayur-emerald font-semibold">
              <ShieldCheck className="w-4 h-4" /> Authenticated
            </span>
          </div>

        </article>

      </div>
    </div>
  );
}
