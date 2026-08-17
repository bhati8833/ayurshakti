'use client';

import React from 'react';
import Link from 'next/link';
import { motion } from 'motion/react';
import { Clock, Tag, ArrowUpRight, User } from 'lucide-react';
import { ArticleDoc } from '@/lib/markdown';

export default function ArticleCard({ article, index }: { article: ArticleDoc; index: number }) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-50px' }}
      transition={{ duration: 0.6, delay: (index % 3) * 0.15, ease: [0.16, 1, 0.3, 1] }}
      className="glass-panel rounded-2xl p-6 sm:p-8 flex flex-col justify-between hover:border-ayur-emerald/40 hover:shadow-card-hover transition-all duration-300 group"
    >
      <div className="space-y-4">
        {/* Category Badge & Reading Time */}
        <div className="flex items-center justify-between text-xs">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-ayur-sand text-ayur-forest font-semibold uppercase tracking-wider">
            <Tag className="w-3 h-3 text-ayur-gold" />
            {article.category}
          </span>
          <span className="flex items-center gap-1 text-ayur-sage font-medium">
            <Clock className="w-3.5 h-3.5" />
            {article.readingTime}
          </span>
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
          <div className="w-7 h-7 rounded-full bg-ayur-forest text-ayur-gold flex items-center justify-center text-xs font-serif font-bold">
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
    </motion.article>
  );
}
