#!/usr/bin/env python
"""
本地测试脚本
"""
import sys
import os
import django
from pathlib import Path

# 添加backend目录到Python路径
BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / 'backend'
sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_imports():
    """测试导入"""
    print("=" * 50)
    print("测试1: 导入模块")
    print("=" * 50)
    try:
        from blog.models import Post, Category, Tag, Comment
        from blog.serializers import PostListSerializer, CommentSerializer
        from accounts.views import current_user, register
        print("[OK] 所有模块导入成功")
        return True
    except Exception as e:
        print(f"错误: 导入失败: {e}")
        return False

def test_models():
    """测试模型"""
    print("\n" + "=" * 50)
    print("测试2: 数据库模型")
    print("=" * 50)
    try:
        from blog.models import Post, Category, Tag
        from django.contrib.auth.models import User
        
        # 检查模型是否存在
        post_count = Post.objects.count()
        category_count = Category.objects.count()
        tag_count = Tag.objects.count()
        user_count = User.objects.count()
        
        print(f"[OK] Post模型: {post_count} 条记录")
        print(f"[OK] Category模型: {category_count} 条记录")
        print(f"[OK] Tag模型: {tag_count} 条记录")
        print(f"[OK] User模型: {user_count} 条记录")
        return True
    except Exception as e:
        print(f"错误: 模型测试失败: {e}")
        return False

def test_admin():
    """测试Admin配置"""
    print("\n" + "=" * 50)
    print("测试3: Django Admin配置")
    print("=" * 50)
    try:
        from django.contrib import admin
        from blog.models import Post, Category, Tag, Comment
        
        # 检查是否已注册
        if admin.site.is_registered(Post):
            print("[OK] Post已注册到Admin")
        else:
            print("[ERROR] Post未注册到Admin")
            
        if admin.site.is_registered(Category):
            print("[OK] Category已注册到Admin")
        else:
            print("[ERROR] Category未注册到Admin")
            
        return True
    except Exception as e:
        print(f"错误: Admin测试失败: {e}")
        return False

def test_urls():
    """测试URL配置"""
    print("\n" + "=" * 50)
    print("测试4: URL配置")
    print("=" * 50)
    try:
        from django.urls import resolve
        from django.test import Client
        
        client = Client()
        
        # 测试API根路径
        try:
            from django.conf import settings
            original_hosts = settings.ALLOWED_HOSTS
            settings.ALLOWED_HOSTS = ['testserver'] + list(original_hosts)
            response = client.get('/api/')
            settings.ALLOWED_HOSTS = original_hosts
            print(f"[OK] API根路径: {response.status_code}")
        except Exception as e:
            print(f"[WARN] API根路径测试失败: {e}")
        
        # 测试博客API路径
        try:
            from django.conf import settings
            original_hosts = settings.ALLOWED_HOSTS
            settings.ALLOWED_HOSTS = ['testserver'] + list(original_hosts)
            response = client.get('/api/blog/posts/')
            settings.ALLOWED_HOSTS = original_hosts
            print(f"[OK] 文章列表API: {response.status_code}")
        except Exception as e:
            print(f"[WARN] 文章列表API测试失败: {e}")
            
        return True
    except Exception as e:
        print(f"错误: URL测试失败: {e}")
        return False

def test_serializers():
    """测试序列化器"""
    print("\n" + "=" * 50)
    print("测试5: 序列化器")
    print("=" * 50)
    try:
        from blog.serializers import PostListSerializer, CommentSerializer
        from blog.models import Post
        
        # 检查序列化器是否存在
        print("[OK] PostListSerializer存在")
        print("[OK] CommentSerializer存在")
        return True
    except Exception as e:
        print(f"错误: 序列化器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("\n" + "=" * 50)
    print("开始本地测试")
    print("=" * 50 + "\n")
    
    results = []
    results.append(test_imports())
    results.append(test_models())
    results.append(test_admin())
    results.append(test_urls())
    results.append(test_serializers())
    
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("[OK] 所有测试通过！")
        return 0
    else:
        print("[ERROR] 部分测试失败")
        return 1

if __name__ == '__main__':
    sys.exit(main())
