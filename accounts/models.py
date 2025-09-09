# accounts/models.py
import re
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


def validate_mobile(value):
    """校验手机号格式"""
    if not re.match(r'^1[3-9]\d{9}$', value):
        raise ValidationError('请输入有效的11位中国大陆手机号')


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, email=None):
        if not username:
            raise ValueError('必须提供手机号')

        email = self.normalize_email(email) if email else None

        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email=None):
        user = self.create_user(
            username=username,
            password=password,
            email=email or f'{username}@admin.local'
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# django只提供了“骨架”用户模型(AbstractBaseUser)， 但是不包含创建用户方法， 
# 创建用户模型时，需要继承 AbstractBaseUser， 也必须继承后user的Manager类，辅助创建用户
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # ✅ 唯一字段：username，既是登录账号，也是手机号
    username = models.CharField(
        max_length=11,
        unique=True,
        verbose_name="手机号",
        help_text="请输入11位中国大陆手机号",
        validators=[validate_mobile]  # 强制格式校验
    )
    email = models.EmailField(blank=True, null=True, verbose_name="邮箱")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()  # 配置管理类

    USERNAME_FIELD = 'username'  # 使用手机号登录
    REQUIRED_FIELDS = ['nickname']  # 创建 superuser 时需要的字段

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"