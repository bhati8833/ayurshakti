'use client';

import React, { useState } from 'react';
import ArticleCard from '@/components/ArticleCard';
import { ArticleDoc } from '@/lib/markdown';
import { Search, BookOpen, Sparkles } from 'lucide-react';

export default function ArticlesClient({ articles }: { articles: ArticleDoc[] }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedLabel, setSelectedLabel] = useState('All');

  // Collect labels
  const allLabels = ['All', ...Array.from(new Set(articles.flatMap((a) => a.labels)))].slice(0, 8);

  const filteredArticles = articles.filter((art) => {
    const matchesSearch =
      art.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      art.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      art.content.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesLabel = selectedLabel === 'All' || art.labels.includes(selectedLabel);

    return matchesSearch && matchesLabel;
  });

  return (
    <div className="py-16 bg-ayur-bg min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-12">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white text-ayur-forest border border-ayur-gold/40 text-xs font-semibold uppercase tracking-widest shadow-sm">
            <BookOpen className="w-4 h-4 text-ayur-emerald" />
            Comprehensive Repository ({articles.length} Articles)
          </span>
          <h1 className="font-serif text-4xl sm:text-6xl font-bold text-ayur-forest">
            Ayurvedic Remedies & Research Protocols
          </h1>
          <p className="text-ayur-sage text-lg">
            Explore authentic Ayurvedic remedies, herbal adaptogen guides, and PubMed-backed citations for holistic wellbeing.
          </p>

          {/* Search Bar */}
          <div className="pt-4 max-w-xl mx-auto relative">
            <div className="relative flex items-center">
              <Search className="w-5 h-5 text-ayur-sage absolute left-4 pointer-events-none" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search articles by keyword (e.g. Ashwagandha, Dog Anxiety, PCOS)..."
                className="w-full pl-12 pr-4 py-4 rounded-full bg-white border border-ayur-border text-ayur-forest placeholder-ayur-sage focus:outline-none focus:border-ayur-emerald shadow-sm transition-colors text-sm"
              />
            </div>
          </div>

          {/* Label Filter Pills */}
          <div className="flex flex-wrap items-center justify-center gap-2 pt-4">
            {allLabels.map((lbl) => (
              <button
                key={lbl}
                onClick={() => setSelectedLabel(lbl)}
                className={`px-4 py-2 rounded-full text-xs font-semibold uppercase tracking-wider transition-all ${
                  selectedLabel === lbl
                    ? 'bg-ayur-forest text-ayur-bg shadow-md'
                    : 'bg-white text-ayur-forest border border-ayur-border hover:bg-ayur-sand'
                }`}
              >
                {lbl}
              </button>
            ))}
          </div>
        </div>

        {/* Results Grid */}
        {filteredArticles.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredArticles.map((art, idx) => (
              <ArticleCard key={art.slug} article={art} index={idx} />
            ))}
          </div>
        ) : (
          <div className="text-center py-20 bg-white rounded-3xl border border-ayur-border max-w-md mx-auto">
            <Sparkles className="w-10 h-10 text-ayur-gold mx-auto mb-3" />
            <h3 className="font-serif text-xl font-bold text-ayur-forest">No articles found</h3>
            <p className="text-sm text-ayur-sage mt-1">Try adjusting your search terms or filter selection.</p>
          </div>
        )}

      </div>
    </div>
  );
}
