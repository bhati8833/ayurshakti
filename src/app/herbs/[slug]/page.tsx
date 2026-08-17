import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getHerbDocs, getHerbBySlug } from '@/lib/markdown';
import { Leaf, Clock, ArrowLeft, ShieldCheck, HeartPulse } from 'lucide-react';

interface HerbPageProps {
  params: {
    slug: string;
  };
}

export async function generateStaticParams() {
  const herbs = getHerbDocs();
  return herbs.map((h) => ({
    slug: h.slug,
  }));
}

export async function generateMetadata({ params }: HerbPageProps): Promise<Metadata> {
  const herb = getHerbBySlug(params.slug);
  if (!herb) return { title: 'Herb Not Found | AyurShakti' };

  return {
    title: `${herb.title} | Ayurvedic Herbal Profile | AyurShakti`,
    description: herb.description,
    alternates: {
      canonical: `/herbs/${params.slug}`,
    },
  };
}

export default function HerbDetailPage({ params }: HerbPageProps) {
  const herb = getHerbBySlug(params.slug);
  if (!herb) notFound();

  const jsonLdHerb = {
    '@context': 'https://schema.org',
    '@type': 'MedicalWebPage',
    '@id': `https://ayurshakti.shop/herbs/${herb.slug}#webpage`,
    url: `https://ayurshakti.shop/herbs/${herb.slug}`,
    name: herb.title,
    headline: herb.title,
    description: herb.description,
    inLanguage: 'en-US',
    author: {
      '@type': 'Person',
      name: 'Suresh Bhati',
      url: 'https://ayurshakti.shop',
    },
    publisher: {
      '@type': 'Organization',
      name: 'AyurShakti',
      url: 'https://ayurshakti.shop',
      logo: 'https://ayurshakti.shop/public/images/logo.png',
    },
    about: {
      '@type': 'Substance',
      name: herb.title,
      description: herb.description,
    },
  };

  return (
    <main className="min-h-screen bg-ayur-bg pb-24">
      {/* Schema.org Herb Profile JSON-LD */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdHerb) }}
      />

      {/* Breadcrumb */}
      <nav aria-label="Breadcrumb" className="bg-ayur-forest/5 border-b border-ayur-border/40 py-3">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-xs font-semibold text-ayur-sage flex items-center gap-2">
          <Link href="/" className="hover:text-ayur-emerald transition-colors">Home</Link>
          <span>/</span>
          <Link href="/herbs" className="hover:text-ayur-emerald transition-colors">Herbal Library</Link>
          <span>/</span>
          <span className="text-ayur-forest capitalize">{herb.title}</span>
        </div>
      </nav>

      {/* Header Banner */}
      <header className="bg-gradient-to-b from-ayur-forest via-ayur-forest/95 to-ayur-bg text-white py-12 sm:py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <span className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-ayur-gold/20 text-ayur-gold border border-ayur-gold/30 text-xs font-bold uppercase tracking-wider mb-4">
            <Leaf className="w-3.5 h-3.5" /> {herb.category}
          </span>

          <h1 className="font-serif text-3xl sm:text-5xl font-bold tracking-tight text-white mb-6">
            {herb.title}
          </h1>

          <p className="text-sm sm:text-base text-ayur-sand/90 max-w-2xl mx-auto">
            {herb.description}
          </p>
        </div>
      </header>

      {/* Content Container */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 mt-10">
        <article className="glass-panel p-6 sm:p-12 rounded-3xl border border-ayur-gold/20 bg-white shadow-xs">
          <div
            className="prose prose-lg max-w-none text-ayur-forest leading-relaxed font-sans
              prose-headings:font-serif prose-headings:font-bold prose-headings:text-ayur-forest
              prose-h2:text-2xl prose-h2:border-b prose-h2:border-ayur-gold/20 prose-h2:pb-2 prose-h2:mt-8
              prose-a:text-ayur-emerald hover:prose-a:underline"
            dangerouslySetInnerHTML={{ __html: herb.htmlContent }}
          />

          {/* Citation & Scientific Evidence Transparency Block */}
          <div className="mt-12 pt-8 border-t border-ayur-gold/30 rounded-2xl bg-ayur-bg/60 p-6 sm:p-8 space-y-4">
            <div className="flex items-center justify-between flex-wrap gap-2">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-ayur-sand text-ayur-forest text-xs font-bold uppercase tracking-wider">
                📜 Primary Source & Evidence Citations
              </span>
              <span className="text-xs font-medium text-ayur-sage">Peer-Reviewed & Cataloged • Authored by Suresh Bhati</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs text-ayur-forest pt-2">
              <div className="p-4 rounded-xl bg-white border border-ayur-gold/20 space-y-1">
                <h4 className="font-serif font-bold text-sm text-ayur-forest">Classical Sanskrit Treatise</h4>
                <p className="text-ayur-sage">Primary verses from <em>Charaka Samhita (Sutrasthana)</em> and <em>Bhavaprakasha Nighantu</em>.</p>
              </div>
              <div className="p-4 rounded-xl bg-white border border-ayur-gold/20 space-y-1">
                <h4 className="font-serif font-bold text-sm text-ayur-forest">PubMed Clinical Studies</h4>
                <p className="text-ayur-sage">Phytochemical screening cross-referenced with NCBI PMIDs & pharmacology databases.</p>
              </div>
            </div>

            <div className="pt-2 text-[11px] text-ayur-sage leading-relaxed flex items-center justify-between flex-wrap gap-2 border-t border-ayur-border/40">
              <span>Medical Disclaimer: Educational material for wellness research. Consult a qualified Ayurvedic practitioner before starting any herbal protocol.</span>
              <Link href="/methodology" className="font-bold text-ayur-emerald hover:underline uppercase tracking-wider">View Full Vetting Methodology →</Link>
            </div>
          </div>
        </article>

        <div className="mt-8 text-center">
          <Link
            href="/herbs"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-ayur-forest text-white text-xs font-bold uppercase tracking-wider hover:bg-ayur-emerald transition-colors"
          >
            <ArrowLeft className="w-4 h-4" /> Back to Herbal Library
          </Link>
        </div>
      </div>
    </main>
  );
}
