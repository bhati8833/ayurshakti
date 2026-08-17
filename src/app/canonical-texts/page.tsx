import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { getAllArticles } from '@/lib/markdown';
import { Compass, ScrollText, ArrowRight } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Sanskrit Canonical Text Library | Classical Archives | AyurShakti',
  description: 'Direct analytical translations of classical Sanskrit literature including Vrikshayurveda, Mrigayurveda, and Samhitas.',
  alternates: {
    canonical: '/canonical-texts',
  },
};

export default function CanonicalTextsPage() {
  const allArticles = getAllArticles();
  const canonicals = allArticles.filter((a) => a.isCanonicalText || a.category.toLowerCase().includes('canonical'));

  return (
    <div className="py-16 bg-ayur-bg min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-16">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white text-ayur-forest border border-ayur-gold/40 text-xs font-semibold uppercase tracking-widest shadow-sm">
            <ScrollText className="w-4 h-4 text-ayur-gold" />
            Classical Sanskrit Archives
          </span>
          <h1 className="font-serif text-4xl sm:text-6xl font-bold text-ayur-forest">
            Sanskrit Canonical Text Library
          </h1>
          <p className="text-ayur-sage text-lg">
            Direct analytical translations of classical Sanskrit literature: Vrikshayurveda (plant medicine), Mrigayurveda (veterinary protocols), and Samhitas.
          </p>
        </div>

        {/* Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {canonicals.map((item) => (
            <div
              key={item.slug}
              className="glass-panel rounded-3xl p-8 hover:border-ayur-gold transition-all shadow-sm hover:shadow-card-hover flex flex-col justify-between space-y-6"
            >
              <div className="space-y-4">
                <div className="w-12 h-12 rounded-full bg-ayur-forest text-ayur-gold flex items-center justify-center font-serif font-bold text-xl">
                  📜
                </div>
                <h2 className="font-serif text-2xl font-bold text-ayur-forest leading-snug">
                  {item.title}
                </h2>
                <p className="text-sm text-ayur-sage leading-relaxed">
                  {item.description}
                </p>
              </div>

              <div className="pt-6 border-t border-ayur-border/60 flex items-center justify-between">
                <span className="text-xs font-bold text-ayur-gold uppercase tracking-wider">Classical Source Manuscript</span>
                <Link
                  href={`/articles/${item.slug}`}
                  className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-ayur-forest hover:text-ayur-emerald transition-colors"
                >
                  Read Study
                  <ArrowRight className="w-4 h-4 text-ayur-gold" />
                </Link>
              </div>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}
