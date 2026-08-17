import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { getSiloDocs } from '@/lib/markdown';
import { PawPrint, ChevronRight, ShieldCheck, HeartPulse } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Veterinary Ayurveda & Pet Health | Mrigayurveda | AyurShakti',
  description: 'Ancient Ayurvedic veterinary sciences, Hastyayurveda (elephantology), Matangalila, and natural herbal care protocols for pets and domestic animals.',
  alternates: {
    canonical: '/pet-health',
  },
};

export default function PetHealthSiloPage() {
  const docs = getSiloDocs('pet-health');

  return (
    <main className="min-h-screen bg-ayur-bg pb-20">
      {/* Hero Header */}
      <section className="relative py-16 sm:py-24 bg-gradient-to-b from-ayur-forest via-ayur-forest/95 to-ayur-bg text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl">
            <span className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-ayur-gold/20 text-ayur-gold border border-ayur-gold/30 text-xs font-semibold uppercase tracking-wider mb-6">
              <PawPrint className="w-4 h-4" /> Ancient Mrigayurveda
            </span>
            <h1 className="font-serif text-4xl sm:text-6xl font-bold tracking-tight text-white mb-6 leading-tight">
              Veterinary Ayurveda & Pet Health
            </h1>
            <p className="text-lg sm:text-xl text-ayur-sand/90 font-sans leading-relaxed mb-8">
              Explore classical Sanskrit treatises on animal health (Pashu Ayurveda), elephantology (Hastyayurveda), and herbal holistic care for pets.
            </p>
          </div>
        </div>
      </section>

      {/* Docs Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-10 relative z-20">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {docs.map((doc) => (
            <div
              key={doc.slug}
              className="glass-panel p-8 rounded-3xl border border-ayur-gold/30 bg-white hover:shadow-xl transition-all duration-300 flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="px-3 py-1 rounded-full bg-ayur-forest/10 text-ayur-forest text-xs font-bold uppercase tracking-wider">
                    {doc.category}
                  </span>
                  <PawPrint className="w-6 h-6 text-ayur-gold group-hover:scale-110 transition-transform" />
                </div>

                <h2 className="font-serif text-2xl font-bold text-ayur-forest mb-3 group-hover:text-ayur-emerald transition-colors">
                  {doc.title}
                </h2>

                <p className="text-sm text-ayur-sage leading-relaxed mb-6">
                  {doc.description}
                </p>
              </div>

              <div className="pt-4 border-t border-ayur-border/40 flex items-center justify-between">
                <span className="text-xs font-semibold text-ayur-gold">
                  {doc.readingTime}
                </span>
                <Link
                  href={`/pet-health/${doc.slug}`}
                  className="px-5 py-2.5 rounded-full bg-ayur-forest text-white text-xs font-bold uppercase tracking-wider hover:bg-ayur-emerald transition-colors flex items-center gap-2"
                >
                  Read Study <ChevronRight className="w-4 h-4" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
