'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { BookOpen, ExternalLink } from 'lucide-react';

interface GlossaryTooltipProps {
  term: string;
  definition: string;
  category?: string;
  slug?: string;
  children: React.ReactNode;
}

export default function GlossaryTooltip({
  term,
  definition,
  category = 'Ayurvedic Lexicon',
  slug,
  children,
}: GlossaryTooltipProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <span
      className="relative inline-block group cursor-help"
      onMouseEnter={() => setIsOpen(true)}
      onMouseLeave={() => setIsOpen(false)}
    >
      <span className="text-ayur-emerald font-medium underline decoration-ayur-emerald/40 underline-offset-4 hover:decoration-ayur-emerald hover:text-ayur-forest transition-colors">
        {children}
      </span>

      {isOpen && (
        <span className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 p-4 rounded-2xl bg-white border border-ayur-gold/30 shadow-card z-50 text-left block text-xs space-y-2 pointer-events-none animate-in fade-in zoom-in-95 duration-150">
          <span className="flex items-center justify-between gap-2 border-b border-ayur-gold/20 pb-1.5">
            <span className="font-serif font-bold text-ayur-forest text-sm flex items-center gap-1.5">
              <BookOpen className="w-3.5 h-3.5 text-ayur-emerald" />
              {term}
            </span>
            <span className="px-2 py-0.5 rounded-full bg-ayur-forest/10 text-ayur-forest text-[10px] font-semibold uppercase">
              {category}
            </span>
          </span>
          <span className="text-ayur-sage block leading-relaxed font-normal">
            {definition}
          </span>
          {slug && (
            <span className="pt-1 block border-t border-ayur-gold/10 text-[11px] font-semibold text-ayur-emerald">
              Click to explore full lexicon entry →
            </span>
          )}
        </span>
      )}
    </span>
  );
}
