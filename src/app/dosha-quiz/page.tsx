import React from 'react';
import { Metadata } from 'next';
import DoshaQuizWidget from '@/components/DoshaQuizWidget';
import { HeartPulse } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Interactive Ayurvedic Dosha Quiz & Prakriti Test | AyurShakti',
  description: 'Discover your unique mind-body Ayurvedic constitution (Vata, Pitta, Kapha) with our classical interactive self-assessment quiz.',
  alternates: {
    canonical: '/dosha-quiz',
  },
};

export default function DoshaQuizPage() {
  return (
    <div className="py-16 bg-ayur-bg min-h-screen">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center space-y-4 mb-12">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white text-ayur-forest border border-ayur-gold/40 text-xs font-semibold uppercase tracking-widest shadow-sm">
            <HeartPulse className="w-4 h-4 text-ayur-emerald" />
            Authentic Ayurvedic Assessment
          </span>
          <h1 className="font-serif text-4xl sm:text-6xl font-bold text-ayur-forest">
            Discover Your Tridosha Balance
          </h1>
          <p className="text-ayur-sage text-lg max-w-2xl mx-auto">
            In Ayurveda, your unique mind-body constitution (Prakriti) determines which dietary protocols and herbal adaptogens will restore maximum energy and vitality.
          </p>
        </div>

        <DoshaQuizWidget />
      </div>
    </div>
  );
}
