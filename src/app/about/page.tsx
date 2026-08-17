import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { Sparkles, ShieldCheck, Microscope, ScrollText, Mail } from 'lucide-react';
import ObfuscatedEmail from '@/components/ObfuscatedEmail';

export const metadata: Metadata = {
  title: 'About Suresh Bhati & AyurShakti | Mission & Scientific Vision',
  description: 'Learn about Suresh Bhati and the mission of AyurShakti: bridging ancient Sanskrit medical treatises with modern PubMed-backed botanical pharmacology.',
  alternates: {
    canonical: '/about',
  },
};

export default function AboutPage() {
  return (
    <div className="py-16 bg-ayur-bg min-h-screen">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-16">
        
        {/* Header */}
        <div className="text-center space-y-4">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white text-ayur-forest border border-ayur-gold/40 text-xs font-semibold uppercase tracking-widest shadow-sm">
            <Sparkles className="w-4 h-4 text-ayur-gold" />
            Founder & Lead Author
          </span>
          <h1 className="font-serif text-4xl sm:text-6xl font-bold text-ayur-forest">
            About Suresh Bhati & AyurShakti
          </h1>
          <p className="text-ayur-sage text-lg leading-relaxed max-w-2xl mx-auto">
            Demystifying classical Sanskrit medical manuscripts with rigorous peer-reviewed PubMed research to bring safe, authentic herbal protocols to modern living.
          </p>
        </div>

        {/* Story Section */}
        <div className="glass-panel-gold rounded-3xl p-8 sm:p-12 border border-ayur-gold/30 shadow-soft-glow space-y-6">
          <h2 className="font-serif text-2xl sm:text-3xl font-bold text-ayur-forest">
            The Mission Behind AyurShakti
          </h2>
          <div className="text-ayur-forest space-y-4 text-base sm:text-lg leading-relaxed">
            <p>
              Ayurveda is one of the world's oldest holistic healing systems, dating back over 3,000 years. However, in the modern digital age, Ayurvedic information is often diluted, generalized, or presented without scientific backing.
            </p>
            <p>
              <strong>AyurShakti.shop</strong> was founded by <strong>Suresh Bhati</strong> to solve this exact problem: to create a trusted digital repository where every herbal remedy is directly rooted in classical Sanskrit manuscripts (such as Charaka Samhita, Sushruta Samhita, and Vrikshayurveda) and validated with contemporary peer-reviewed pharmacological studies.
            </p>
          </div>
        </div>

        {/* 3 Core Pillars */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="glass-panel rounded-2xl p-6 text-center space-y-3">
            <ScrollText className="w-8 h-8 text-ayur-gold mx-auto" />
            <h3 className="font-serif font-bold text-lg text-ayur-forest">Classical Sourcing</h3>
            <p className="text-xs text-ayur-sage">Direct translations from ancient Sanskrit texts on human and pet botanical care.</p>
          </div>

          <div className="glass-panel rounded-2xl p-6 text-center space-y-3">
            <Microscope className="w-8 h-8 text-ayur-emerald mx-auto" />
            <h3 className="font-serif font-bold text-lg text-ayur-forest">PubMed Validation</h3>
            <p className="text-xs text-ayur-sage">Correlating active phytonutrients (withanolides, curcuminoids) with clinical studies.</p>
          </div>

          <div className="glass-panel rounded-2xl p-6 text-center space-y-3">
            <ShieldCheck className="w-8 h-8 text-ayur-emerald mx-auto" />
            <h3 className="font-serif font-bold text-lg text-ayur-forest">Safety & Purity</h3>
            <p className="text-xs text-ayur-sage">Clear dosage guidelines, safety contraindications, and adaptogenic protocols.</p>
          </div>
        </div>

        {/* Contact & Inquiry Box */}
        <div className="bg-ayur-forest rounded-3xl p-8 sm:p-12 text-white space-y-6 text-center">
          <h2 className="font-serif text-3xl font-bold">Have Questions or Research Inquiries?</h2>
          <p className="text-sm text-ayur-bg/80 max-w-lg mx-auto">
            We welcome scientific collaborations, research questions, and reader feedback.
          </p>
          <div className="pt-2">
            <ObfuscatedEmail
              className="inline-flex items-center gap-2 px-8 py-4 rounded-full bg-ayur-gold text-ayur-forest font-bold text-xs uppercase tracking-wider hover:bg-white transition-all shadow-lg"
            >
              <Mail className="w-4 h-4" /> Contact Suresh Bhati (contact@ayurshakti.shop)
            </ObfuscatedEmail>
          </div>
        </div>

      </div>
    </div>
  );
}
