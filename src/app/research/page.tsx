import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { getSiloDocs } from '@/lib/markdown';
import { Microscope, ChevronRight, ShieldCheck, BookOpen } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Ayurvedic Research Papers & Alchemy Studies | AyurShakti',
  description: 'Academic studies on Rasa Jala Nidhi, ancient Indian surgery, Nyaya-Vaisesika philosophy, Marma Shastra, and ethnobotanical research.',
  alternates: {
    canonical: 'https://ayurshakti.shop/research',
  },
};

export default function ResearchSiloPage() {
  const docs = getSiloDocs('research');

  return (
    <main className="min-h-screen bg-ayur-bg pb-20">
      {/* Hero Header */}
      <section className="relative py-16 sm:py-24 bg-gradient-to-b from-ayur-forest via-ayur-forest/95 to-ayur-bg text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl">
            <span className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-ayur-gold/20 text-ayur-gold border border-ayur-gold/30 text-xs font-semibold uppercase tracking-wider mb-6">
              <Microscope className="w-4 h-4" /> Academic Research & Essays
            </span>
            <h1 className="font-serif text-4xl sm:text-6xl font-bold tracking-tight text-white mb-6 leading-tight">
              Ayurvedic Research & Alchemy
            </h1>
            <p className="text-lg sm:text-xl text-ayur-sand/90 font-sans leading-relaxed mb-8">
              Critical academic studies, historical investigations, and ancient alchemical texts (Rasa Shastra) connecting traditional wisdom with modern science.
            </p>
          </div>
        </div>
      </section>

      {/* Studies Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-10 relative z-20">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {docs.map((doc) => (
            <div
              key={doc.slug}
              className="glass-panel p-6 rounded-3xl border border-ayur-gold/30 bg-white hover:shadow-xl transition-all duration-300 flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="px-3 py-1 rounded-full bg-ayur-forest/10 text-ayur-forest text-xs font-bold uppercase tracking-wider">
                    {doc.category}
                  </span>
                  <Microscope className="w-5 h-5 text-ayur-gold group-hover:scale-110 transition-transform" />
                </div>

                <h2 className="font-serif text-xl font-bold text-ayur-forest mb-3 group-hover:text-ayur-emerald transition-colors line-clamp-2">
                  {doc.title}
                </h2>

                <p className="text-xs text-ayur-sage line-clamp-3 leading-relaxed mb-6">
                  {doc.description}
                </p>
              </div>

              <div className="pt-4 border-t border-ayur-border/40 flex items-center justify-between">
                <span className="text-xs font-semibold text-ayur-gold">
                  {doc.readingTime}
                </span>
                <Link
                  href={`/research/${doc.slug}`}
                  className="px-4 py-2 rounded-full bg-ayur-forest text-white text-xs font-bold uppercase tracking-wider hover:bg-ayur-emerald transition-colors flex items-center gap-1.5"
                >
                  Read Paper <ChevronRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
