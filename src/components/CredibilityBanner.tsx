import React from 'react';
import Link from 'next/link';
import { ScrollText, Microscope, ShieldAlert, Award, CheckCircle2, UserCheck, Calendar, ArrowUpRight } from 'lucide-react';

export default function CredibilityBanner() {
  return (
    <section className="py-16 bg-white border-y border-ayur-gold/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header with Freshness Marker */}
        <div className="text-center max-w-3xl mx-auto mb-12 space-y-3">
          <div className="flex items-center justify-center gap-2 mb-2">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 text-emerald-800 text-xs font-bold uppercase tracking-wider border border-emerald-200">
              <Calendar className="w-3.5 h-3.5 text-emerald-600" />
              Peer-Reviewed & Updated: August 2026
            </span>
          </div>

          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-ayur-sand text-ayur-forest text-xs font-bold uppercase tracking-widest border border-ayur-gold/40">
            <Award className="w-4 h-4 text-ayur-gold" />
            Editorial Rigor & Scientific Transparency
          </span>
          
          <h2 className="font-serif text-3xl sm:text-4xl font-bold text-ayur-forest">
            How We Evaluate Ayurvedic Remedies & Manuscripts
          </h2>
          <p className="text-ayur-sage text-sm sm:text-base leading-relaxed">
            Every protocol published on AyurShakti undergoes a dual-layer verification framework: combining 3,000-year classical Sanskrit literature with contemporary PubMed pharmacology.
          </p>
        </div>

        {/* 4 Methodology Pillars */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          
          <div className="p-6 rounded-2xl bg-ayur-bg/70 border border-ayur-gold/20 hover:border-ayur-gold/50 transition-all space-y-3 shadow-sm">
            <div className="w-10 h-10 rounded-xl bg-ayur-forest text-[#E5C158] flex items-center justify-center font-bold">
              <ScrollText className="w-5 h-5 text-[#E5C158]" />
            </div>
            <h3 className="font-serif font-bold text-lg text-ayur-forest">1. Sanskrit Primary Sources</h3>
            <p className="text-xs text-ayur-sage leading-relaxed">
              Direct analysis of 366 chapters across <em>Charaka Samhita</em>, <em>Sushruta Samhita</em>, and <em>Bhavaprakasha Nighantu</em>.
            </p>
            <div className="flex items-center gap-1 text-[11px] font-semibold text-emerald-700 pt-2">
              <CheckCircle2 className="w-3.5 h-3.5" /> Direct Devanagari Translation
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-ayur-bg/70 border border-ayur-gold/20 hover:border-ayur-gold/50 transition-all space-y-3 shadow-sm">
            <div className="w-10 h-10 rounded-xl bg-ayur-forest text-[#E5C158] flex items-center justify-center font-bold">
              <Microscope className="w-5 h-5 text-[#E5C158]" />
            </div>
            <h3 className="font-serif font-bold text-lg text-ayur-forest">2. PubMed Validation</h3>
            <p className="text-xs text-ayur-sage leading-relaxed">
              Phytonutrient profiling (withanolides, curcuminoids, guggulsterones) matched with PubMed clinical trials.
            </p>
            <div className="flex items-center gap-1 text-[11px] font-semibold text-emerald-700 pt-2">
              <CheckCircle2 className="w-3.5 h-3.5" /> PMIDs Cited In-Text
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-ayur-bg/70 border border-ayur-gold/20 hover:border-ayur-gold/50 transition-all space-y-3 shadow-sm">
            <div className="w-10 h-10 rounded-xl bg-ayur-forest text-[#E5C158] flex items-center justify-center font-bold">
              <ShieldAlert className="w-5 h-5 text-[#E5C158]" />
            </div>
            <h3 className="font-serif font-bold text-lg text-ayur-forest">3. Safety & Dosages</h3>
            <p className="text-xs text-ayur-sage leading-relaxed">
              Clear body-weight dosing parameters, contraindications, and herb-drug interactions for humans and pets.
            </p>
            <div className="flex items-center gap-1 text-[11px] font-semibold text-emerald-700 pt-2">
              <CheckCircle2 className="w-3.5 h-3.5" /> Species-Specific Guidelines
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-ayur-bg/70 border border-ayur-gold/20 hover:border-ayur-gold/50 transition-all space-y-3 shadow-sm">
            <div className="w-10 h-10 rounded-xl bg-ayur-forest text-[#E5C158] flex items-center justify-center font-bold">
              <Award className="w-5 h-5 text-[#E5C158]" />
            </div>
            <h3 className="font-serif font-bold text-lg text-ayur-forest">4. Expert Bylines</h3>
            <p className="text-xs text-ayur-sage leading-relaxed">
              All guides researched and maintained by <strong>Suresh Bhati</strong>, ensuring editorial independence and accuracy.
            </p>
            <div className="flex items-center gap-1 text-[11px] font-semibold text-emerald-700 pt-2">
              <CheckCircle2 className="w-3.5 h-3.5" /> Transparent Attribution
            </div>
          </div>

        </div>

        {/* Lead Author Profile & Dataset Counters */}
        <div className="mt-12 pt-10 border-t border-ayur-border/60 grid grid-cols-1 lg:grid-cols-3 gap-8 items-center">
          
          {/* Author Badge */}
          <div className="lg:col-span-2 p-6 rounded-2xl bg-ayur-sand/50 border border-ayur-gold/30 flex flex-col sm:flex-row items-start sm:items-center gap-5">
            <div className="w-14 h-14 rounded-full bg-ayur-forest text-[#E5C158] flex items-center justify-center font-serif text-2xl font-bold shrink-0 shadow-md">
              SB
            </div>
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <h4 className="font-serif font-bold text-lg text-ayur-forest">Suresh Bhati</h4>
                <span className="px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[11px] font-semibold">Lead Author & Researcher</span>
              </div>
              <p className="text-xs text-ayur-sage leading-relaxed">
                Ayurvedic researcher specializing in classical Sanskrit medical translation, botanical pharmacognosy, and evidence-based veterinary remedies.
              </p>
              <div className="pt-1">
                <Link href="/about" className="inline-flex items-center gap-1 text-xs font-bold text-ayur-emerald uppercase tracking-wider hover:underline">
                  View Full Author Bio & Methodology
                  <ArrowUpRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          </div>

          {/* Dataset Metrics */}
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-white border border-ayur-border text-center">
              <span className="block font-serif text-2xl font-bold text-ayur-forest">366</span>
              <span className="text-[11px] text-ayur-sage uppercase font-semibold">Samhita Chapters</span>
            </div>
            <div className="p-4 rounded-xl bg-white border border-ayur-border text-center">
              <span className="block font-serif text-2xl font-bold text-ayur-forest">42</span>
              <span className="text-[11px] text-ayur-sage uppercase font-semibold">Herb Profiles</span>
            </div>
            <div className="p-4 rounded-xl bg-white border border-ayur-border text-center">
              <span className="block font-serif text-2xl font-bold text-ayur-forest">21,499</span>
              <span className="text-[11px] text-ayur-sage uppercase font-semibold">Sanskrit Terms</span>
            </div>
            <div className="p-4 rounded-xl bg-white border border-ayur-border text-center">
              <span className="block font-serif text-2xl font-bold text-ayur-forest">100%</span>
              <span className="text-[11px] text-ayur-sage uppercase font-semibold">Peer-Reviewed</span>
            </div>
          </div>

        </div>

      </div>
    </section>
  );
}
