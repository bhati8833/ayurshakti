import React from 'react';
import Link from 'next/link';
import { Clock, Tag, ArrowUpRight } from 'lucide-react';
import { ArticleDoc } from '@/lib/markdown';

export default function ArticleCard({ article }: { article: ArticleDoc; index?: number }) {
  return (
    <article className="glass-panel rounded-2xl p-6 sm:p-8 flex flex-col justify-between hover:border-ayur-emerald/40 hover:shadow-card-hover transition-all duration-300 group">
      <div className="space-y-4">
        {/* Category Badge, Published Date & Reading Time */}
        <div className="flex items-center justify-between text-xs gap-2">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-ayur-sand text-ayur-forest font-semibold uppercase tracking-wider">
            <Tag className="w-3 h-3 text-ayur-gold" />
            {article.category}
          </span>
          <div className="flex items-center gap-2 text-ayur-sage font-medium">
            <span>{article.publishedDate ? new Date(article.publishedDate).toLocaleDateString('en-US', { month: 'short', year: 'numeric' }) : 'Aug 2026'}</span>
            <span>•</span>
            <span className="flex items-center gap-1">
              <Clock className="w-3.5 h-3.5" />
              {article.readingTime}
            </span>
          </div>
        </div>

        {/* Title */}
        <Link href={`/articles/${article.slug}`}>
          <h3 className="font-serif text-xl sm:text-2xl font-bold text-ayur-forest group-hover:text-ayur-emerald transition-colors leading-snug">
            {article.title}
          </h3>
        </Link>

        {/* Description Excerpt */}
        <p className="text-sm text-ayur-sage line-clamp-3 leading-relaxed">
          {article.description}
        </p>
      </div>

      {/* Author & Footer Link */}
      <div className="pt-6 mt-6 border-t border-ayur-border/60 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-full bg-ayur-forest text-[#E5C158] flex items-center justify-center text-xs font-serif font-bold">
            SB
          </div>
          <span className="text-xs font-medium text-ayur-forest">Suresh Bhati</span>
        </div>

        <Link
          href={`/articles/${article.slug}`}
          className="inline-flex items-center gap-1 text-xs font-bold text-ayur-emerald uppercase tracking-wider group-hover:text-ayur-forest transition-colors"
        >
          Read Protocol
          <ArrowUpRight className="w-4 h-4 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
        </Link>
      </div>
    </article>
  );
}
