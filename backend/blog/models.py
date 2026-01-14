from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    """分类模型"""
    name = models.CharField(max_length=100, unique=True, verbose_name='分类名称')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL标识')
    description = models.TextField(blank=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """标签模型"""
    name = models.CharField(max_length=50, unique=True, verbose_name='标签名称')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL标识')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    """文章模型"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
        ('archived', '已归档'),
    ]

    title = models.CharField(max_length=200, verbose_name='标题')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL标识')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='作者')
    content = models.TextField(verbose_name='内容（Markdown）')
    excerpt = models.TextField(max_length=500, blank=True, verbose_name='摘要')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', verbose_name='分类')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name='标签')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    pinned = models.BooleanField(default=False, verbose_name='置顶')
    is_paid = models.BooleanField(default=False, verbose_name='付费文章')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='价格')
    view_count = models.PositiveIntegerField(default=0, verbose_name='阅读量')
    like_count = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    comment_count = models.PositiveIntegerField(default=0, verbose_name='评论数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-pinned', '-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at', '-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """保存时自动设置发布时间"""
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    """评论模型（支持嵌套回复）"""
    STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '已审核'),
        ('rejected', '已拒绝'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='文章')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments', verbose_name='作者')
    author_name = models.CharField(max_length=100, verbose_name='作者名称')
    author_email = models.EmailField(blank=True, verbose_name='作者邮箱')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='父评论')
    content = models.TextField(verbose_name='评论内容')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='审核状态')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'status']),
            models.Index(fields=['parent']),
        ]

    def __str__(self):
        return f'{self.author_name} 评论: {self.content[:50]}'


class ViewLog(models.Model):
    """阅读量记录（IP去重）"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='view_logs', verbose_name='文章')
    ip_address = models.GenericIPAddressField(verbose_name='IP地址')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='用户')
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name='浏览时间')

    class Meta:
        verbose_name = '浏览记录'
        verbose_name_plural = '浏览记录'
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['post', 'ip_address']),
            models.Index(fields=['viewed_at']),
        ]
        # 移除unique_together，因为同一IP可能在不同时间访问

    def __str__(self):
        return f'{self.ip_address} - {self.post.title}'


class Like(models.Model):
    """点赞记录"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', verbose_name='文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='likes', verbose_name='用户')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')

    class Meta:
        verbose_name = '点赞记录'
        verbose_name_plural = '点赞记录'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post']),
        ]
        # 同一用户/IP对同一文章只能点赞一次
        constraints = [
            models.UniqueConstraint(
                fields=['post', 'user'],
                condition=models.Q(user__isnull=False),
                name='unique_user_like'
            ),
        ]

    def __str__(self):
        user_info = self.user.username if self.user else self.ip_address
        return f'{user_info} 点赞了 {self.post.title}'


class Payment(models.Model):
    """付费记录"""
    STATUS_CHOICES = [
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('failed', '支付失败'),
        ('refunded', '已退款'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='payments', verbose_name='文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', verbose_name='用户')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='支付状态')
    payment_method = models.CharField(max_length=50, blank=True, verbose_name='支付方式')
    transaction_id = models.CharField(max_length=100, blank=True, unique=True, verbose_name='交易ID')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')

    class Meta:
        verbose_name = '支付记录'
        verbose_name_plural = '支付记录'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['transaction_id']),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.post.title} - {self.amount}'


class StaticPage(models.Model):
    """静态页面模型"""
    title = models.CharField(max_length=200, verbose_name='标题')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL标识')
    content = models.TextField(verbose_name='内容（Markdown）')
    is_published = models.BooleanField(default=True, verbose_name='是否发布')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '静态页面'
        verbose_name_plural = '静态页面'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('static-page', kwargs={'slug': self.slug})
