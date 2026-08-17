import React from 'react';
import { Metadata } from 'next';
import HeroSection from '@/components/HeroSection';
import CredibilityBanner from '@/components/CredibilityBanner';
import DoshaQuizWidget from '@/components/DoshaQuizWidget';
import FeaturedArticles from '@/components/FeaturedArticles';
import CanonicalLibrary from '@/components/CanonicalLibrary';
import { getAllArticles } from '@/lib/markdown';

export const metadata: Metadata = {
  title: 'Ayurvedic Remedies & Evidence-Based Protocols | AyurShakti',
  description: 'Explore evidence-based Ayurvedic remedies, Sanskrit canonical text analysis (Charaka & Sushruta Samhita), herbal botanical profiles, and PubMed peer-reviewed protocols by Suresh Bhati.',
  alternates: {
    canonical: '/',
  },
};

export default function HomePage() {
  const allArticles = getAllArticles();
  
  const standardArticles = allArticles.filter((a) => !a.isCanonicalText);

  return (
    <div className="space-y-0">
      {/* 1. Cinematic Hero Section */}
      <HeroSection />

      {/* 2. Scientific Methodology & Credibility Banner */}
      <CredibilityBanner />

      {/* 3. Interactive Dosha Self-Assessment */}
      <section className="px-4 sm:px-6 lg:px-8 pt-12">
        <DoshaQuizWidget />
      </section>

      {/* 4. Featured Evidence-Based Research Grid */}
      <FeaturedArticles articles={standardArticles.length > 0 ? standardArticles : allArticles} />

      {/* 5. Sanskrit Canonical Repository */}
      <CanonicalLibrary />
    </div>
  );
}
