import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { Sparkles, Flame, ShieldCheck, HeartPulse, HelpCircle, ArrowRight, CheckCircle2 } from 'lucide-react';
import DoshaQuizWidget from '@/components/DoshaQuizWidget';

export const metadata: Metadata = {
  title: 'Beginners Guide to Ayurvedic Concepts: Dosha, Agni & Prakriti | AyurShakti',
  description: 'A comprehensive beginner guide explaining Dosha (Vata, Pitta, Kapha), Agni (digestive fire), Prakriti (body constitution), Ojas, and Ama. Authored by Suresh Bhati.',
  alternates: {
    canonical: '/dosha-guide',
  },
};

export default function DoshaGuidePage() {
  const jsonLdGuide = {
    '@context': 'https://schema.org',
    '@type': 'EducationalArticle',
    '@id': 'https://ayurshakti.shop/dosha-guide#article',
    url: 'https://ayurshakti.shop/dosha-guide',
    headline: 'Beginners Guide to Ayurvedic Concepts: Dosha, Agni & Prakriti',
    description: 'A beginner-friendly guide to core Ayurvedic principles: Vata, Pitta, Kapha, Agni, and Prakriti.',
    author: {
      '@type': 'Person',
      name: 'Suresh Bhati',
      url: 'https://ayurshakti.shop/about',
    },
    publisher: {
      '@type': 'Organization',
      name: 'AyurShakti',
      url: 'https://ayurshakti.shop',
    },
  };

  return (
    <main className="min-h-screen bg-ayur-bg pb-24">
      {/* Schema.org JSON-LD */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdGuide) }}
      />

      {/* Breadcrumb */}
      <nav aria-label="Breadcrumb" className="bg-ayur-forest/5 border-b border-ayur-border/40 py-3">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-xs font-semibold text-ayur-sage flex items-center gap-2">
          <Link href="/" className="hover:text-ayur-emerald transition-colors">Home</Link>
          <span>/</span>
          <span className="text-ayur-forest">Ayurvedic Core Concepts Guide</span>
        </div>
      </nav>

      {/* Hero Header */}
      <header className="bg-gradient-to-b from-ayur-forest via-ayur-forest/95 to-ayur-bg text-white py-16 sm:py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-4">
          <span className="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-full bg-ayur-gold/20 text-ayur-gold border border-ayur-gold/30 text-xs font-bold uppercase tracking-widest">
            <Sparkles className="w-4 h-4 text-ayur-gold" /> Ayurvedic Fundamentals 101
          </span>
          <h1 className="font-serif text-3xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-white leading-tight">
            Understanding Dosha, Agni & Prakriti
          </h1>
          <p className="text-sm sm:text-lg text-ayur-sand/90 max-w-2xl mx-auto leading-relaxed">
            The ultimate beginner's manual to ancient Indian mind-body physiology, metabolic balance, and constitutional health.
          </p>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 mt-12 space-y-12">
        
        {/* Section 1: The Three Doshas */}
        <section className="glass-panel p-8 sm:p-12 rounded-3xl border border-ayur-gold/30 bg-white space-y-8 shadow-xs">
          <div>
            <span className="px-3.5 py-1 rounded-full bg-ayur-sand text-ayur-forest font-bold text-xs uppercase tracking-wider">Concept 1</span>
            <h2 className="font-serif text-3xl font-bold text-ayur-forest mt-3">The Three Tridoshas (Vata, Pitta, Kapha)</h2>
            <p className="text-ayur-sage text-sm sm:text-base mt-2 leading-relaxed">
              In Ayurveda, physiological and psychological functions are governed by three primary energetic forces called <strong>Tridoshas</strong>. Every individual possesses a unique ratio of these three forces from birth.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            {/* Vata */}
            <div className="p-6 rounded-2xl bg-emerald-50/60 border border-emerald-200 space-y-3">
              <div className="w-10 h-10 rounded-full bg-emerald-700 text-white font-serif font-bold flex items-center justify-center">वात</div>
              <h3 className="font-serif font-bold text-xl text-emerald-950">Vata (Air & Space)</h3>
              <p className="text-xs text-emerald-800 leading-relaxed">
                Controls all bodily movement, nerve impulses, breathing, and circulatory flow. Attributes: Dry, light, cold, mobile.
              </p>
              <div className="text-[11px] font-semibold text-emerald-900 pt-2 border-t border-emerald-200">
                Imbalance Signs: Anxiety, insomnia, dry skin, constipation.
              </div>
            </div>

            {/* Pitta */}
            <div className="p-6 rounded-2xl bg-amber-50/60 border border-amber-200 space-y-3">
              <div className="w-10 h-10 rounded-full bg-amber-600 text-white font-serif font-bold flex items-center justify-center">पित्त</div>
              <h3 className="font-serif font-bold text-xl text-amber-950">Pitta (Fire & Water)</h3>
              <p className="text-xs text-amber-800 leading-relaxed">
                Governs digestion (Agni), cellular metabolism, body temperature, and mental focus. Attributes: Hot, sharp, oily, intense.
              </p>
              <div className="text-[11px] font-semibold text-amber-900 pt-2 border-t border-amber-200">
                Imbalance Signs: Acid reflux, inflammation, skin rashes, irritability.
              </div>
            </div>

            {/* Kapha */}
            <div className="p-6 rounded-2xl bg-teal-50/60 border border-teal-200 space-y-3">
              <div className="w-10 h-10 rounded-full bg-teal-700 text-white font-serif font-bold flex items-center justify-center">कफ</div>
              <h3 className="font-serif font-bold text-xl text-teal-950">Kapha (Earth & Water)</h3>
              <p className="text-xs text-teal-800 leading-relaxed">
                Provides physical structure, tissue stamina, immune defense, and joint lubrication. Attributes: Heavy, slow, cool, smooth.
              </p>
              <div className="text-[11px] font-semibold text-teal-900 pt-2 border-t border-teal-200">
                Imbalance Signs: Weight gain, congestion, sluggishness, fluid retention.
              </div>
            </div>

          </div>
        </section>

        {/* Section 2: Agni (Digestive Fire) */}
        <section className="glass-panel p-8 sm:p-12 rounded-3xl border border-ayur-gold/30 bg-white space-y-6 shadow-xs">
          <span className="px-3.5 py-1 rounded-full bg-ayur-sand text-ayur-forest font-bold text-xs uppercase tracking-wider">Concept 2</span>
          <h2 className="font-serif text-3xl font-bold text-ayur-forest flex items-center gap-3">
            <Flame className="w-7 h-7 text-amber-600" /> Agni: The Digestive & Metabolic Fire
          </h2>
          <p className="text-ayur-forest text-base leading-relaxed">
            Classical Ayurveda states that health begins in the gut with <strong>Agni</strong> (digestive fire). Robust Agni cleanly breaks down food, extracts nutrients, and creates <em>Ojas</em> (vital immunity). Impaired Agni creates <em>Ama</em> (toxic metabolic residue).
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
            <div className="p-5 rounded-2xl bg-ayur-bg border border-ayur-gold/20">
              <h3 className="font-serif font-bold text-base text-ayur-forest mb-1">Ama (Metabolic Toxins)</h3>
              <p className="text-xs text-ayur-sage">Undigested food residue that accumulates in the GI tract, causing fatigue, brain fog, and chronic inflammation.</p>
            </div>
            <div className="p-5 rounded-2xl bg-ayur-bg border border-ayur-gold/20">
              <h3 className="font-serif font-bold text-base text-ayur-forest mb-1">Ojas (Vital Energy)</h3>
              <p className="text-xs text-ayur-sage">The refined byproduct of healthy digestion that maintains cellular resilience, radiant skin, and natural immunity.</p>
            </div>
          </div>
        </section>

        {/* Section 3: Interactive Assessment Callout */}
        <section className="pt-6">
          <DoshaQuizWidget />
        </section>

        {/* Section 4: Next Steps */}
        <section className="p-8 rounded-3xl bg-ayur-forest text-white text-center space-y-4">
          <h2 className="font-serif text-2xl font-bold text-ayur-gold">Ready to Explore Evidence-Based Herbal Protocols?</h2>
          <p className="text-sm text-ayur-sand max-w-xl mx-auto">
            Discover how specific botanical herbs like Ashwagandha, Shatavari, and Giloy balance Vata, Pitta, and Kapha.
          </p>
          <div className="pt-2">
            <Link href="/herbs" className="inline-flex items-center gap-2 px-8 py-3.5 rounded-full bg-ayur-gold text-ayur-forest font-bold text-xs uppercase tracking-widest hover:bg-white transition-colors">
              Explore 42 Botanical Herb Profiles <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </section>

      </div>
    </main>
  );
}
