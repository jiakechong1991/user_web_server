
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts import views as account_views
from agent import views as agent_views

urlpatterns = [
    path('admin/', admin.site.urls),  # 后台管理
    path('accounts/', include('allauth.urls')),  # web端登录注册
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 登录获取 token
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),       # 刷新 token
    path('api/auth/logout/', account_views.LogoutView.as_view(), name='logout'),  # 👈 自定义登出
    # # 其他如 logout 等仍可用 dj-rest-auth
    path('api-auth/', include('rest_framework.urls')), # DRF 自带的登录页面（用于调试）
    path('api/auth/', include('dj_rest_auth.urls')), # 真正的 API 登录接口
    # path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    # path需要两个入参：route字符串和view函数
    path('api/accounts/', include('accounts.urls')),
    path('api/agents/', include('agent.urls')),
    path('app_learn/', include('app_learn.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
