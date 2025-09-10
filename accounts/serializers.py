# accounts/serializers.py
from rest_framework import serializers
from .models import UserProfile, CustomUser
from datetime import date 
import re


class SendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)

    def validate_phone(self, value):
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError("请输入有效的11位手机号")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    # 可选：暴露 user 的部分字段，比如 username（手机号）
    username = serializers.CharField(source='user.username', read_only=True)
    # 如果你想允许修改昵称，也可以暴露 nickname 字段（它在 UserProfile 里）
    avatar = serializers.ImageField(use_url=True)
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'username',
            'nickname',
            'avatar',
            'sex',
            'birthday',
            'education',
            'signature',
            'hobby',
            'updated_at',
        ]
        read_only_fields = ['id', 'username', 'updated_at']  # 用户不能修改这些
    
    ## 所有validate_ 开头的方法，会在 实例.is_valid() 调用时，自动扫描调用
    def validate_nickname(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("昵称至少2个字符")
        return value
    def validate_birthday(self, value):
        if value > date.today():
            raise serializers.ValidationError("生日不能是未来日期")
        return value  # 校验通过，必须返回原值或修正后的值
    def update(self, instance, validated_data):
        # 支持头像文件上传
        avatar = validated_data.pop('avatar', None)
        if avatar:
            instance.avatar = avatar

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance