from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import AgentProfile
from .serializers import AgentProfileSerializer

class AgentProfileListCreateAPIView(APIView):
    """负责 agent的列表获取 和 创建"""
    permission_classes = [IsAuthenticated]
    serializer_class = AgentProfileSerializer

    def get(self, request, *args, **kwargs):
        """获取当前用户的所有角色列表"""
        agent_profiles = AgentProfile.objects.filter(user=request.user)
        serializer = self.serializer_class(agent_profiles, many=True)  # 注意 many=True
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """创建新角色"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # 关联当前用户
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgentProfileDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AgentProfileSerializer

    def get_object(self, pk):
        """获取指定 ID 的角色，并确保属于当前用户"""
        try:
            return AgentProfile.objects.get(pk=pk, user=self.request.user)
        except AgentProfile.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        """获取指定角色详情"""
        agent_profile = self.get_object(pk) # pk可以自动映射到主键(id,username都行)上，是一种约定写法
        if not agent_profile:
            return Response({"detail": "角色不存在或无权限访问"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(agent_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        """完全更新角色"""
        return self._update(request, pk, partial=False)

    def patch(self, request, pk, *args, **kwargs):
        """部分更新角色"""
        return self._update(request, pk, partial=True)

    def delete(self, request, pk, *args, **kwargs):
        """删除角色"""
        agent_profile = self.get_object(pk)
        if not agent_profile:
            return Response({"detail": "角色不存在或无权限访问"}, status=status.HTTP_404_NOT_FOUND)
        agent_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _update(self, request, pk, partial=False):
        agent_profile = self.get_object(pk)
        if not agent_profile:
            return Response({"detail": "角色不存在或无权限访问"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(agent_profile, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save() # 如果serializer初始化时否指定instance参数，则调用update，否则调用create
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)