import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getArticleBySlug, getAllArticles } from '@/lib/markdown';
import ArticleCard from '@/components/ArticleCard';
import { ArrowLeft, Clock, Tag, User, ShieldCheck, Share2, Sparkles, BookOpen } from 'lucide-react';

interface ArticlePageProps {
  params: {
    slug: string;
  };
}

export async function generateStaticParams() {
  const articles = getAllArticles();
  return articles.map((art) => ({
    slug: art.slug,
  }));
}

export async function generateMetadata({ params }: ArticlePageProps): Promise<Metadata> {
  const article = getArticleBySlug(params.slug);
  if (!article) return { title: 'Article Not Found | AyurShakti' };

  return {
    title: `${article.title} | AyurShakti`,
    description: article.description || article.title,
    alternates: {
      canonical: `/articles/${params.slug}`,
    },
    openGraph: {
      title: article.title,
      description: article.description || article.title,
      url: `https://ayurshakti.shop/articles/${params.slug}`,
      type: 'article',
      publishedTime: article.publishedDate,
      authors: [article.author || 'Suresh Bhati'],
    },
  };
}

export default function ArticleDetailPage({ params }: ArticlePageProps) {
  const article = getArticleBySlug(params.slug);

  if (!article) {
    notFound();
  }

  const allArticles = getAllArticles();
  const relatedArticles = allArticles
    .filter((a) => a.slug !== article.slug)
    .slice(0, 3);

  const jsonLdArticle = {
    '@context': 'https://schema.org',
    '@type': 'MedicalWebPage',
    '@id': `https://ayurshakti.shop/articles/${article.slug}#webpage`,
    url: `https://ayurshakti.shop/articles/${article.slug}`,
    name: article.title,
    headline: article.title,
    description: article.description || article.title,
    inLanguage: 'en-US',
    author: {
      '@type': 'Person',
      name: article.author || 'Suresh Bhati',
      jobTitle: 'Ayurvedic Researcher & Author',
      url: 'https://ayurshakti.shop',
    },
    publisher: {
      '@type': 'Organization',
      name: 'AyurShakti',
      url: 'https://ayurshakti.shop',
      logo: 'https://ayurshakti.shop/public/images/logo.png',
    },
    datePublished: article.publishedDate,
    dateModified: article.publishedDate,
    about: {
      '@type': 'MedicalTopic',
      name: article.category || 'Ayurveda',
    },
  };

  return (
    <article className="py-12 bg-ayur-bg min-h-screen">
      {/* Schema.org Article / MedicalWebPage JSON-LD */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdArticle) }}
      />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        
        {/* Back Navigation */}
        <div className="flex items-center justify-between">
          <Link
            href="/articles"
            className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-ayur-forest hover:text-ayur-emerald transition-colors"
          >
            <ArrowLeft className="w-4 h-4 text-ayur-gold" />
            Back to Articles
          </Link>

          <span className="px-3.5 py-1 rounded-full bg-ayur-sand text-ayur-forest text-xs font-bold uppercase tracking-wider">
            {article.category}
          </span>
        </div>

        {/* Header Block */}
        <div className="space-y-6">
          <h1 className="font-serif text-3xl sm:text-5xl lg:text-6xl font-bold text-ayur-forest leading-tight">
            {article.title}
          </h1>

          {/* Meta Info Strip */}
          <div className="flex flex-wrap items-center gap-4 sm:gap-6 text-xs text-ayur-sage border-y border-ayur-border/60 py-4">
            <span className="flex items-center gap-1.5 font-medium text-ayur-forest">
              <User className="w-4 h-4 text-ayur-gold" />
              Authored by {article.author}
            </span>
            <span className="flex items-center gap-1.5">
              <Clock className="w-4 h-4 text-ayur-emerald" />
              {article.readingTime}
            </span>
            <span className="flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-ayur-gold" />
              Peer-Reviewed PubMed Protocol
            </span>
          </div>
        </div>

        {/* Executive Summary Box */}
        {article.description && (
          <div className="glass-panel-gold rounded-2xl p-6 sm:p-8 border border-ayur-gold/40 shadow-xs space-y-2">
            <span className="text-xs font-bold uppercase tracking-widest text-ayur-gold flex items-center gap-1.5">
              <Sparkles className="w-4 h-4" /> Clinical Executive Summary
            </span>
            <p className="text-ayur-forest text-base sm:text-lg font-serif italic leading-relaxed">
              "{article.description}"
            </p>
          </div>
        )}

        {/* Render Main Article HTML Content */}
        <div
          className="prose-ayur bg-white rounded-3xl p-8 sm:p-12 border border-ayur-border shadow-sm"
          dangerouslySetInnerHTML={{ __html: article.htmlContent }}
        />

        {/* Article Footnotes & Labels */}
        <div className="pt-6 border-t border-ayur-border flex flex-wrap items-center justify-between gap-4">
          <div className="flex flex-wrap items-center gap-2">
            <Tag className="w-4 h-4 text-ayur-sage" />
            {article.labels.map((lbl) => (
              <span
                key={lbl}
                className="px-3 py-1 rounded-full bg-ayur-sand text-ayur-forest text-xs font-semibold uppercase tracking-wider"
              >
                {lbl}
              </span>
            ))}
          </div>
        </div>

        {/* Related Articles Section */}
        {relatedArticles.length > 0 && (
          <div className="pt-12 space-y-6 border-t border-ayur-border">
            <div className="flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-ayur-gold" />
              <h2 className="font-serif text-2xl font-bold text-ayur-forest">
                Related Research Protocols
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {relatedArticles.map((relArt, idx) => (
                <ArticleCard key={relArt.slug} article={relArt} index={idx} />
              ))}
            </div>
          </div>
        )}

      </div>
    </article>
  );
}
