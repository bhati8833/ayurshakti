import React from 'react';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { getArticleBySlug, getAllArticles } from '@/lib/markdown';
import ArticleCard from '@/components/ArticleCard';
import { ArrowLeft, Clock, Tag, User, ShieldCheck, Share2, Sparkles, BookOpen } from 'lucide-react';

export async function generateStaticParams() {
  const articles = getAllArticles();
  return articles.map((art) => ({
    slug: art.slug,
  }));
}

export default function ArticleDetailPage({ params }: { params: { slug: string } }) {
  const article = getArticleBySlug(params.slug);

  if (!article) {
    notFound();
  }

  const allArticles = getAllArticles();
  const relatedArticles = allArticles
    .filter((a) => a.slug !== article.slug)
    .slice(0, 3);

  return (
    <article className="py-12 bg-ayur-bg min-h-screen">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Back Button Navigation */}
        <div className="mb-8">
          <Link
            href="/articles"
            className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-ayur-forest hover:text-ayur-emerald transition-colors"
          >
            <ArrowLeft className="w-4 h-4 text-ayur-gold" />
            Back to Articles Library
          </Link>
        </div>

        {/* Article Header Card */}
        <header className="glass-panel-gold rounded-3xl p-8 sm:p-12 mb-12 border border-ayur-gold/30 shadow-soft-glow space-y-6">
          <div className="flex flex-wrap items-center gap-3 text-xs font-semibold">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-ayur-forest text-ayur-bg uppercase tracking-wider">
              <Tag className="w-3 h-3 text-ayur-gold" />
              {article.category}
            </span>
            <span className="flex items-center gap-1 text-ayur-sage">
              <Clock className="w-3.5 h-3.5" />
              {article.readingTime}
            </span>
            <span className="inline-flex items-center gap-1 text-ayur-emerald font-bold uppercase tracking-wider">
              <ShieldCheck className="w-4 h-4" /> PubMed Peer-Reviewed Protocol
            </span>
          </div>

          <h1 className="font-serif text-3xl sm:text-5xl font-bold text-ayur-forest leading-tight">
            {article.title}
          </h1>

          <div className="pt-6 border-t border-ayur-border/60 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-ayur-forest text-ayur-gold flex items-center justify-center font-serif font-bold text-sm">
                SB
              </div>
              <div>
                <span className="text-sm font-bold text-ayur-forest block">{article.author}</span>
                <span className="text-xs text-ayur-sage">Ayurvedic Researcher & Author • {article.publishedDate}</span>
              </div>
            </div>

            <div className="flex items-center gap-2 text-xs font-semibold text-ayur-gold uppercase tracking-wider">
              <Sparkles className="w-4 h-4 text-ayur-gold" /> Evidence-Based
            </div>
          </div>
        </header>

        {/* Article Body HTML Content */}
        <div
          className="prose-ayur bg-white rounded-3xl p-8 sm:p-14 border border-ayur-border shadow-sm mb-16 mx-auto"
          dangerouslySetInnerHTML={{ __html: article.htmlContent }}
        />

        {/* Author Bio Box */}
        <div className="glass-panel rounded-3xl p-8 mb-16 border border-ayur-border flex flex-col sm:flex-row items-center gap-6 shadow-sm">
          <div className="w-16 h-16 rounded-full bg-ayur-forest text-ayur-gold flex items-center justify-center font-serif font-bold text-2xl shrink-0">
            SB
          </div>
          <div className="space-y-2 text-center sm:text-left">
            <h3 className="font-serif text-xl font-bold text-ayur-forest">About Suresh Bhati</h3>
            <p className="text-xs text-ayur-sage leading-relaxed">
              Suresh Bhati is an Ayurvedic practitioner and researcher dedicated to decoding classical Sanskrit texts and correlating them with modern pharmacological studies.
            </p>
          </div>
        </div>

        {/* Related Articles Section */}
        {relatedArticles.length > 0 && (
          <div className="space-y-8 pt-8 border-t border-ayur-border">
            <div className="flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-ayur-emerald" />
              <h3 className="font-serif text-2xl font-bold text-ayur-forest">Related Research Protocols</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {relatedArticles.map((art, idx) => (
                <ArticleCard key={art.slug} article={art} index={idx} />
              ))}
            </div>
          </div>
        )}

      </div>
    </article>
  );
}
