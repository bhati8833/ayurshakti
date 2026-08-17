'use client';

import React, { useState, useEffect } from 'react';

interface ObfuscatedEmailProps {
  user?: string;
  domain?: string;
  className?: string;
  children?: React.ReactNode;
  showText?: boolean;
}

export default function ObfuscatedEmail({
  user = 'contact',
  domain = 'ayurshakti.shop',
  className = '',
  children,
  showText = true,
}: ObfuscatedEmailProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const fullEmail = `${user}@${domain}`;

  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    window.location.href = `mailto:${fullEmail}`;
  };

  // SSR/SSG Fallback: Prevents plain-text mailto: harvesting in static build HTML
  if (!mounted) {
    return (
      <a
        href="#"
        onClick={handleClick}
        className={className}
        aria-label="Contact via email"
      >
        {children || `${user} [at] ${domain}`}
      </a>
    );
  }

  return (
    <a
      href={`mailto:${fullEmail}`}
      onClick={handleClick}
      className={className}
      title={`Send email to ${fullEmail}`}
    >
      {children || (showText ? fullEmail : `${user} [at] ${domain}`)}
    </a>
  );
}
