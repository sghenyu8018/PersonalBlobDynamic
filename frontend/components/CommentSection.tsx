'use client';

import { useState, useEffect } from 'react';
import { blogApi } from '@/lib/blog';
import type { Comment } from '@/lib/types';
import CommentList from './CommentList';
import CommentForm from './CommentForm';

interface CommentSectionProps {
  postId: number;
  postSlug: string;
  initialComments: Comment[];
}

export default function CommentSection({ postId, postSlug, initialComments }: CommentSectionProps) {
  const [comments, setComments] = useState<Comment[]>(initialComments);
  const [loading, setLoading] = useState(false);

  const handleCommentSubmit = async (data: {
    content: string;
    author_name: string;
    author_email?: string;
    parent?: number;
  }) => {
    setLoading(true);
    try {
      await blogApi.createComment({
        ...data,
        post: postId,
      });
      // 刷新评论列表
      const newComments = await blogApi.getComments(postSlug);
      setComments(newComments);
    } catch (error) {
      console.error('提交评论失败:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-12">
      <h2 className="text-2xl font-bold mb-6">评论</h2>
      <CommentForm onSubmit={handleCommentSubmit} loading={loading} />
      <CommentList comments={comments} />
    </div>
  );
}
