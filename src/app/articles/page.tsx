import React from 'react';
import ArticlesClient from '@/components/ArticlesClient';
import { getAllArticles } from '@/lib/markdown';

export default function ArticlesPage() {
  const articles = getAllArticles();
  return <ArticlesClient articles={articles} />;
}
