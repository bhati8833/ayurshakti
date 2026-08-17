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

  return (
    <main className="min-h-screen bg-ayur-bg pb-24">
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
