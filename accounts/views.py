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
def access_token_check(request):
    """一个简单的高速接口，帮助测试 access token 是否有效"""
    user = request.user
    return Response({
        'usrename': user.username,
        'token_flat': "access_token有效"
    })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  

    @extend_schema( # 这是API文档生成器，生成接口文档用。不影响实际逻辑
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
    permission_classes = [IsAuthenticated] # 权限控制器
    serializer_class = UserProfileSerializer  # 指定序列化器

    def _get_object(self):
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
    
    # 多种http方法支持（这个几个方法很特殊，是系统默认支持的）
    def get(self, request, *args, **kwargs):
        """读取当前用户资料"""
        profile = self._get_object()
        serializer = self.serializer_class(profile)  # 序列化
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """完全更新用户资料, 所有字段都必须提供"""
        return self._update(request, partial=False)

    def patch(self, request, *args, **kwargs):
        """部分更新用户资料"""
        return self._update(request, partial=True)

    def _update(self, request, partial=False):  
        """更新用户资料的底层接口"""
        profile = self._get_object()  # 获取当前用户的 UserProfile
        # 反序列化：从data--->UserProfile
        serializer = self.serializer_class(profile, data=request.data, partial=partial)
        if serializer.is_valid(): # 调用 is_valid() 会触发所有校验，包括 validate_ 的所有方法
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendVerificationCodeView(APIView):
    @extend_schema(
        description="发送手机验证码",
        request=SendCodeSerializer,
        responses={200: {"type": "object", "properties": {"message": {"type": "string"}}}}
    )
    def post(self, request):
        serializer = SendCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data['phone']
        
        # 调用服务层
        result = send_verification_code_service(phone)
        
        if result['success']:
            return Response({'message': result['message']}, status=status.HTTP_200_OK)
        else:
            return Response({'error': result['message']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


