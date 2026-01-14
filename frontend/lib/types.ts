export interface User {
  id: number;
  username: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  is_staff: boolean;
  date_joined: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
  post_count: number;
  created_at: string;
}

export interface Tag {
  id: number;
  name: string;
  slug: string;
  post_count: number;
  created_at: string;
}

export interface Author {
  id: number;
  username: string;
  first_name?: string;
  last_name?: string;
}

export interface Post {
  id: number;
  title: string;
  slug: string;
  author: Author;
  content?: string;
  excerpt?: string;
  category?: Category;
  tags: Tag[];
  status: 'draft' | 'published' | 'archived';
  pinned: boolean;
  is_paid: boolean;
  price?: number;
  view_count: number;
  like_count: number;
  comment_count: number;
  created_at: string;
  updated_at: string;
  published_at?: string;
}

export interface Comment {
  id: number;
  author?: Author;
  author_name: string;
  author_email?: string;
  content: string;
  status: 'pending' | 'approved' | 'rejected';
  parent?: number;
  replies?: Comment[];
  created_at: string;
  updated_at: string;
}
