import api from './api';
import type { Post, Category, Tag, Comment } from './types';

export const blogApi = {
  // 文章相关
  getPosts: async (params?: {
    category?: string;
    tag?: string;
    search?: string;
    page?: number;
  }) => {
    const response = await api.get('/blog/posts/', { params });
    return response.data;
  },

  getPost: async (slug: string) => {
    const response = await api.get(`/blog/posts/${slug}/`);
    return response.data;
  },

  viewPost: async (slug: string) => {
    const response = await api.post(`/blog/posts/${slug}/view/`);
    return response.data;
  },

  likePost: async (slug: string) => {
    const response = await api.post(`/blog/posts/${slug}/like/`);
    return response.data;
  },

  // 分类相关
  getCategories: async () => {
    const response = await api.get('/blog/categories/');
    return response.data;
  },

  getCategory: async (slug: string) => {
    const response = await api.get(`/blog/categories/${slug}/`);
    return response.data;
  },

  // 标签相关
  getTags: async () => {
    const response = await api.get('/blog/tags/');
    return response.data;
  },

  getTag: async (slug: string) => {
    const response = await api.get(`/blog/tags/${slug}/`);
    return response.data;
  },

  // 评论相关
  getComments: async (postSlug: string) => {
    const response = await api.get('/blog/comments/', {
      params: { post: postSlug },
    });
    return response.data;
  },

  createComment: async (data: {
    post: number;
    content: string;
    author_name: string;
    author_email?: string;
    parent?: number;
  }) => {
    const response = await api.post('/blog/comments/', data);
    return response.data;
  },
};
