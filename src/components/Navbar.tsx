'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'motion/react';
import {
  Sparkles,
  Menu,
  X,
  BookOpen,
  ChevronDown,
  Leaf,
  PawPrint,
  Microscope,
  Scroll,
  HeartPulse,
  ShieldCheck,
} from 'lucide-react';

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);

  const samhitaLinks = [
    { title: 'Charaka Samhita', slug: 'charaka-samhita', desc: 'Internal medicine & therapeutics (150 chapters)' },
    { title: 'Sushruta Samhita', slug: 'sushruta-samhita', desc: 'Ayurvedic surgery & anatomy (216 chapters)' },
  ];

  const herbLinks = [
    { title: 'Ashwagandha', slug: 'ashwagandha', desc: 'Vitality & Adaptogenic Strength' },
    { title: 'Shatavari', slug: 'shatavari', desc: 'Rejuvenation & Reproductive Health' },
    { title: 'Giloy (Guduchi)', slug: 'giloy', desc: 'Immunomodulator & Detoxifier' },
    { title: 'Triphala', slug: 'triphala', desc: 'Tridoshic Digestive Formula' },
    { title: 'Tulsi & Turmeric', slug: 'tulsi', desc: 'Respiratory & Anti-inflammatory' },
  ];

  const researchLinks = [
    { title: 'Rasa Shastra & Alchemy', slug: 'alchemy-in-india-and-china-by-vijaya-jayant-deshpande', desc: 'Ancient chemistry & metallic therapeutics' },
    { title: 'Ancient Indian Surgery', slug: 'surgery-in-ancient-india-study-by-p-p-prathapan', desc: 'Sushruta surgical traditions & instruments' },
    { title: 'Vrikshayurveda Botany', slug: 'vrikshayurveda-and-environmental-philosophy-by-beenapani', desc: 'Ancient plant pathology & herbal farming' },
    { title: 'Marma Shastra Science', slug: 'marma-sastra-and-ayurveda-study-by-c-suresh-kumar', desc: 'Vital energy points & anatomical therapy' },
  ];

  return (
    <header className="sticky top-0 z-50 w-full glass-panel border-b border-ayur-border transition-all duration-300 bg-white/90 backdrop-blur-md">
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

        {/* Desktop Navigation Links with Mega Menu */}
        <nav className="hidden md:flex items-center gap-6">
          <Link
            href="/"
            className="text-sm font-medium text-ayur-forest hover:text-ayur-emerald transition-colors py-2"
          >
            Home
          </Link>

          {/* 1. Samhitas Silo Dropdown */}
          <div
            className="relative"
            onMouseEnter={() => setActiveDropdown('samhitas')}
            onMouseLeave={() => setActiveDropdown(null)}
          >
            <Link
              href="/samhitas"
              className="text-sm font-medium text-ayur-forest hover:text-ayur-emerald transition-colors py-2 flex items-center gap-1.5"
            >
              <Scroll className="w-4 h-4 text-ayur-gold" />
              <span>Samhitas</span>
              <ChevronDown className="w-3.5 h-3.5 text-ayur-sage" />
            </Link>

            <AnimatePresence>
              {activeDropdown === 'samhitas' && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                  transition={{ duration: 0.15 }}
                  className="absolute top-full left-0 w-80 bg-white border border-ayur-border rounded-2xl shadow-xl p-4 mt-1 z-50"
                >
                  <div className="text-xs font-semibold uppercase tracking-wider text-ayur-gold mb-3 px-2">
                    Classical Sanskrit Library
                  </div>
                  <div className="space-y-1">
                    {samhitaLinks.map((item) => (
                      <Link
                        key={item.slug}
                        href={`/samhitas/${item.slug}`}
                        className="block p-2.5 rounded-xl hover:bg-ayur-sand/50 transition-colors group"
                      >
                        <div className="text-sm font-bold text-ayur-forest group-hover:text-ayur-emerald">
                          {item.title}
                        </div>
                        <div className="text-xs text-ayur-sage mt-0.5">{item.desc}</div>
                      </Link>
                    ))}
                  </div>
                  <div className="mt-3 pt-3 border-t border-ayur-border/40 text-center">
                    <Link href="/samhitas" className="text-xs font-bold text-ayur-emerald hover:underline">
                      Explore All Classical Texts →
                    </Link>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* 2. Herbs Silo Dropdown */}
          <div
            className="relative"
            onMouseEnter={() => setActiveDropdown('herbs')}
            onMouseLeave={() => setActiveDropdown(null)}
          >
            <Link
              href="/herbs"
              className="text-sm font-medium text-ayur-forest hover:text-ayur-emerald transition-colors py-2 flex items-center gap-1.5"
            >
              <Leaf className="w-4 h-4 text-ayur-gold" />
              <span>Herbal Library</span>
              <ChevronDown className="w-3.5 h-3.5 text-ayur-sage" />
            </Link>

            <AnimatePresence>
              {activeDropdown === 'herbs' && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                  transition={{ duration: 0.15 }}
                  className="absolute top-full left-0 w-80 bg-white border border-ayur-border rounded-2xl shadow-xl p-4 mt-1 z-50"
                >
                  <div className="text-xs font-semibold uppercase tracking-wider text-ayur-gold mb-3 px-2">
                    Botanical Materia Medica
                  </div>
                  <div className="space-y-1">
                    {herbLinks.map((item) => (
                      <Link
                        key={item.slug}
                        href={`/herbs/${item.slug}`}
                        className="block p-2.5 rounded-xl hover:bg-ayur-sand/50 transition-colors group"
                      >
                        <div className="text-sm font-bold text-ayur-forest group-hover:text-ayur-emerald">
                          {item.title}
                        </div>
                        <div className="text-xs text-ayur-sage mt-0.5">{item.desc}</div>
                      </Link>
                    ))}
                  </div>
                  <div className="mt-3 pt-3 border-t border-ayur-border/40 text-center">
                    <Link href="/herbs" className="text-xs font-bold text-ayur-emerald hover:underline">
                      View All Herb Profiles →
                    </Link>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* 3. Pet Care Silo Link */}
          <Link
            href="/pet-health"
            className="text-sm font-medium text-ayur-forest hover:text-ayur-emerald transition-colors py-2 flex items-center gap-1.5"
          >
            <PawPrint className="w-4 h-4 text-ayur-gold" />
            <span>Pet Health</span>
          </Link>

          {/* 4. Research Silo Dropdown */}
          <div
            className="relative"
            onMouseEnter={() => setActiveDropdown('research')}
            onMouseLeave={() => setActiveDropdown(null)}
          >
            <Link
              href="/research"
              className="text-sm font-medium text-ayur-forest hover:text-ayur-emerald transition-colors py-2 flex items-center gap-1.5"
            >
              <Microscope className="w-4 h-4 text-ayur-gold" />
              <span>Research</span>
              <ChevronDown className="w-3.5 h-3.5 text-ayur-sage" />
            </Link>

            <AnimatePresence>
              {activeDropdown === 'research' && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                  transition={{ duration: 0.15 }}
                  className="absolute top-full right-0 w-80 bg-white border border-ayur-border rounded-2xl shadow-xl p-4 mt-1 z-50"
                >
                  <div className="text-xs font-semibold uppercase tracking-wider text-ayur-gold mb-3 px-2">
                    Ayurvedic History & Studies
                  </div>
                  <div className="space-y-1">
                    {researchLinks.map((item) => (
                      <Link
                        key={item.slug}
                        href={`/research/${item.slug}`}
                        className="block p-2.5 rounded-xl hover:bg-ayur-sand/50 transition-colors group"
                      >
                        <div className="text-sm font-bold text-ayur-forest group-hover:text-ayur-emerald">
                          {item.title}
                        </div>
                        <div className="text-xs text-ayur-sage mt-0.5">{item.desc}</div>
                      </Link>
                    ))}
                  </div>
                  <div className="mt-3 pt-3 border-t border-ayur-border/40 text-center">
                    <Link href="/research" className="text-xs font-bold text-ayur-emerald hover:underline">
                      Explore All Research Studies →
                    </Link>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* 5. Glossary Link */}
          <Link
            href="/glossary"
            className="text-sm font-medium text-ayur-forest hover:text-ayur-emerald transition-colors py-2 flex items-center gap-1.5"
          >
            <BookOpen className="w-4 h-4 text-ayur-gold" />
            <span>Glossary</span>
          </Link>

          {/* 6. Methodology Link */}
          <Link
            href="/methodology"
            className="text-sm font-medium text-ayur-forest hover:text-ayur-emerald transition-colors py-2 flex items-center gap-1.5"
          >
            <ShieldCheck className="w-4 h-4 text-ayur-gold" />
            <span>Methodology</span>
          </Link>
        </nav>

        {/* Action Button */}
        <div className="hidden lg:flex items-center gap-4">
          <Link
            href="/dosha-quiz"
            className="px-5 py-2.5 rounded-full bg-ayur-forest text-ayur-bg text-xs font-semibold uppercase tracking-wider hover:bg-ayur-emerald transition-all duration-300 shadow-md hover:shadow-lg hover:-translate-y-0.5 flex items-center gap-2"
          >
            <HeartPulse className="w-4 h-4 text-ayur-gold" />
            <span>Dosha Quiz</span>
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
            className="md:hidden bg-white border-b border-ayur-border px-6 py-6 space-y-4 max-h-[85vh] overflow-y-auto"
          >
            <Link
              href="/"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-base font-bold text-ayur-forest py-2 border-b border-ayur-border/40"
            >
              Home
            </Link>

            <div className="py-2 border-b border-ayur-border/40">
              <div className="font-bold text-sm text-ayur-gold uppercase tracking-wider mb-2 flex items-center gap-2">
                <Scroll className="w-4 h-4" /> Classical Samhitas
              </div>
              <div className="pl-4 space-y-2">
                <Link
                  href="/samhitas/charaka-samhita"
                  onClick={() => setMobileMenuOpen(false)}
                  className="block text-sm text-ayur-forest font-semibold hover:text-ayur-emerald"
                >
                  Charaka Samhita (150 Ch.)
                </Link>
                <Link
                  href="/samhitas/sushruta-samhita"
                  onClick={() => setMobileMenuOpen(false)}
                  className="block text-sm text-ayur-forest font-semibold hover:text-ayur-emerald"
                >
                  Sushruta Samhita (216 Ch.)
                </Link>
              </div>
            </div>

            <div className="py-2 border-b border-ayur-border/40">
              <div className="font-bold text-sm text-ayur-gold uppercase tracking-wider mb-2 flex items-center gap-2">
                <Leaf className="w-4 h-4" /> Herbal Library
              </div>
              <div className="pl-4 space-y-2">
                <Link
                  href="/herbs"
                  onClick={() => setMobileMenuOpen(false)}
                  className="block text-sm text-ayur-forest font-semibold hover:text-ayur-emerald"
                >
                  All Herb Profiles
                </Link>
              </div>
            </div>

            <Link
              href="/pet-health"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-base font-bold text-ayur-forest py-2 border-b border-ayur-border/40 flex items-center gap-2"
            >
              <PawPrint className="w-4 h-4 text-ayur-gold" /> Pet Health & Veterinary
            </Link>

            <Link
              href="/research"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-base font-bold text-ayur-forest py-2 border-b border-ayur-border/40 flex items-center gap-2"
            >
              <Microscope className="w-4 h-4 text-ayur-gold" /> Research & Studies
            </Link>

            <Link
              href="/glossary"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-base font-bold text-ayur-forest py-2 border-b border-ayur-border/40 flex items-center gap-2"
            >
              <BookOpen className="w-4 h-4 text-ayur-gold" /> A-Z Sanskrit Glossary
            </Link>

            <div className="pt-3">
              <Link
                href="/dosha-quiz"
                onClick={() => setMobileMenuOpen(false)}
                className="w-full justify-center px-5 py-3 rounded-xl bg-ayur-forest text-ayur-bg text-sm font-semibold uppercase tracking-wider flex items-center gap-2 shadow-md"
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
