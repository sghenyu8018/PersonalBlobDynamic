import { notFound } from 'next/navigation';
import { blogApi } from '@/lib/blog';
import PostContent from '@/components/PostContent';
import CommentSection from '@/components/CommentSection';

export default async function PostPage({
  params,
}: {
  params: { slug: string };
}) {
  try {
    const post = await blogApi.getPost(params.slug);
    const comments = await blogApi.getComments(params.slug);

    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <PostContent post={post} />
        <CommentSection postId={post.id} postSlug={params.slug} initialComments={comments} />
      </div>
    );
  } catch (error) {
    // 构建时如果API不可用，返回404
    // 这在生产构建时是正常的，因为API可能还未启动
    if (process.env.NODE_ENV === 'production') {
      console.warn(`Failed to load post ${params.slug} during build, will fetch at runtime`);
    }
    notFound();
  }
}
