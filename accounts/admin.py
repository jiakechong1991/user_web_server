from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    # 显示在用户列表中的字段
    list_display = ('username', 'nickname', 'email', 'is_staff', 'is_active', 'date_joined')
    
    # 可以点击进入编辑的字段
    list_display_links = ('username', 'nickname')
    
    # 右侧过滤栏
    list_filter = ('is_staff', 'is_active', 'date_joined')
    
    # 搜索框，支持按这些字段搜索
    search_fields = ('username', 'nickname', 'email')
    
    # 编辑页面的字段分组
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('nickname', 'email')}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要日期', {'fields': ('last_login', 'date_joined')}),
    )
    
    # 默认排序
    ordering = ('-date_joined',)


# 注册模型
admin.site.register(CustomUser, CustomUserAdmin)