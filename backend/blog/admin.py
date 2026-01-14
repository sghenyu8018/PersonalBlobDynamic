from django.contrib import admin
from .models import Category, Tag, Post, Comment, ViewLog, Like, Payment, StaticPage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'pinned', 'is_paid', 'view_count', 'published_at']
    list_filter = ['status', 'category', 'tags', 'pinned', 'is_paid', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'created_at'
    readonly_fields = ['view_count', 'like_count', 'comment_count', 'created_at', 'updated_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'post', 'status', 'parent', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['author_name', 'content', 'post__title']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['approve_comments', 'reject_comments']

    def approve_comments(self, request, queryset):
        queryset.update(status='approved')
    approve_comments.short_description = '审核通过选中的评论'

    def reject_comments(self, request, queryset):
        queryset.update(status='rejected')
    reject_comments.short_description = '拒绝选中的评论'


@admin.register(ViewLog)
class ViewLogAdmin(admin.ModelAdmin):
    list_display = ['post', 'ip_address', 'user', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['post__title', 'ip_address']
    readonly_fields = ['viewed_at']
    date_hierarchy = 'viewed_at'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'ip_address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__title', 'user__username', 'ip_address']
    readonly_fields = ['created_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'amount', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['user__username', 'post__title', 'transaction_id']
    readonly_fields = ['created_at', 'paid_at']
    date_hierarchy = 'created_at'


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_published', 'updated_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
