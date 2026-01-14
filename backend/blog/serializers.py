from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Tag, Post, Comment


class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器"""
    post_count = serializers.IntegerField(source='posts.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'post_count', 'created_at']
        read_only_fields = ['id', 'created_at']


class TagSerializer(serializers.ModelSerializer):
    """标签序列化器"""
    post_count = serializers.IntegerField(source='posts.count', read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'post_count', 'created_at']
        read_only_fields = ['id', 'created_at']


class AuthorSerializer(serializers.ModelSerializer):
    """作者序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class PostListSerializer(serializers.ModelSerializer):
    """文章列表序列化器"""
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    excerpt = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'excerpt', 'category', 'tags',
            'status', 'pinned', 'is_paid', 'view_count', 'like_count',
            'comment_count', 'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['id', 'view_count', 'like_count', 'comment_count', 'created_at', 'updated_at']

    def get_excerpt(self, obj):
        if obj.excerpt:
            return obj.excerpt
        # 如果没有摘要，从内容中提取前200字符
        return obj.content[:200] + '...' if len(obj.content) > 200 else obj.content


class PostDetailSerializer(serializers.ModelSerializer):
    """文章详情序列化器"""
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'content', 'excerpt', 'category', 'tags',
            'status', 'pinned', 'is_paid', 'price', 'view_count', 'like_count',
            'comment_count', 'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = [
            'id', 'author', 'view_count', 'like_count', 'comment_count',
            'created_at', 'updated_at', 'published_at'
        ]


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """文章创建/更新序列化器"""
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False, allow_null=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)

    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'content', 'excerpt', 'category', 'tags',
            'status', 'pinned', 'is_paid', 'price', 'published_at'
        ]

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """评论序列化器"""
    author = AuthorSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'author', 'author_name', 'author_email', 'content',
            'status', 'parent', 'replies', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'status', 'created_at', 'updated_at']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class CommentCreateSerializer(serializers.ModelSerializer):
    """评论创建序列化器"""
    class Meta:
        model = Comment
        fields = ['post', 'content', 'author_name', 'author_email', 'parent']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['ip_address'] = self.get_client_ip(request)
        if request.user.is_authenticated:
            validated_data['author'] = request.user
            validated_data['author_name'] = request.user.get_full_name() or request.user.username
            validated_data['author_email'] = request.user.email
        return super().create(validated_data)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
