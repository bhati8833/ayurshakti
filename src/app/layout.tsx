import './globals.css';
import type { Metadata } from 'next';
import { Playfair_Display, Plus_Jakarta_Sans } from 'next/font/google';
import Script from 'next/script';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';

const GA_MEASUREMENT_ID = 'G-1KKZFZB7ML';

const playfair = Playfair_Display({
  subsets: ['latin'],
  variable: '--font-playfair',
  display: 'swap',
});

const jakarta = Plus_Jakarta_Sans({
  subsets: ['latin'],
  variable: '--font-jakarta',
  display: 'swap',
});

export const metadata: Metadata = {
  metadataBase: new URL('https://ayurshakti.shop'),
  title: 'AyurShakti — Authentic Ayurvedic Wisdom & Science-Backed Protocols',
  description: 'Evidence-based Ayurvedic remedies, Sanskrit canonical text analysis, and PubMed peer-reviewed protocols for human and pet health. Authored by Suresh Bhati.',
  keywords: ['Ayurveda', 'Ashwagandha', 'Shatavari', 'Giloy', 'Triphala', 'Dog Health Ayurveda', 'Dosha Quiz', 'Suresh Bhati'],
  authors: [{ name: 'Suresh Bhati', url: 'https://ayurshakti.shop' }],
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: 'AyurShakti — Authentic Ayurvedic Wisdom & Science-Backed Protocols',
    description: 'Evidence-based Ayurvedic remedies and Sanskrit canonical text analysis for human and pet health.',
    url: 'https://ayurshakti.shop',
    siteName: 'AyurShakti',
    locale: 'en_US',
    type: 'website',
  },
};

const jsonLdOrganization = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  '@id': 'https://ayurshakti.shop/#organization',
  name: 'AyurShakti',
  url: 'https://ayurshakti.shop',
  logo: 'https://ayurshakti.shop/public/images/logo.png',
  description: 'Evidence-based Ayurvedic remedies, Sanskrit canonical text analysis, and PubMed peer-reviewed protocols.',
  founder: {
    '@type': 'Person',
    name: 'Suresh Bhati',
    url: 'https://ayurshakti.shop',
  },
  sameAs: [
    'https://twitter.com/ayurshakti_shop',
    'https://bsky.app/profile/ayurshakti.bsky.social',
  ],
};

const jsonLdWebSite = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  '@id': 'https://ayurshakti.shop/#website',
  url: 'https://ayurshakti.shop',
  name: 'AyurShakti',
  description: 'Authentic Ayurvedic Wisdom & Science-Backed Protocols',
  publisher: {
    '@id': 'https://ayurshakti.shop/#organization',
  },
  inLanguage: 'en-US',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${playfair.variable} ${jakarta.variable}`}>
      <head>
        {/* Schema.org Global Organization & WebSite JSON-LD */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdOrganization) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdWebSite) }}
        />

        {/* Google Analytics 4 (GA4) Tag */}
        <Script
          src={`https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`}
          strategy="afterInteractive"
        />
        <Script id="google-analytics" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '${GA_MEASUREMENT_ID}', {
              page_path: window.location.pathname,
            });
          `}
        </Script>
      </head>
      <body className="min-h-screen flex flex-col bg-ayur-bg text-ayur-forest antialiased">
        <Navbar />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
