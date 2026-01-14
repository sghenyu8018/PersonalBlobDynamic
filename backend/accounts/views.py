from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserRegistrationSerializer, LoginSerializer


@api_view(['GET'])
def current_user(request):
    """获取当前登录用户信息"""
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    return Response({'detail': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """用户注册"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """用户登录"""
    serializer = LoginSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_view(request):
    """用户登出"""
    logout(request)
    return Response({'detail': '登出成功'})


@api_view(['GET'])
def check_permission(request):
    """检查用户权限（是否为管理员）"""
    if request.user.is_authenticated:
        return Response({
            'is_authenticated': True,
            'is_staff': request.user.is_staff,
            'is_superuser': request.user.is_superuser,
        })
    return Response({
        'is_authenticated': False,
        'is_staff': False,
        'is_superuser': False,
    })
