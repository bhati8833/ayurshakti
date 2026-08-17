'use client';

import React from 'react';
import Link from 'next/link';
import { motion } from 'motion/react';
import { ArrowRight, ScrollText, Leaf, PawPrint, Microscope } from 'lucide-react';

export default function CanonicalLibrary() {
  const silos = [
    {
      title: 'Classical Samhitas',
      slug: '/samhitas',
      icon: ScrollText,
      badge: '366 Chapters',
      desc: 'Complete English translations of Charaka Samhita and Sushruta Samhita with chapter-by-chapter therapeutics and surgical wisdom.',
    },
    {
      title: 'Botanical Herbal Library',
      slug: '/herbs',
      icon: Leaf,
      badge: 'Dravyaguna Studies',
      desc: 'Authenticated adaptogens and herbs like Ashwagandha, Shatavari, Giloy, and Triphala with energetic profiles and clinical research.',
    },
    {
      title: 'Pet Health & Veterinary',
      slug: '/pet-health',
      icon: PawPrint,
      badge: 'Mrigayurveda',
      desc: 'Ancient Indian veterinary sciences, elephantology (Hastyayurveda), and natural herbal care protocols for pets.',
    },
    {
      title: 'Research & Alchemy',
      slug: '/research',
      icon: Microscope,
      badge: 'Rasa Shastra',
      desc: 'Academic papers on ancient surgery, Rasa Shastra mineral alchemy, Marma points, and ethnobotanical studies.',
    },
  ];

  return (
    <section className="py-24 bg-ayur-card/50 relative border-y border-ayur-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Title */}
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white text-ayur-forest border border-ayur-gold/40 text-xs font-semibold uppercase tracking-widest shadow-sm">
            <ScrollText className="w-4 h-4 text-ayur-gold" />
            Topical Knowledge Silos
          </span>
          <h2 className="font-serif text-3xl sm:text-5xl font-bold text-ayur-forest">
            Sanskrit Canonical Samhitas & Ayurvedic Knowledge Hubs
          </h2>
          <p className="text-ayur-sage text-base sm:text-lg">
            Organized into dedicated Ayurvedic knowledge hubs for intuitive navigation, deep search engine indexing, and evidence-based study.
          </p>
        </div>

        {/* Silo Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {silos.map((silo, idx) => {
            const Icon = silo.icon;
            return (
              <motion.div
                key={silo.slug}
                initial={{ opacity: 0, y: 25 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: idx * 0.15 }}
                className="glass-panel rounded-3xl p-8 hover:border-ayur-gold/60 transition-all shadow-sm hover:shadow-card-hover group flex flex-col justify-between bg-white"
              >
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="w-12 h-12 rounded-2xl bg-ayur-forest/10 text-ayur-forest flex items-center justify-center group-hover:bg-ayur-forest group-hover:text-ayur-gold transition-colors">
                      <Icon className="w-6 h-6" />
                    </div>
                    <span className="px-3 py-1 rounded-full bg-ayur-sand text-ayur-forest text-xs font-bold uppercase tracking-wider">
                      {silo.badge}
                    </span>
                  </div>

                  <h3 className="font-serif text-2xl font-bold text-ayur-forest group-hover:text-ayur-emerald transition-colors leading-snug">
                    {silo.title}
                  </h3>

                  <p className="text-sm text-ayur-sage leading-relaxed">
                    {silo.desc}
                  </p>
                </div>

                <div className="pt-6 mt-6 border-t border-ayur-border/60 flex items-center justify-between">
                  <span className="text-xs font-semibold uppercase tracking-wider text-ayur-gold">
                    Authoritative Hub
                  </span>
                  <Link
                    href={silo.slug}
                    className="inline-flex items-center gap-1.5 text-xs font-bold text-ayur-forest uppercase tracking-wider group-hover:text-ayur-emerald transition-colors"
                  >
                    Enter Silo Hub
                    <ArrowRight className="w-4 h-4 text-ayur-gold group-hover:translate-x-1 transition-transform" />
                  </Link>
                </div>
              </motion.div>
            );
          })}
        </div>

      </div>
    </section>
  );
}
