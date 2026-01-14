'use client';

import { useState } from 'react';

interface CommentFormProps {
  onSubmit: (data: {
    content: string;
    author_name: string;
    author_email?: string;
    parent?: number;
  }) => void;
  loading?: boolean;
  parentId?: number;
  onCancel?: () => void;
}

export default function CommentForm({ onSubmit, loading = false, parentId, onCancel }: CommentFormProps) {
  const [content, setContent] = useState('');
  const [authorName, setAuthorName] = useState('');
  const [authorEmail, setAuthorEmail] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim() || !authorName.trim()) {
      return;
    }
    onSubmit({
      content: content.trim(),
      author_name: authorName.trim(),
      author_email: authorEmail.trim() || undefined,
      parent: parentId,
    });
    setContent('');
    setAuthorName('');
    setAuthorEmail('');
    if (onCancel) onCancel();
  };

  return (
    <form onSubmit={handleSubmit} className="mb-8">
      <div className="space-y-4">
        <div>
          <label htmlFor="author_name" className="block text-sm font-medium mb-2">
            姓名 *
          </label>
          <input
            type="text"
            id="author_name"
            value={authorName}
            onChange={(e) => setAuthorName(e.target.value)}
            required
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800"
          />
        </div>
        <div>
          <label htmlFor="author_email" className="block text-sm font-medium mb-2">
            邮箱（可选）
          </label>
          <input
            type="email"
            id="author_email"
            value={authorEmail}
            onChange={(e) => setAuthorEmail(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800"
          />
        </div>
        <div>
          <label htmlFor="content" className="block text-sm font-medium mb-2">
            评论内容 *
          </label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
            rows={6}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800"
          />
        </div>
        <div className="flex gap-4">
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? '提交中...' : '提交评论'}
          </button>
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              className="px-6 py-2 border border-gray-300 dark:border-gray-600 rounded-lg"
            >
              取消
            </button>
          )}
        </div>
      </div>
    </form>
  );
}
