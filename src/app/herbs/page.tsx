import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { getHerbDocs } from '@/lib/markdown';
import { Leaf, Sparkles, ChevronRight, ShieldCheck, HeartPulse } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Botanical Herbal Library & Dravyaguna | AyurShakti',
  description: 'Explore authenticated Ayurvedic herb profiles including Ashwagandha, Shatavari, Giloy, Triphala, and Tulsi with detailed energetic profiles and scientific studies.',
  alternates: {
    canonical: 'https://ayurshakti.shop/herbs',
  },
};

export default function HerbSiloPage() {
  const herbs = getHerbDocs();

  return (
    <main className="min-h-screen bg-ayur-bg pb-20">
      {/* Hero Header */}
      <section className="relative py-16 sm:py-24 bg-gradient-to-b from-ayur-forest via-ayur-forest/95 to-ayur-bg text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl">
            <span className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-ayur-gold/20 text-ayur-gold border border-ayur-gold/30 text-xs font-semibold uppercase tracking-wider mb-6">
              <Leaf className="w-4 h-4" /> Dravyaguna Materia Medica
            </span>
            <h1 className="font-serif text-4xl sm:text-6xl font-bold tracking-tight text-white mb-6 leading-tight">
              Botanical Herbal Library
            </h1>
            <p className="text-lg sm:text-xl text-ayur-sand/90 font-sans leading-relaxed mb-8">
              Scientific adaptogenic profiles, Rasa (taste), Virya (potency), Vipaka (post-digestive effect), and clinical applications of authentic Ayurvedic botanicals.
            </p>
          </div>
        </div>
      </section>

      {/* Herbs Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-10 relative z-20">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {herbs.map((herb) => (
            <div
              key={herb.slug}
              className="glass-panel p-6 rounded-3xl border border-ayur-gold/30 bg-white hover:shadow-xl transition-all duration-300 flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="px-3 py-1 rounded-full bg-ayur-forest/10 text-ayur-forest text-xs font-bold uppercase tracking-wider">
                    {herb.category}
                  </span>
                  <Leaf className="w-5 h-5 text-ayur-gold group-hover:rotate-12 transition-transform" />
                </div>

                <h2 className="font-serif text-2xl font-bold text-ayur-forest mb-2 group-hover:text-ayur-emerald transition-colors">
                  {herb.title}
                </h2>

                <p className="text-xs text-ayur-sage line-clamp-3 leading-relaxed mb-6">
                  {herb.description}
                </p>
              </div>

              <div className="pt-4 border-t border-ayur-border/40 flex items-center justify-between">
                <span className="text-xs font-semibold text-ayur-gold">
                  {herb.readingTime}
                </span>
                <Link
                  href={`/herbs/${herb.slug}`}
                  className="px-4 py-2 rounded-full bg-ayur-forest text-white text-xs font-bold uppercase tracking-wider hover:bg-ayur-emerald transition-colors flex items-center gap-1.5"
                >
                  View Profile <ChevronRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
