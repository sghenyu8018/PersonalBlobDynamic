'use client';

import Link from 'next/link';
import type { Post } from '@/lib/types';

interface PostListProps {
  posts: Post[];
}

export default function PostList({ posts }: PostListProps) {
  return (
    <div className="space-y-6">
      {posts.map((post) => (
        <article key={post.id} className="border-b border-gray-200 dark:border-gray-700 pb-6">
          <div className="flex items-center gap-2 mb-2">
            {post.pinned && (
              <span className="px-2 py-1 text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded">
                置顶
              </span>
            )}
            {post.is_paid && (
              <span className="px-2 py-1 text-xs bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200 rounded">
                付费
              </span>
            )}
          </div>
          <h2 className="text-2xl font-bold mb-2">
            <Link
              href={`/posts/${post.slug}`}
              className="hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
            >
              {post.title}
            </Link>
          </h2>
          {post.excerpt && (
            <p className="text-gray-600 dark:text-gray-400 mb-4">{post.excerpt}</p>
          )}
          <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
            <span>{post.author.username}</span>
            <span>{new Date(post.published_at || post.created_at).toLocaleDateString('zh-CN')}</span>
            <span>👁️ {post.view_count}</span>
            <span>❤️ {post.like_count}</span>
            <span>💬 {post.comment_count}</span>
            {post.category && (
              <Link
                href={`/category/${post.category.slug}`}
                className="hover:text-blue-600 dark:hover:text-blue-400"
              >
                {post.category.name}
              </Link>
            )}
          </div>
        </article>
      ))}
    </div>
  );
}
