import React from 'react';
import { Metadata } from 'next';
import HeroSection from '@/components/HeroSection';
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

      {/* 2. Interactive Dosha Self-Assessment */}
      <section className="px-4 sm:px-6 lg:px-8">
        <DoshaQuizWidget />
      </section>

      {/* 3. Featured Evidence-Based Research Grid */}
      <FeaturedArticles articles={standardArticles.length > 0 ? standardArticles : allArticles} />

      {/* 4. Sanskrit Canonical Repository */}
      <CanonicalLibrary />
    </div>
  );
}
