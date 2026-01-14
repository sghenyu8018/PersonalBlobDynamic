import { blogApi } from '@/lib/blog';
import PostList from '@/components/PostList';

export default async function Home() {
  let posts = [];
  try {
    const data = await blogApi.getPosts();
    posts = data.results || data;
  } catch (error) {
    console.error('Failed to load posts:', error);
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">个人技术博客</h1>
      {posts.length > 0 ? (
        <PostList posts={posts} />
      ) : (
        <p className="text-gray-600 dark:text-gray-400">暂无文章</p>
      )}
    </div>
  );
}
