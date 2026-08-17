'use client';

import React, { useState, useMemo } from 'react';
import Link from 'next/link';
import { Search, Volume2, Share2, ArrowRight, Check, BookOpen, Sparkles, Filter, ChevronLeft, ChevronRight } from 'lucide-react';

export interface GlossaryTerm {
  term: string;
  devanagari: string;
  slug: string;
  letter: string;
  category: string;
  definition: string;
  dosha?: string;
  link?: string;
}

interface GlossarySearchProps {
  initialTerms: GlossaryTerm[];
  currentLetter?: string;
  totalCount?: number;
  showAlphabetBar?: boolean;
}

const ALPHABET = 'abcdefghijklmnopqrstuvwxyz'.split('');
const ITEMS_PER_PAGE = 48;

const CATEGORIES = [
  { id: 'all', label: 'All Categories' },
  { id: 'dravyaguna', label: 'Herbs & Botanicals' },
  { id: 'chikitsa', label: 'Treatments & Procedures' },
  { id: 'nidana', label: 'Pathology & Disorders' },
  { id: 'sharira', label: 'Anatomy & Physiology' },
  { id: 'lexicon', label: 'Classical Lexicon' },
];

export default function GlossarySearch({
  initialTerms,
  currentLetter,
  totalCount,
  showAlphabetBar = true,
}: GlossarySearchProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [copiedSlug, setCopiedSlug] = useState<string | null>(null);

  // Instant Live Filter
  const filteredTerms = useMemo(() => {
    return initialTerms.filter((item) => {
      // Keyword match (Name, Devanagari, Definition, Category)
      const q = searchTerm.trim().toLowerCase();
      const matchesSearch =
        !q ||
        item.term.toLowerCase().includes(q) ||
        item.devanagari.toLowerCase().includes(q) ||
        item.definition.toLowerCase().includes(q) ||
        item.category.toLowerCase().includes(q);

      // Category filter match
      let matchesCat = true;
      if (selectedCategory === 'dravyaguna') {
        matchesCat = item.category.toLowerCase().includes('dravyaguna') || item.category.toLowerCase().includes('herb');
      } else if (selectedCategory === 'chikitsa') {
        matchesCat = item.category.toLowerCase().includes('chikitsa') || item.category.toLowerCase().includes('treatment');
      } else if (selectedCategory === 'nidana') {
        matchesCat = item.category.toLowerCase().includes('nidana') || item.category.toLowerCase().includes('disorder');
      } else if (selectedCategory === 'sharira') {
        matchesCat = item.category.toLowerCase().includes('sharira') || item.category.toLowerCase().includes('anatomy');
      } else if (selectedCategory === 'lexicon') {
        matchesCat = item.category.toLowerCase().includes('lexicon');
      }

      return matchesSearch && matchesCat;
    });
  }, [initialTerms, searchTerm, selectedCategory]);

  // Reset pagination on search change
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1);
  };

  const handleCategoryChange = (catId: string) => {
    setSelectedCategory(catId);
    setCurrentPage(1);
  };

  // Pagination calculation
  const totalPages = Math.ceil(filteredTerms.length / ITEMS_PER_PAGE) || 1;
  const paginatedTerms = useMemo(() => {
    const start = (currentPage - 1) * ITEMS_PER_PAGE;
    return filteredTerms.slice(start, start + ITEMS_PER_PAGE);
  }, [filteredTerms, currentPage]);

  // Web Speech API Audio Pronunciation
  const speakTerm = (text: string) => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.85;
      utterance.pitch = 1.0;
      utterance.lang = 'hi-IN'; // Sanskrit phonetic fallback
      window.speechSynthesis.speak(utterance);
    }
  };

  // Copy shareable link
  const handleCopyLink = (term: GlossaryTerm) => {
    if (typeof window !== 'undefined' && navigator.clipboard) {
      const url = `${window.location.origin}/glossary/${term.letter.toLowerCase()}#${term.slug}`;
      navigator.clipboard.writeText(url);
      setCopiedSlug(term.slug);
      setTimeout(() => setCopiedSlug(null), 2000);
    }
  };

  return (
    <div className="space-y-8">
      
      {/* Search Input Hero Card */}
      <div className="glass-panel p-6 sm:p-10 rounded-3xl border border-ayur-gold/30 shadow-card bg-gradient-to-br from-white via-ayur-bg/40 to-ayur-gold/10 relative overflow-hidden">
        <div className="max-w-3xl mx-auto space-y-6">
          
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-ayur-forest/60">
              <Search className="w-5 h-5" />
            </div>
            <input
              type="text"
              value={searchTerm}
              onChange={handleSearchChange}
              placeholder="Search by term name, Devanagari script, or medical keyword (e.g. Abhyanga, Agni, Ama, Herb)..."
              className="w-full pl-12 pr-4 py-4 rounded-2xl border border-ayur-gold/40 bg-white/95 text-ayur-forest placeholder-ayur-sage focus:outline-none focus:ring-2 focus:ring-ayur-emerald focus:border-transparent text-base shadow-sm font-sans transition-all"
            />
            {searchTerm && (
              <button
                onClick={() => { setSearchTerm(''); setCurrentPage(1); }}
                className="absolute inset-y-0 right-0 pr-4 flex items-center text-xs font-semibold text-ayur-sage hover:text-ayur-forest uppercase tracking-wider"
              >
                Clear
              </button>
            )}
          </div>

          {/* Category Filter Pills */}
          <div className="flex flex-wrap items-center justify-center gap-2 pt-2">
            {CATEGORIES.map((cat) => {
              const isActive = selectedCategory === cat.id;
              return (
                <button
                  key={cat.id}
                  onClick={() => handleCategoryChange(cat.id)}
                  className={`px-4 py-2 rounded-full text-xs font-semibold tracking-wide transition-all ${
                    isActive
                      ? 'bg-ayur-forest text-ayur-gold shadow-md scale-105'
                      : 'bg-white/80 text-ayur-forest hover:bg-ayur-forest/10 border border-ayur-gold/20'
                  }`}
                >
                  {cat.label}
                </button>
              );
            })}
          </div>

        </div>
      </div>

      {/* A-Z Alphabet Quick Bar (Optional) */}
      {showAlphabetBar && (
        <div className="flex flex-wrap justify-center gap-1.5 p-3 rounded-2xl bg-white border border-ayur-gold/30 shadow-xs max-w-4xl mx-auto">
          {ALPHABET.map((l) => {
            const isActive = currentLetter?.toLowerCase() === l;
            return (
              <Link
                key={l}
                href={`/glossary/${l}`}
                className={`w-8 h-8 rounded-lg font-serif font-bold text-xs flex items-center justify-center transition-colors uppercase ${
                  isActive
                    ? 'bg-ayur-forest text-ayur-gold shadow-sm'
                    : 'text-ayur-forest hover:bg-ayur-forest/10'
                }`}
                title={`Browse letter ${l.toUpperCase()}`}
              >
                {l}
              </Link>
            );
          })}
        </div>
      )}

      {/* Results Header Counter */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-medium text-ayur-sage border-b border-ayur-gold/20 pb-4">
        <div>
          Showing <span className="font-bold text-ayur-forest">{filteredTerms.length.toLocaleString()}</span> terms
          {currentLetter && ` starting with letter '${currentLetter.toUpperCase()}'`}
          {searchTerm && ` matching "${searchTerm}"`}
        </div>
        {totalPages > 1 && (
          <div>
            Page <span className="font-bold text-ayur-forest">{currentPage}</span> of{' '}
            <span className="font-bold text-ayur-forest">{totalPages}</span>
          </div>
        )}
      </div>

      {/* Terms Grid */}
      {paginatedTerms.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {paginatedTerms.map((item) => (
            <div
              key={`${item.slug}-${item.term}`}
              id={item.slug}
              className="p-6 rounded-2xl border border-ayur-gold/20 bg-white hover:border-ayur-emerald/50 hover:shadow-card transition-all flex flex-col justify-between group space-y-4 relative"
            >
              <div className="space-y-3">
                {/* Header: Term Name + Devanagari Script */}
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h3 className="font-serif font-bold text-lg text-ayur-forest group-hover:text-ayur-emerald transition-colors flex items-center gap-2">
                      {item.term}
                      {item.devanagari && item.devanagari !== item.term && (
                        <span className="text-xs font-sans font-normal text-ayur-gold bg-ayur-forest/5 px-2 py-0.5 rounded-md">
                          {item.devanagari}
                        </span>
                      )}
                    </h3>
                  </div>

                  {/* Audio Speech & Copy Buttons */}
                  <div className="flex items-center gap-1 opacity-80 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={() => speakTerm(item.term)}
                      className="p-1.5 rounded-lg text-ayur-sage hover:text-ayur-emerald hover:bg-ayur-forest/5 transition-colors"
                      title="Listen to Sanskrit pronunciation"
                    >
                      <Volume2 className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => handleCopyLink(item)}
                      className="p-1.5 rounded-lg text-ayur-sage hover:text-ayur-emerald hover:bg-ayur-forest/5 transition-colors"
                      title="Copy shareable term link"
                    >
                      {copiedSlug === item.slug ? <Check className="w-4 h-4 text-emerald-600" /> : <Share2 className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {/* Category & Dosha Badge */}
                <div className="flex flex-wrap items-center gap-2">
                  <span className="px-2.5 py-0.5 rounded-full bg-ayur-forest/10 text-ayur-forest text-[11px] font-semibold uppercase tracking-wider">
                    {item.category}
                  </span>
                  {item.dosha && (
                    <span className="px-2.5 py-0.5 rounded-full bg-ayur-gold/20 text-ayur-forest text-[11px] font-medium">
                      {item.dosha}
                    </span>
                  )}
                </div>

                {/* Concise English Definition */}
                <p className="text-sm text-ayur-sage leading-relaxed">
                  {item.definition}
                </p>
              </div>

              {/* Internal Link to Herb/Samhita (If Available) */}
              {item.link && (
                <div className="pt-2 border-t border-ayur-gold/10">
                  <Link
                    href={item.link}
                    className="inline-flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-ayur-forest hover:text-ayur-emerald transition-colors"
                  >
                    View Botanical / Research Protocol
                    <ArrowRight className="w-3.5 h-3.5 text-ayur-gold group-hover:translate-x-1 transition-transform" />
                  </Link>
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        /* Empty State */
        <div className="text-center py-16 px-4 bg-white rounded-3xl border border-ayur-gold/20 space-y-4">
          <BookOpen className="w-12 h-12 text-ayur-gold mx-auto opacity-50" />
          <h3 className="font-serif text-xl font-bold text-ayur-forest">No Sanskrit Terms Found</h3>
          <p className="text-sm text-ayur-sage max-w-md mx-auto">
            We couldn't find any terms matching "{searchTerm}". Try clearing your search filter or selecting a different category.
          </p>
          <button
            onClick={() => { setSearchTerm(''); setSelectedCategory('all'); setCurrentPage(1); }}
            className="px-6 py-2.5 rounded-xl bg-ayur-forest text-ayur-gold text-xs font-semibold uppercase tracking-wider hover:bg-ayur-forest/90 transition-all shadow-sm"
          >
            Reset All Filters
          </button>
        </div>
      )}

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-2 pt-6">
          <button
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
            disabled={currentPage === 1}
            className="p-2.5 rounded-xl border border-ayur-gold/30 bg-white text-ayur-forest hover:bg-ayur-forest hover:text-ayur-gold disabled:opacity-40 disabled:hover:bg-white disabled:hover:text-ayur-forest transition-colors shadow-xs"
            title="Previous Page"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          
          <span className="px-4 py-2 rounded-xl bg-white border border-ayur-gold/30 text-xs font-bold text-ayur-forest shadow-xs">
            Page {currentPage} of {totalPages}
          </span>

          <button
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
            disabled={currentPage === totalPages}
            className="p-2.5 rounded-xl border border-ayur-gold/30 bg-white text-ayur-forest hover:bg-ayur-forest hover:text-ayur-gold disabled:opacity-40 disabled:hover:bg-white disabled:hover:text-ayur-forest transition-colors shadow-xs"
            title="Next Page"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      )}

    </div>
  );
}
