from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request):
    """API根端点"""
    return Response({
        'message': '个人技术博客 API',
        'version': '1.0',
    })
