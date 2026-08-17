import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getSiloDocs, getSiloDocBySlug } from '@/lib/markdown';
import { Microscope, ArrowLeft } from 'lucide-react';

interface ResearchPageProps {
  params: {
    slug: string;
  };
}

export async function generateStaticParams() {
  const docs = getSiloDocs('research');
  return docs.map((d) => ({
    slug: d.slug,
  }));
}

export async function generateMetadata({ params }: ResearchPageProps): Promise<Metadata> {
  const doc = getSiloDocBySlug('research', params.slug);
  if (!doc) return { title: 'Study Not Found | AyurShakti' };

  return {
    title: `${doc.title} | Ayurvedic Research Paper | AyurShakti`,
    description: doc.description,
    alternates: {
      canonical: `/research/${params.slug}`,
    },
  };
}

export default function ResearchDetailPage({ params }: ResearchPageProps) {
  const doc = getSiloDocBySlug('research', params.slug);
  if (!doc) notFound();

  return (
    <main className="min-h-screen bg-ayur-bg pb-24">
      <nav aria-label="Breadcrumb" className="bg-ayur-forest/5 border-b border-ayur-border/40 py-3">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-xs font-semibold text-ayur-sage flex items-center gap-2">
          <Link href="/" className="hover:text-ayur-emerald transition-colors">Home</Link>
          <span>/</span>
          <Link href="/research" className="hover:text-ayur-emerald transition-colors">Research</Link>
          <span>/</span>
          <span className="text-ayur-forest line-clamp-1">{doc.title}</span>
        </div>
      </nav>

      <header className="bg-gradient-to-b from-ayur-forest via-ayur-forest/95 to-ayur-bg text-white py-12 sm:py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <span className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-ayur-gold/20 text-ayur-gold border border-ayur-gold/30 text-xs font-bold uppercase tracking-wider mb-4">
            <Microscope className="w-3.5 h-3.5" /> {doc.category}
          </span>
          <h1 className="font-serif text-3xl sm:text-5xl font-bold tracking-tight text-white mb-6">
            {doc.title}
          </h1>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 mt-10">
        <article className="glass-panel p-6 sm:p-12 rounded-3xl border border-ayur-gold/20 bg-white shadow-xs">
          <div
            className="prose prose-lg max-w-none text-ayur-forest leading-relaxed font-sans
              prose-headings:font-serif prose-headings:font-bold prose-headings:text-ayur-forest
              prose-h2:text-2xl prose-h2:border-b prose-h2:border-ayur-gold/20 prose-h2:pb-2 prose-h2:mt-8
              prose-a:text-ayur-emerald hover:prose-a:underline"
            dangerouslySetInnerHTML={{ __html: doc.htmlContent }}
          />
        </article>

        <div className="mt-8 text-center">
          <Link
            href="/research"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-ayur-forest text-white text-xs font-bold uppercase tracking-wider hover:bg-ayur-emerald transition-colors"
          >
            <ArrowLeft className="w-4 h-4" /> Back to Research Hub
          </Link>
        </div>
      </div>
    </main>
  );
}
