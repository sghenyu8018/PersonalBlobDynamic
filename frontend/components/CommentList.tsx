'use client';

import type { Comment } from '@/lib/types';

interface CommentListProps {
  comments: Comment[];
  level?: number;
}

export default function CommentList({ comments, level = 0 }: CommentListProps) {
  if (!comments || comments.length === 0) {
    return <p className="text-gray-500 dark:text-gray-400">暂无评论</p>;
  }

  return (
    <div className={`space-y-4 ${level > 0 ? 'ml-8 border-l-2 border-gray-200 dark:border-gray-700 pl-4' : ''}`}>
      {comments.map((comment) => (
        <div key={comment.id} className="border-b border-gray-100 dark:border-gray-800 pb-4">
          <div className="flex items-start gap-4">
            <div className="flex-shrink-0 w-10 h-10 bg-gray-200 dark:bg-gray-700 rounded-full flex items-center justify-center">
              {comment.author?.username?.[0] || comment.author_name[0] || '?'}
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <span className="font-semibold">
                  {comment.author?.username || comment.author_name}
                </span>
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  {new Date(comment.created_at).toLocaleString('zh-CN')}
                </span>
              </div>
              <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                {comment.content}
              </p>
              {comment.replies && comment.replies.length > 0 && (
                <div className="mt-4">
                  <CommentList comments={comment.replies} level={level + 1} />
                </div>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
