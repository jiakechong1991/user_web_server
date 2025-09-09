from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
# Create your views here.



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    return Response({
        'usrename': user.username,
        'date_joined': user.date_joined
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def access_token_check(request):
    """一个简单的高速接口，帮助测试 access token 是否有效"""
    user = request.user
    return Response({
        'usrename': user.username,
        'token_flat': "access_token有效"
    })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="将 refresh token 加入黑名单，实现真正登出"
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # 将 refresh token 和关联的 access token 加入黑名单
            return Response({"detail": "已成功登出，token 已失效。"})
        except Exception as e:
            return Response({"detail": "登出失败"}, status=400)