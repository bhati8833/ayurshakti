'use client';

import React, { useEffect, useState } from 'react';

interface TOCItem {
  id: string;
  text: string;
}

interface TableOfContentsProps {
  htmlContent: string;
}

export default function TableOfContents({ htmlContent }: TableOfContentsProps) {
  const [toc, setToc] = useState<TOCItem[]>([]);
  const [activeId, setActiveId] = useState<string>('');

  useEffect(() => {
    // Parse H2 headings from rendered HTML string
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlContent, 'text/html');
    const h2Elements = doc.querySelectorAll('h2');

    const items: TOCItem[] = [];
    h2Elements.forEach((h2, idx) => {
      const text = h2.textContent || `Section ${idx + 1}`;
      const id = h2.id || `section-${idx + 1}`;
      items.push({ id, text });
    });

    setToc(items);

    // Track active section on scroll
    const handleScroll = () => {
      const headingElements = Array.from(document.querySelectorAll('article h2'));
      const scrollPosition = window.scrollY + 150;

      for (let i = headingElements.length - 1; i >= 0; i--) {
        const el = headingElements[i];
        if (el && (el as HTMLElement).offsetTop <= scrollPosition) {
          setActiveId(el.id);
          break;
        }
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, [htmlContent]);

  if (toc.length === 0) return null;

  return (
    <nav className="glass-panel-gold rounded-3xl p-6 shadow-sm border border-ayur-gold/30">
      <h3 className="font-serif font-bold text-lg text-ayur-forest mb-4 flex items-center gap-2">
        <svg className="w-5 h-5 text-ayur-gold" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h7" />
        </svg>
        Table of Contents
      </h3>

      <ul className="space-y-2.5 text-sm">
        {toc.map((item) => {
          const isActive = activeId === item.id;
          return (
            <li key={item.id}>
              <a
                href={`#${item.id}`}
                className={`block transition-all duration-200 line-clamp-1 py-1 px-3 rounded-xl ${
                  isActive
                    ? 'bg-ayur-forest text-white font-semibold shadow-xs translate-x-1'
                    : 'text-ayur-forest/80 hover:text-ayur-forest hover:bg-ayur-gold/10'
                }`}
              >
                {item.text}
              </a>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
