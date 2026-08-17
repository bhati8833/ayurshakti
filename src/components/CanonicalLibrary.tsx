'use client';

import React from 'react';
import Link from 'next/link';
import { motion } from 'motion/react';
import { Compass, BookCheck, ArrowRight, Sparkles, ScrollText } from 'lucide-react';
import { ArticleDoc } from '@/lib/markdown';

export default function CanonicalLibrary({ canonicals }: { canonicals: ArticleDoc[] }) {
  return (
    <section className="py-24 bg-ayur-card/50 relative border-y border-ayur-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Title */}
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white text-ayur-forest border border-ayur-gold/40 text-xs font-semibold uppercase tracking-widest shadow-sm">
            <ScrollText className="w-4 h-4 text-ayur-gold" />
            Sanskrit Classical Repository
          </span>
          <h2 className="font-serif text-3xl sm:text-5xl font-bold text-ayur-forest">
            Canonical Texts & Puranic Manuscripts
          </h2>
          <p className="text-ayur-sage text-base sm:text-lg">
            Direct English translations and analytical studies of classical Sanskrit works on Ayurveda, Mrigayurveda (veterinary care), and Vrikshayurvedic agriculture.
          </p>
        </div>

        {/* Canonical Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {canonicals.slice(0, 4).map((text, idx) => (
            <motion.div
              key={text.slug}
              initial={{ opacity: 0, y: 25 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: idx * 0.15 }}
              className="glass-panel rounded-2xl p-8 hover:border-ayur-gold/60 transition-all shadow-sm hover:shadow-card-hover group flex flex-col justify-between"
            >
              <div className="space-y-4">
                <div className="w-10 h-10 rounded-full bg-ayur-forest text-ayur-gold flex items-center justify-center font-serif font-bold text-sm">
                  📜
                </div>
                <h3 className="font-serif text-2xl font-bold text-ayur-forest group-hover:text-ayur-emerald transition-colors leading-snug">
                  {text.title}
                </h3>
                <p className="text-sm text-ayur-sage line-clamp-3 leading-relaxed">
                  {text.description}
                </p>
              </div>

              <div className="pt-6 mt-6 border-t border-ayur-border/60 flex items-center justify-between">
                <span className="text-xs font-semibold uppercase tracking-wider text-ayur-gold">Classical Source Manuscript</span>
                <Link
                  href={`/articles/${text.slug}`}
                  className="inline-flex items-center gap-1.5 text-xs font-bold text-ayur-forest uppercase tracking-wider group-hover:text-ayur-emerald transition-colors"
                >
                  Read Manuscript
                  <ArrowRight className="w-4 h-4 text-ayur-gold group-hover:translate-x-1 transition-transform" />
                </Link>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Callout Footer Link */}
        <div className="mt-16 text-center">
          <Link
            href="/canonical-texts"
            className="inline-flex items-center gap-2 text-xs font-bold text-ayur-forest uppercase tracking-widest hover:text-ayur-emerald transition-colors underline decoration-ayur-gold decoration-2 underline-offset-4"
          >
            Explore Complete Sanskrit Canonical Library ({canonicals.length} Volumes)
            <ArrowRight className="w-4 h-4 text-ayur-gold" />
          </Link>
        </div>

      </div>
    </section>
  );
}
