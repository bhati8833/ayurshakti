'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { ArticleDoc } from '@/lib/markdown';
import ArticleCard from './ArticleCard';
import { ArrowRight, BookOpen } from 'lucide-react';

export default function FeaturedArticles({ articles }: { articles: ArticleDoc[] }) {
  const [selectedCategory, setSelectedCategory] = useState<string>('All');

  // Extract unique categories
  const categories = ['All', ...Array.from(new Set(articles.map((a) => a.category))).slice(0, 5)];

  const filteredArticles =
    selectedCategory === 'All'
      ? articles.slice(0, 6)
      : articles.filter((a) => a.category === selectedCategory).slice(0, 6);

  return (
    <section className="py-20 bg-ayur-bg relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-6">
          <div>
            <span className="inline-flex items-center gap-1.5 text-xs font-bold uppercase tracking-widest text-ayur-gold mb-2">
              <BookOpen className="w-4 h-4 text-ayur-emerald" />
              Evidence-Based Library
            </span>
            <h2 className="font-serif text-3xl sm:text-5xl font-bold text-ayur-forest tracking-tight">
              Featured Ayurvedic Remedies & Clinical Protocols
            </h2>
          </div>

          {/* Category Filter Pills */}
          <div className="flex flex-wrap items-center gap-2">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-4 py-2 rounded-full text-xs font-semibold uppercase tracking-wider transition-all ${
                  selectedCategory === cat
                    ? 'bg-ayur-forest text-ayur-bg shadow-md'
                    : 'bg-white text-ayur-forest border border-ayur-border hover:bg-ayur-sand'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Article Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredArticles.map((article, idx) => (
            <ArticleCard key={article.slug} article={article} index={idx} />
          ))}
        </div>

        {/* View All Articles Link */}
        <div className="mt-16 text-center">
          <Link
            href="/articles"
            className="inline-flex items-center gap-3 px-8 py-4 rounded-full bg-white border border-ayur-forest text-ayur-forest font-semibold text-xs uppercase tracking-widest hover:bg-ayur-forest hover:text-ayur-bg transition-all duration-300 shadow-sm hover:shadow-md group"
          >
            Explore All {articles.length} Research Articles
            <ArrowRight className="w-4 h-4 text-ayur-gold group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>

      </div>
    </section>
  );
}
