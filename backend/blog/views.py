from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q
from django.utils import timezone
from .models import Category, Tag, Post, Comment, ViewLog, Like
from .serializers import (
    CategorySerializer, TagSerializer,
    PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer,
    CommentSerializer, CommentCreateSerializer
)
from .services import CommentService


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """分类视图集"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """标签视图集"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'


class PostViewSet(viewsets.ModelViewSet):
    """文章视图集"""
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'published_at', 'view_count', 'like_count']
    ordering = ['-pinned', '-published_at', '-created_at']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostDetailSerializer

    def get_queryset(self):
        queryset = Post.objects.select_related('author', 'category').prefetch_related('tags')
        
        # 对于非管理员用户，只显示已发布的文章
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='published', published_at__lte=timezone.now())
        
        # 分类过滤
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # 标签过滤
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        
        # 搜索
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        
        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def view(self, request, slug=None):
        """记录文章阅读量"""
        post = self.get_object()
        ip_address = self.get_client_ip(request)
        
        # 24小时内同一IP只计算一次
        from datetime import timedelta
        yesterday = timezone.now() - timedelta(hours=24)
        
        if not ViewLog.objects.filter(
            post=post,
            ip_address=ip_address,
            viewed_at__gte=yesterday
        ).exists():
            ViewLog.objects.create(
                post=post,
                ip_address=ip_address,
                user=request.user if request.user.is_authenticated else None
            )
            post.view_count += 1
            post.save(update_fields=['view_count'])
        
        return Response({'view_count': post.view_count})

    @action(detail=True, methods=['post'])
    def like(self, request, slug=None):
        """点赞文章"""
        post = self.get_object()
        ip_address = self.get_client_ip(request)
        
        # 检查是否已点赞
        like_filter = {'post': post}
        if request.user.is_authenticated:
            like_filter['user'] = request.user
        else:
            like_filter['ip_address'] = ip_address
        
        like_obj, created = Like.objects.get_or_create(**like_filter)
        
        if created:
            post.like_count += 1
            post.save(update_fields=['like_count'])
            return Response({'liked': True, 'like_count': post.like_count})
        else:
            like_obj.delete()
            post.like_count = max(0, post.like_count - 1)
            post.save(update_fields=['like_count'])
            return Response({'liked': False, 'like_count': post.like_count})

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class CommentViewSet(viewsets.ModelViewSet):
    """评论视图集"""
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.select_related('author', 'post', 'parent').filter(parent=None)
        
        # 文章过滤
        post_slug = self.request.query_params.get('post', None)
        if post_slug:
            queryset = queryset.filter(post__slug=post_slug)
        
        # 对于非管理员用户，只显示已审核的评论
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='approved')
        
        return queryset.order_by('created_at')

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        # 处理评论内容：转义HTML和过滤敏感词
        content = serializer.validated_data.get('content', '')
        processed_content = CommentService.process_comment_content(content)
        serializer.save(
            ip_address=self.get_client_ip(self.request),
            content=processed_content
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
