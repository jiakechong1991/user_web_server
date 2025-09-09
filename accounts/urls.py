from django.urls import path
from . import views

urlpatterns = [
    # url路径(字符串)    视图函数，             别名
    # 这个别名可以直接在 模板中引用，
    # 也可以在代码中直接 url = reverse('access_token_check')  # 返回 '/access_token_check/'
    path('profile/', views.user_profile, name='user_profile'),
    path('access_token_check/', views.access_token_check, name='access_token_check'),
]