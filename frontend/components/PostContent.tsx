'use client';

import { useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import Prism from 'prismjs';
import 'prismjs/themes/prism-tomorrow.css';
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-typescript';
import 'prismjs/components/prism-python';
import 'prismjs/components/prism-bash';
import 'prismjs/components/prism-json';
import type { Post } from '@/lib/types';
import { blogApi } from '@/lib/blog';

interface PostContentProps {
  post: Post;
}

export default function PostContent({ post }: PostContentProps) {
  useEffect(() => {
    // 代码高亮
    Prism.highlightAll();
  }, [post.content]);

  useEffect(() => {
    // 记录阅读量
    blogApi.viewPost(post.slug).catch(console.error);
  }, [post.slug]);

  return (
    <article className="prose prose-lg dark:prose-invert max-w-none">
      <header className="mb-8">
        <h1 className="text-4xl font-bold mb-4">{post.title}</h1>
        <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
          <span>作者: {post.author.username}</span>
          <span>发布于: {new Date(post.published_at || post.created_at).toLocaleString('zh-CN')}</span>
          <span>👁️ {post.view_count}</span>
          <span>❤️ {post.like_count}</span>
          <span>💬 {post.comment_count}</span>
        </div>
        {post.category && (
          <div className="mt-4">
            <span className="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded">
              {post.category.name}
            </span>
          </div>
        )}
      </header>
      <div className="markdown-body">
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          rehypePlugins={[rehypeRaw]}
          components={{
            code({ node, inline, className, children, ...props }: any) {
              const match = /language-(\w+)/.exec(className || '');
              return !inline && match ? (
                <pre className={className}>
                  <code className={className} {...props}>
                    {children}
                  </code>
                </pre>
              ) : (
                <code className={className} {...props}>
                  {children}
                </code>
              );
            },
          }}
        >
          {post.content || ''}
        </ReactMarkdown>
      </div>
    </article>
  );
}
