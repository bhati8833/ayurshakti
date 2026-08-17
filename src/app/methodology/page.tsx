import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { ScrollText, Microscope, ShieldCheck, Award, BookOpen, CheckCircle2, FileCode, ExternalLink } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Scientific Methodology & Source Vetting Policy | AyurShakti',
  description: 'Learn how AyurShakti vets 3,000-year-old Sanskrit Samhitas and correlates them with modern PubMed peer-reviewed pharmacology. Authored by Suresh Bhati.',
  alternates: {
    canonical: '/methodology',
  },
};

export default function MethodologyPage() {
  const jsonLdMethodology = {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    '@id': 'https://ayurshakti.shop/methodology#webpage',
    url: 'https://ayurshakti.shop/methodology',
    name: 'Scientific Methodology & Source Vetting Policy',
    description: 'Detailed methodology on Sanskrit manuscript translation and PubMed pharmacological verification by Suresh Bhati.',
    publisher: {
      '@type': 'Organization',
      name: 'AyurShakti',
      url: 'https://ayurshakti.shop',
    },
    author: {
      '@type': 'Person',
      name: 'Suresh Bhati',
      url: 'https://ayurshakti.shop/about',
    },
  };

  return (
    <main className="min-h-screen bg-ayur-bg pb-24">
      {/* Schema.org JSON-LD */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdMethodology) }}
      />

      {/* Breadcrumb */}
      <nav aria-label="Breadcrumb" className="bg-ayur-forest/5 border-b border-ayur-border/40 py-3">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-xs font-semibold text-ayur-sage flex items-center gap-2">
          <Link href="/" className="hover:text-ayur-emerald transition-colors">Home</Link>
          <span>/</span>
          <span className="text-ayur-forest">Editorial Methodology</span>
        </div>
      </nav>

      {/* Hero Header */}
      <header className="bg-gradient-to-b from-ayur-forest via-ayur-forest/95 to-ayur-bg text-white py-16 sm:py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-4">
          <span className="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-full bg-ayur-gold/20 text-ayur-gold border border-ayur-gold/30 text-xs font-bold uppercase tracking-widest">
            <Award className="w-4 h-4 text-ayur-gold" /> Evidence & Editorial Standards
          </span>
          <h1 className="font-serif text-3xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-white">
            Our Scientific Methodology & Vetting Framework
          </h1>
          <p className="text-sm sm:text-lg text-ayur-sand/90 max-w-2xl mx-auto leading-relaxed">
            How AyurShakti validates 3,000-year-old Sanskrit treatises alongside peer-reviewed PubMed pharmacological research.
          </p>
        </div>
      </header>

      {/* Body Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 mt-12 space-y-12">
        
        {/* Intro Card */}
        <section className="glass-panel p-8 sm:p-10 rounded-3xl border border-ayur-gold/30 bg-white space-y-6 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-ayur-forest text-ayur-gold flex items-center justify-center font-bold">
              <ScrollText className="w-6 h-6" />
            </div>
            <div>
              <h2 className="font-serif text-2xl font-bold text-ayur-forest">Dual-Layer Verification Protocol</h2>
              <p className="text-xs text-ayur-sage font-medium uppercase tracking-wider">Authored by Suresh Bhati • Updated August 2026</p>
            </div>
          </div>
          <p className="text-ayur-forest text-base leading-relaxed">
            Ayurveda is one of the world's oldest medical systems, documented in classical Sanskrit manuscripts such as the <em>Charaka Samhita</em>, <em>Sushruta Samhita</em>, and <em>Astanga Hridaya</em>. However, modern integrative healthcare requires both classical textual fidelity and empirical biochemical verification.
          </p>
          <p className="text-ayur-sage text-sm leading-relaxed">
            At AyurShakti, every article, botanical profile, and veterinary protocol is evaluated through a strict 4-step evidence pipeline before publication.
          </p>
        </section>

        {/* Step-by-Step Vetting Pipeline */}
        <section className="space-y-8">
          <h2 className="font-serif text-3xl font-bold text-ayur-forest text-center">
            The 4-Step Verification Process
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Step 1 */}
            <div className="p-6 rounded-2xl bg-white border border-ayur-gold/20 shadow-xs space-y-3">
              <span className="px-3 py-1 rounded-full bg-ayur-sand text-ayur-forest text-xs font-bold uppercase tracking-wider">Step 1</span>
              <h3 className="font-serif text-xl font-bold text-ayur-forest flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-ayur-emerald" /> Primary Sanskrit Text Analysis
              </h3>
              <p className="text-xs text-ayur-sage leading-relaxed">
                We review original Devanagari verses from <em>Charaka Samhita</em> (Sutrasthana, Chikitsasthana), <em>Sushruta Samhita</em> (Sharirasthana), and <em>Bhavaprakasha Nighantu</em>. Verse numbers are cataloged and cross-referenced.
              </p>
            </div>

            {/* Step 2 */}
            <div className="p-6 rounded-2xl bg-white border border-ayur-gold/20 shadow-xs space-y-3">
              <span className="px-3 py-1 rounded-full bg-ayur-sand text-ayur-forest text-xs font-bold uppercase tracking-wider">Step 2</span>
              <h3 className="font-serif text-xl font-bold text-ayur-forest flex items-center gap-2">
                <Microscope className="w-5 h-5 text-ayur-gold" /> PubMed & NCBI Phytotherapy Correlation
              </h3>
              <p className="text-xs text-ayur-sage leading-relaxed">
                Therapeutic claims are matched against double-blind, randomized controlled trials (RCTs) indexed on PubMed. Active phytochemicals (e.g. <em>withanolides</em> in Ashwagandha, <em>bacosides</em> in Brahmi) are verified with PMIDs.
              </p>
            </div>

            {/* Step 3 */}
            <div className="p-6 rounded-2xl bg-white border border-ayur-gold/20 shadow-xs space-y-3">
              <span className="px-3 py-1 rounded-full bg-ayur-sand text-ayur-forest text-xs font-bold uppercase tracking-wider">Step 3</span>
              <h3 className="font-serif text-xl font-bold text-ayur-forest flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-ayur-emerald" /> Safety & Species-Specific Dosage Vetting
              </h3>
              <p className="text-xs text-ayur-sage leading-relaxed">
                Safety parameters are established including organ-specific contraindications (liver/kidney toxicity thresholds) and species-specific dosing rules for canine and feline veterinary care (*Mrigayurveda*).
              </p>
            </div>

            {/* Step 4 */}
            <div className="p-6 rounded-2xl bg-white border border-ayur-gold/20 shadow-xs space-y-3">
              <span className="px-3 py-1 rounded-full bg-ayur-sand text-ayur-forest text-xs font-bold uppercase tracking-wider">Step 4</span>
              <h3 className="font-serif text-xl font-bold text-ayur-forest flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5 text-ayur-gold" /> Continuous Peer Review & Updates
              </h3>
              <p className="text-xs text-ayur-sage leading-relaxed">
                Articles are updated annually or when new clinical study data emerges. All updates display clear publication and last-reviewed date markers.
              </p>
            </div>

          </div>
        </section>

        {/* Transparency Banner */}
        <section className="glass-panel p-8 rounded-3xl bg-ayur-forest text-white space-y-4">
          <h2 className="font-serif text-2xl font-bold text-ayur-gold">Editorial Independence & Citation Policy</h2>
          <p className="text-sm text-ayur-sand leading-relaxed">
            AyurShakti operates as an independent educational resource. We do not sell pharmaceutical products or receive commercial sponsorship for therapeutic claims. All citations link directly to open-access PubMed research papers and public manuscript repositories.
          </p>
          <div className="pt-2 flex flex-wrap gap-4 text-xs font-bold uppercase tracking-wider">
            <Link href="/about" className="px-4 py-2 rounded-full bg-ayur-gold text-ayur-forest hover:bg-white transition-colors">
              Meet Lead Author Suresh Bhati
            </Link>
            <Link href="/samhitas" className="px-4 py-2 rounded-full bg-white/10 text-white hover:bg-white/20 transition-colors">
              Browse Samhita Library
            </Link>
          </div>
        </section>

      </div>
    </main>
  );
}
