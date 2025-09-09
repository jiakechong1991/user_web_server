from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from .serializers import UserProfileSerializer
from .models import UserProfile
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


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        # 获取当前用户的 UserProfile，不存在则返回 404（理论上不会，因为信号已自动创建）
        try:
            return self.request.user.profile
        except UserProfile.DoesNotExist:
            # 双重保险：万一信号没触发，这里手动创建
            return UserProfile.objects.create(
                user=self.request.user,
                nickname=f"用户{self.request.user.username[-4:]}",
                sex='m',
                birthday='1990-01-01',
                signature="这家伙很懒，什么也没留下~"
            )
    def get(self, request, *args, **kwargs):
        """读取当前用户资料"""
        profile = self.get_object()
        serializer = self.serializer_class(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """完全更新用户资料"""
        return self._update(request, partial=False)

    def patch(self, request, *args, **kwargs):
        """部分更新用户资料"""
        return self._update(request, partial=True)

    def _update(self, request, partial=False):  
        """更新用户资料的底层接口"""
        profile = self.get_object()  # 获取当前用户的 UserProfile
        # 创建序列化器，并传入当前用户的 UserProfile
        serializer = self.serializer_class(profile, data=request.data, partial=partial)
        if serializer.is_valid(): # 调用 is_valid() 会触发所有校验，包括 validate_ 的所有方法
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





