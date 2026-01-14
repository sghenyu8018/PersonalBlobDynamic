"""
权限类
"""
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """只有作者可以编辑，其他用户只能读取"""
    
    def has_object_permission(self, request, view, obj):
        # 读取权限对所有用户开放
        if request.method in permissions.SAFE_METHODS:
            return True
        # 写入权限只给作者
        return obj.author == request.user


class IsPaidOrReadOnly(permissions.BasePermission):
    """付费文章权限检查"""
    
    def has_object_permission(self, request, view, obj):
        # 如果不是付费文章，所有人都可以访问
        if not obj.is_paid:
            return True
        
        # 付费文章：作者和管理员可以访问
        if request.user.is_authenticated:
            if obj.author == request.user or request.user.is_staff:
                return True
            
            # 检查是否已支付
            from .models import Payment
            if Payment.objects.filter(
                post=obj,
                user=request.user,
                status='paid'
            ).exists():
                return True
        
        # 未支付用户只能看到摘要
        return False
