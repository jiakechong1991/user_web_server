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
    def create_user(self, username, password, nickname=None, email=None):
        if not username:
            raise ValueError('必须提供手机号')

        email = self.normalize_email(email) if email else None

        user = self.model(
            username=username,
            nickname=nickname,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, nickname=None, email=None):
        user = self.create_user(
            username=username,
            password=password,
            nickname=nickname,
            email=email or f'{username}@admin.local'
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # ✅ 唯一字段：username，既是登录账号，也是手机号
    username = models.CharField(
        max_length=11,
        unique=True,
        verbose_name="手机号",
        help_text="请输入11位中国大陆手机号",
        validators=[validate_mobile]  # 强制格式校验
    )

    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name="昵称")
    email = models.EmailField(blank=True, null=True, verbose_name="邮箱")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'  # 使用手机号登录
    REQUIRED_FIELDS = ['nickname']  # 创建 superuser 时需要的字段

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"