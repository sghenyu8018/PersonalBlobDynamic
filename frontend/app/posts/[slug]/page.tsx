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
        <CommentSection postSlug={params.slug} initialComments={comments} />
      </div>
    );
  } catch (error) {
    notFound();
  }
}
