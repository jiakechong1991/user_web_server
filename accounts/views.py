from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .serializers import UserProfileSerializer
from .serializers import SendCodeSerializer
from .serializers import RegisterSerializer
from .services import  send_verification_code_service
from .models import UserProfile, CustomUser
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
            serializer.save()  # 调用序列化器的 update()方法
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator([
    # 限制手机号：1分钟1次
    ratelimit(key='post:phone', rate='1/m', method='POST', block=True),
    # 限制IP：1小时5次
    ratelimit(key='ip', rate='5/h', method='POST', block=True),
    # 限制全局：1分钟10次（防DDoS）
    ratelimit(key='header:x-real-ip', rate='10/m', method='POST', block=True),
], name='dispatch')
class SendVerificationCodeView(APIView):
    """请求server发送验证码"""
    # 因为我们在settings.py中配置了所有API都要认证，这里我们对该接口取消认证
    permission_classes = [AllowAny]  # 允许任何人访问
    authentication_classes = []      # 不进行任何身份认证（可选，更彻底）
    serializer_class = SendCodeSerializer  # 指定序列化器
    
    @extend_schema(description="发送手机验证码")
    def post(self, request, *args, **kwargs):
        ###这里提出一个自问自答：
        ###为什么上面UserProfileAPIView 这样写：
        # serializer = self.serializer_class(profile, data=request.data, partial=partial)
        # 这是因为：self.serializer_class 有几个入参： instance,data,partial,context,many
        # 源码定义：(instance=None, data=empty, **kwargs)
        # 场景：如果你要创建/更新对象 那就传instance
        # 场景：如果你只是验证数据，那就不用传instance
        
        # 先用序列化器验证数据
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 然后执行view逻辑
        phone = serializer.validated_data['phone']
        # 调用验证码发送服务
        result = send_verification_code_service(phone)
        
        if result['success']:
            return Response({'message': result['message']}, status=status.HTTP_200_OK)
        else:
            return Response({'error': result['message']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegisterView(APIView):
    """注册视图 """
    permission_classes = [AllowAny]  # 允许任何人访问
    authentication_classes = []      # 不进行任何身份认证（可选，更彻底）
    serializer_class = RegisterSerializer  # 指定序列化器
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = CustomUser.objects.create_user(
            username=serializer.validated_data['username'],
            phone=serializer.validated_data['phone'],
            password=serializer.validated_data['password']
        )

        return Response({"message": "注册成功"}, status=201)
