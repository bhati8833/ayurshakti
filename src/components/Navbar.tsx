'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'motion/react';
import { Sparkles, Menu, X, BookOpen, Compass, ShieldCheck, HeartPulse } from 'lucide-react';

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full glass-panel border-b border-ayur-border transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        
        {/* Brand Logo */}
        <Link href="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-full bg-ayur-forest flex items-center justify-center text-ayur-gold shadow-md group-hover:scale-105 transition-transform duration-300">
            <Sparkles className="w-5 h-5" />
          </div>
          <div className="flex flex-col">
            <span className="font-serif text-2xl font-bold tracking-tight text-ayur-forest group-hover:text-ayur-emerald transition-colors">
              AyurShakti
            </span>
            <span className="text-[10px] tracking-widest uppercase font-semibold text-ayur-gold -mt-1">
              Holistic Herbals & Science
            </span>
          </div>
        </Link>

        {/* Desktop Navigation Links */}
        <nav className="hidden md:flex items-center gap-8">
          <Link
            href="/"
            className="text-sm font-medium text-ayur-forest hover:text-ayur-emerald transition-colors relative py-1 after:content-[''] after:absolute after:bottom-0 after:left-0 after:w-0 after:h-0.5 after:bg-ayur-emerald hover:after:w-full after:transition-all"
          >
            Home
          </Link>
          <Link
            href="/articles"
            className="text-sm font-medium text-ayur-forest hover:text-ayur-emerald transition-colors relative py-1 after:content-[''] after:absolute after:bottom-0 after:left-0 after:w-0 after:h-0.5 after:bg-ayur-emerald hover:after:w-full after:transition-all flex items-center gap-1.5"
          >
            <BookOpen className="w-4 h-4 text-ayur-gold" />
            Articles & Research
          </Link>
          <Link
            href="/canonical-texts"
            className="text-sm font-medium text-ayur-forest hover:text-ayur-emerald transition-colors relative py-1 after:content-[''] after:absolute after:bottom-0 after:left-0 after:w-0 after:h-0.5 after:bg-ayur-emerald hover:after:w-full after:transition-all flex items-center gap-1.5"
          >
            <Compass className="w-4 h-4 text-ayur-gold" />
            Canonical Texts
          </Link>
          <Link
            href="/glossary"
            className="text-sm font-medium text-ayur-forest hover:text-ayur-emerald transition-colors relative py-1 after:content-[''] after:absolute after:bottom-0 after:left-0 after:w-0 after:h-0.5 after:bg-ayur-emerald hover:after:w-full after:transition-all flex items-center gap-1.5"
          >
            <BookOpen className="w-4 h-4 text-ayur-gold" />
            A-Z Glossary
          </Link>
          <Link
            href="/dosha-quiz"
            className="text-sm font-medium text-ayur-forest hover:text-ayur-emerald transition-colors relative py-1 after:content-[''] after:absolute after:bottom-0 after:left-0 after:w-0 after:h-0.5 after:bg-ayur-emerald hover:after:w-full after:transition-all flex items-center gap-1.5"
          >
            <HeartPulse className="w-4 h-4 text-ayur-gold" />
            Dosha Quiz
          </Link>
          <Link
            href="/about"
            className="text-sm font-medium text-ayur-forest hover:text-ayur-emerald transition-colors relative py-1 after:content-[''] after:absolute after:bottom-0 after:left-0 after:w-0 after:h-0.5 after:bg-ayur-emerald hover:after:w-full after:transition-all"
          >
            About Suresh Bhati
          </Link>
        </nav>

        {/* Action Button */}
        <div className="hidden lg:flex items-center gap-4">
          <Link
            href="/dosha-quiz"
            className="px-5 py-2.5 rounded-full bg-ayur-forest text-ayur-bg text-xs font-semibold uppercase tracking-wider hover:bg-ayur-emerald transition-all duration-300 shadow-md hover:shadow-lg hover:-translate-y-0.5 flex items-center gap-2"
          >
            <ShieldCheck className="w-4 h-4 text-ayur-gold" />
            Find Your Dosha
          </Link>
        </div>

        {/* Mobile Menu Button */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="md:hidden p-2 rounded-lg text-ayur-forest hover:bg-ayur-sand transition-colors"
          aria-label="Toggle Navigation Menu"
        >
          {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile Drawer Menu */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden bg-ayur-bg border-b border-ayur-border px-6 py-6 space-y-4"
          >
            <Link
              href="/"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-base font-medium text-ayur-forest py-2 border-b border-ayur-border/50"
            >
              Home
            </Link>
            <Link
              href="/articles"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-base font-medium text-ayur-forest py-2 border-b border-ayur-border/50"
            >
              Articles & Research
            </Link>
            <Link
              href="/canonical-texts"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-base font-medium text-ayur-forest py-2 border-b border-ayur-border/50"
            >
              Canonical Texts
            </Link>
            <Link
              href="/dosha-quiz"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-base font-medium text-ayur-forest py-2 border-b border-ayur-border/50"
            >
              Dosha Quiz
            </Link>
            <Link
              href="/about"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-base font-medium text-ayur-forest py-2 border-b border-ayur-border/50"
            >
              About Suresh Bhati
            </Link>
            <div className="pt-2">
              <Link
                href="/dosha-quiz"
                onClick={() => setMobileMenuOpen(false)}
                className="w-full justify-center px-5 py-3 rounded-xl bg-ayur-forest text-ayur-bg text-sm font-semibold uppercase tracking-wider flex items-center gap-2"
              >
                <ShieldCheck className="w-4 h-4 text-ayur-gold" />
                Find Your Dosha
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
