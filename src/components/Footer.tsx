'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Sparkles, Send, Heart, BookOpen, Compass, ShieldCheck, Mail } from 'lucide-react';
import ObfuscatedEmail from '@/components/ObfuscatedEmail';

export default function Footer() {
  const [email, setEmail] = useState('');
  const [subscribed, setSubscribed] = useState(false);

  const handleSubscribe = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      setSubscribed(true);
      setEmail('');
    }
  };

  return (
    <footer className="bg-ayur-forest text-ayur-bg relative overflow-hidden pt-20 pb-12 border-t-4 border-ayur-gold">
      
      {/* Background Soft Radial Glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[300px] bg-emerald-500/10 blur-[150px] pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        
        {/* Top Newsletter & Brand Quote Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 pb-16 border-b border-ayur-herbal/80 items-center">
          
          {/* Brand Intro Column */}
          <div className="lg:col-span-6 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-ayur-gold text-ayur-forest flex items-center justify-center font-bold">
                <Sparkles className="w-5 h-5 text-ayur-forest" />
              </div>
              <span className="font-serif text-3xl font-bold tracking-tight text-white">
                AyurShakti.shop
              </span>
            </div>

            <p className="text-ayur-bg/80 text-sm sm:text-base max-w-lg leading-relaxed">
              Bridging authentic classical Sanskrit Ayurvedic manuscripts with modern peer-reviewed PubMed research. Dedicated to holistic human and pet vitality.
            </p>

            <div className="flex items-center gap-4 text-xs font-semibold uppercase tracking-wider text-[#E5C158] pt-2">
              <span className="flex items-center gap-1.5"><ShieldCheck className="w-4 h-4 text-emerald-400" /> Peer Reviewed</span>
              <span>•</span>
              <span>Sanskrit Sourced</span>
              <span>•</span>
              <span>Evidence Based</span>
            </div>
          </div>

          {/* Newsletter Subscribe Box */}
          <div className="lg:col-span-6">
            <div className="p-8 rounded-3xl bg-ayur-herbal/60 border border-[#E5C158]/30 shadow-lg space-y-4">
              <div className="flex items-center gap-2">
                <Mail className="w-4 h-4 text-[#E5C158]" />
                <span className="text-xs font-bold uppercase tracking-widest text-[#E5C158]">Weekly Herbal Research Digest</span>
              </div>
              <h3 className="font-serif text-xl sm:text-2xl font-bold text-white">
                Subscribe for Science-Backed Protocols
              </h3>
              <p className="text-xs text-ayur-bg/70">
                Join 5,000+ readers getting analytical studies on Ashwagandha, Giloy, Shatavari, and pet care directly to their inbox.
              </p>

              {subscribed ? (
                <div className="p-4 rounded-xl bg-emerald-950/80 border border-emerald-500/40 text-emerald-300 text-sm font-semibold flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-[#E5C158]" />
                  Thank you for subscribing! Welcome to AyurShakti Research.
                </div>
              ) : (
                <form onSubmit={handleSubscribe} className="flex flex-col sm:flex-row gap-2 pt-2">
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Enter your email address..."
                    required
                    className="flex-1 px-5 py-3 rounded-full bg-ayur-forest/90 border border-[#E5C158]/30 text-white placeholder-ayur-bg/50 text-sm focus:outline-none focus:border-[#E5C158] transition-colors"
                  />
                  <button
                    type="submit"
                    className="px-6 py-3 rounded-full bg-[#E5C158] text-ayur-forest font-bold text-xs uppercase tracking-wider hover:bg-white transition-colors flex items-center justify-center gap-2"
                  >
                    Subscribe <Send className="w-3.5 h-3.5" />
                  </button>
                </form>
              )}
            </div>
          </div>

        </div>

        {/* Links Navigation Matrix */}
        <div className="py-12 grid grid-cols-2 md:grid-cols-4 gap-8 border-b border-ayur-herbal/80 text-xs">
          
          <div className="space-y-3">
            <h4 className="font-bold text-[#E5C158] uppercase tracking-widest text-sm">Navigation Matrix</h4>
            <ul className="space-y-2 text-ayur-bg/80">
              <li><Link href="/" className="hover:text-[#E5C158] transition-colors">Home Landing</Link></li>
              <li><Link href="/samhitas" className="hover:text-[#E5C158] transition-colors">Classical Samhitas (366 Ch.)</Link></li>
              <li><Link href="/canonical-texts" className="hover:text-[#E5C158] transition-colors">Canonical Library (826 Pages)</Link></li>
              <li><Link href="/herbs" className="hover:text-[#E5C158] transition-colors">Herbal Library (42 Herbs)</Link></li>
              <li><Link href="/pet-health" className="hover:text-[#E5C158] transition-colors">Pet Health & Veterinary</Link></li>
              <li><Link href="/research" className="hover:text-[#E5C158] transition-colors">Research & Studies</Link></li>
              <li><Link href="/articles" className="hover:text-[#E5C158] transition-colors">Evidence-Based Articles</Link></li>
              <li><Link href="/glossary" className="hover:text-[#E5C158] transition-colors">A-Z Sanskrit Glossary (21k Terms)</Link></li>
              <li><Link href="/dosha-quiz" className="hover:text-[#E5C158] transition-colors">Take Dosha Assessment</Link></li>
            </ul>
          </div>

          <div className="space-y-3">
            <h4 className="font-bold text-[#E5C158] uppercase tracking-widest text-sm">Herbal Pillars</h4>
            <ul className="space-y-2 text-ayur-bg/80">
              <li><Link href="/herbs/ashwagandha" className="hover:text-[#E5C158] transition-colors">Ashwagandha Adaptogens</Link></li>
              <li><Link href="/herbs/giloy" className="hover:text-[#E5C158] transition-colors">Giloy Immunity Protocols</Link></li>
              <li><Link href="/herbs/shatavari" className="hover:text-[#E5C158] transition-colors">Shatavari Women's Health</Link></li>
              <li><Link href="/herbs/triphala" className="hover:text-[#E5C158] transition-colors">Triphala & Agni Digestion</Link></li>
              <li><Link href="/herbs/arjuna" className="hover:text-[#E5C158] transition-colors">Arjuna Cardiovascular</Link></li>
              <li><Link href="/herbs" className="hover:text-[#E5C158] transition-colors">Explore All 42 Profiles →</Link></li>
            </ul>
          </div>

          <div className="space-y-3">
            <h4 className="font-bold text-[#E5C158] uppercase tracking-widest text-sm">Pet Care (Mrigayurveda)</h4>
            <ul className="space-y-2 text-ayur-bg/80">
              <li><Link href="/pet-health/natural-remedies-for-dog-anxiety" className="hover:text-[#E5C158] transition-colors">Dog Anxiety Remedies</Link></li>
              <li><Link href="/pet-health/natural-remedies-dog-itchy-skin" className="hover:text-[#E5C158] transition-colors">Dog Itchy Skin & Neem</Link></li>
              <li><Link href="/pet-health/turmeric-for-dogs" className="hover:text-[#E5C158] transition-colors">Turmeric & Joint Health</Link></li>
              <li><Link href="/pet-health/coconut-oil-for-dogs" className="hover:text-[#E5C158] transition-colors">Coconut Oil for Dogs</Link></li>
              <li><Link href="/pet-health/triphala-for-dogs" className="hover:text-[#E5C158] transition-colors">Triphala for Canine Gut</Link></li>
              <li><Link href="/pet-health" className="hover:text-[#E5C158] transition-colors">View All Pet Protocols →</Link></li>
            </ul>
          </div>

          <div className="space-y-3">
            <h4 className="font-bold text-[#E5C158] uppercase tracking-widest text-sm">Transparency & About</h4>
            <ul className="space-y-2 text-ayur-bg/80">
              <li><Link href="/about" className="hover:text-[#E5C158] transition-colors">About Author Suresh Bhati</Link></li>
              <li><Link href="/methodology" className="hover:text-[#E5C158] transition-colors">Scientific Methodology</Link></li>
              <li><Link href="/dosha-guide" className="hover:text-[#E5C158] transition-colors">Dosha, Agni & Prakriti Guide</Link></li>
              <li><Link href="/sitemap.xml" className="hover:text-[#E5C158] transition-colors">XML Sitemap</Link></li>
              <li><ObfuscatedEmail className="hover:text-[#E5C158] transition-colors" /></li>
            </ul>
          </div>

        </div>

        {/* DRAMATIC OVERSIZED MONUMENTAL BRAND FOOTER TEXT */}
        <div className="py-12 text-center select-none overflow-hidden">
          <span className="font-serif text-[13vw] font-extrabold tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-ayur-gold/40 via-ayur-gold/15 to-transparent leading-none block uppercase opacity-80">
            AYURSHAKTI
          </span>
        </div>

        {/* Bottom Copyright & Byline */}
        <div className="pt-6 border-t border-ayur-herbal/60 flex flex-col sm:flex-row items-center justify-between text-xs text-ayur-bg/60 gap-4">
          <p>© {new Date().getFullYear()} AyurShakti.shop. All rights reserved.</p>
          <p className="flex items-center gap-1 font-medium text-ayur-bg/80">
            Crafted with <Heart className="w-3.5 h-3.5 text-rose-400 fill-rose-400" /> by <strong className="text-[#E5C158] font-serif">Suresh Bhati</strong>
          </p>
        </div>

      </div>
    </footer>
  );
}
