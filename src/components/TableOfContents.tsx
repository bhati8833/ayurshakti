'use client';

import React, { useEffect, useState } from 'react';

interface TOCItem {
  id: string;
  text: string;
  level: number; // 2 for h2, 3 for h3
}

interface TableOfContentsProps {
  htmlContent: string;
}

export default function TableOfContents({ htmlContent }: TableOfContentsProps) {
  const [toc, setToc] = useState<TOCItem[]>([]);
  const [activeId, setActiveId] = useState<string>('');

  useEffect(() => {
    // Parse H2 and H3 headings from rendered HTML string
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlContent, 'text/html');
    const headingNodes = doc.querySelectorAll('h2, h3');

    const items: TOCItem[] = [];
    headingNodes.forEach((node, idx) => {
      const level = node.tagName.toLowerCase() === 'h3' ? 3 : 2;
      let rawText = node.textContent?.trim() || `Section ${idx + 1}`;
      
      // Clean leading section numbers e.g. "45. Chapter 3" -> "Chapter 3"
      const cleanText = rawText.replace(/^(\d+[\.\s]+)+/, '').trim();
      const text = cleanText || rawText;

      let id = node.id;
      if (!id) {
        id = text
          .toLowerCase()
          .replace(/[^a-z0-9\s-]/g, '')
          .replace(/[\s-]+/g, '-')
          .replace(/^-+|-+$/g, '');
        if (!id) id = `section-${idx + 1}`;
      }

      items.push({ id, text, level });
    });

    setToc(items);

    // Track active section on scroll
    const handleScroll = () => {
      const headingElements = Array.from(document.querySelectorAll('h2[id], h3[id]'));
      if (headingElements.length === 0) return;

      const scrollPosition = window.scrollY + 140;

      for (let i = headingElements.length - 1; i >= 0; i--) {
        const el = headingElements[i] as HTMLElement;
        if (el && el.offsetTop <= scrollPosition) {
          setActiveId(el.id);
          break;
        }
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  }, [htmlContent]);

  const scrollToHeading = (e: React.MouseEvent<HTMLAnchorElement>, id: string) => {
    e.preventDefault();
    const element = document.getElementById(id);
    if (element) {
      const yOffset = -100;
      const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;
      window.scrollTo({ top: y, behavior: 'smooth' });
      setActiveId(id);
      window.history.pushState(null, '', `#${id}`);
    }
  };

  if (toc.length === 0) return null;

  return (
    <nav className="glass-panel-gold rounded-3xl p-6 shadow-sm border border-ayur-gold/30 bg-white/80 backdrop-blur-md">
      <h3 className="font-serif font-bold text-lg text-ayur-forest mb-4 flex items-center gap-2">
        <svg className="w-5 h-5 text-ayur-gold" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h7" />
        </svg>
        Table of Contents
      </h3>

      <ul className="space-y-1.5 text-xs max-h-[60vh] overflow-y-auto pr-1">
        {toc.map((item) => {
          const isActive = activeId === item.id;
          const isH3 = item.level === 3;

          return (
            <li key={item.id} className={isH3 ? 'pl-4' : ''}>
              <a
                href={`#${item.id}`}
                onClick={(e) => scrollToHeading(e, item.id)}
                className={`block transition-all duration-200 line-clamp-1 py-1 px-2.5 rounded-lg ${
                  isH3 ? 'text-ayur-forest/70 hover:text-ayur-forest' : 'font-semibold text-ayur-forest'
                } ${
                  isActive
                    ? 'bg-ayur-forest text-white font-bold shadow-xs translate-x-1'
                    : 'hover:bg-ayur-gold/15 text-ayur-forest/85'
                }`}
              >
                {isH3 ? `• ${item.text}` : item.text}
              </a>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}

