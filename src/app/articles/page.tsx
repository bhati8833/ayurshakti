import React from 'react';
import { Metadata } from 'next';
import ArticlesClient from '@/components/ArticlesClient';
import { getAllArticles } from '@/lib/markdown';

export const metadata: Metadata = {
  title: 'Ayurvedic Remedies & Clinical Research Protocols | AyurShakti',
  description: 'Explore authentic Ayurvedic remedies, PubMed-backed botanical research protocols, and classical health guidelines authored by Suresh Bhati.',
  keywords: ['Ayurvedic Remedies', 'Ayurvedic Medicine', 'Ashwagandha', 'Shatavari', 'Giloy', 'Triphala', 'Dog Anxiety Remedies', 'Gut Health Ayurveda'],
  alternates: {
    canonical: '/articles',
  },
};

export default function ArticlesPage() {
  const articles = getAllArticles();
  return <ArticlesClient articles={articles} />;
}
