'use client';

import React from 'react';
import Link from 'next/link';
import { motion } from 'motion/react';
import { Sparkles, ArrowRight, ShieldCheck, Microscope, BookOpenCheck, HeartPulse } from 'lucide-react';

export default function HeroSection() {
  return (
    <section className="relative overflow-hidden pt-12 pb-24 lg:pt-20 lg:pb-32 bg-gradient-to-b from-ayur-bg via-ayur-card/40 to-ayur-bg">
      
      {/* Background Soft Organic Glow Orbs */}
      <div className="absolute top-10 left-1/2 -translate-x-1/2 w-[600px] h-[350px] bg-emerald-200/20 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute top-40 right-10 w-[300px] h-[300px] bg-amber-200/20 blur-[100px] rounded-full pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        
        {/* Top Eyebrow Tag */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
          className="flex justify-center mb-6"
        >
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white border border-ayur-gold/30 text-ayur-forest text-xs font-semibold uppercase tracking-widest shadow-sm">
            <Sparkles className="w-3.5 h-3.5 text-ayur-gold" />
            Verified Classical Ayurveda & Scientific PubMed Citations
          </span>
        </motion.div>

        {/* Hero Monumental Headline */}
        <div className="text-center max-w-4xl mx-auto space-y-6">
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
            className="font-serif text-4xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-ayur-forest leading-[1.12]"
          >
            Ancient Herbal Wisdom.{' '}
            <span className="block italic font-serif font-normal text-ayur-emerald underline decoration-ayur-gold/40 decoration-wavy decoration-2">
              Backed by Modern Science.
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4, ease: [0.16, 1, 0.3, 1] }}
            className="text-lg sm:text-xl text-ayur-sage max-w-2xl mx-auto leading-relaxed"
          >
            Explore evidence-based Ayurvedic remedies, Sanskrit canonical texts, and PubMed peer-reviewed botanical protocols for human and pet vitality.
          </motion.p>

          {/* Action CTAs */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6, ease: [0.16, 1, 0.3, 1] }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4"
          >
            <Link
              href="/articles"
              className="w-full sm:w-auto px-8 py-4 rounded-full bg-ayur-forest text-ayur-bg font-semibold text-sm tracking-wide uppercase shadow-lg hover:bg-ayur-emerald transition-all duration-300 flex items-center justify-center gap-3 group hover:-translate-y-1"
            >
              Explore Research Articles
              <ArrowRight className="w-4 h-4 text-ayur-gold group-hover:translate-x-1 transition-transform" />
            </Link>

            <Link
              href="/dosha-quiz"
              className="w-full sm:w-auto px-8 py-4 rounded-full bg-white border border-ayur-border text-ayur-forest font-semibold text-sm tracking-wide uppercase shadow-sm hover:border-ayur-gold hover:bg-ayur-sand transition-all duration-300 flex items-center justify-center gap-2"
            >
              <HeartPulse className="w-4 h-4 text-ayur-emerald" />
              Take Dosha Quiz
            </Link>
          </motion.div>
        </div>

        {/* Floating Dosha Pills */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1, delay: 0.8, ease: [0.16, 1, 0.3, 1] }}
          className="mt-16 grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-3xl mx-auto"
        >
          {/* Vata Card */}
          <div className="glass-panel rounded-2xl p-6 text-center hover:border-ayur-emerald/40 transition-all duration-300 shadow-sm hover:shadow-md">
            <div className="w-12 h-12 rounded-full bg-emerald-100 text-ayur-emerald flex items-center justify-center mx-auto mb-3 font-serif font-bold text-xl">
              वात
            </div>
            <h3 className="font-serif font-bold text-lg text-ayur-forest">Vata (Air & Space)</h3>
            <p className="text-xs text-ayur-sage mt-1">Controls movement, nervous system, and creative energy.</p>
          </div>

          {/* Pitta Card */}
          <div className="glass-panel rounded-2xl p-6 text-center hover:border-ayur-gold/40 transition-all duration-300 shadow-sm hover:shadow-md">
            <div className="w-12 h-12 rounded-full bg-amber-100 text-amber-700 flex items-center justify-center mx-auto mb-3 font-serif font-bold text-xl">
              पित्त
            </div>
            <h3 className="font-serif font-bold text-lg text-ayur-forest">Pitta (Fire & Water)</h3>
            <p className="text-xs text-ayur-sage mt-1">Governs digestion (Agni), metabolism, and focus.</p>
          </div>

          {/* Kapha Card */}
          <div className="glass-panel rounded-2xl p-6 text-center hover:border-ayur-emerald/40 transition-all duration-300 shadow-sm hover:shadow-md">
            <div className="w-12 h-12 rounded-full bg-teal-100 text-teal-800 flex items-center justify-center mx-auto mb-3 font-serif font-bold text-xl">
              कफ
            </div>
            <h3 className="font-serif font-bold text-lg text-ayur-forest">Kapha (Earth & Water)</h3>
            <p className="text-xs text-ayur-sage mt-1">Provides physical stamina, immunity, and joint lubrication.</p>
          </div>
        </motion.div>

        {/* Feature Badges Grid */}
        <div className="mt-16 pt-8 border-t border-ayur-border/60 grid grid-cols-2 md:grid-cols-4 gap-6 max-w-5xl mx-auto text-center">
          <div className="flex flex-col items-center">
            <Microscope className="w-6 h-6 text-ayur-emerald mb-2" />
            <span className="text-xs font-semibold uppercase text-ayur-forest tracking-wider">PubMed Peer-Reviewed</span>
          </div>
          <div className="flex flex-col items-center">
            <BookOpenCheck className="w-6 h-6 text-ayur-gold mb-2" />
            <span className="text-xs font-semibold uppercase text-ayur-forest tracking-wider">Sanskrit Manuscripts</span>
          </div>
          <div className="flex flex-col items-center">
            <ShieldCheck className="w-6 h-6 text-ayur-emerald mb-2" />
            <span className="text-xs font-semibold uppercase text-ayur-forest tracking-wider">100% Herbal Safety</span>
          </div>
          <div className="flex flex-col items-center">
            <HeartPulse className="w-6 h-6 text-ayur-gold mb-2" />
            <span className="text-xs font-semibold uppercase text-ayur-forest tracking-wider">Human & Pet Wellness</span>
          </div>
        </div>

      </div>
    </section>
  );
}
