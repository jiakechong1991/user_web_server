# accounts/serializers.py
from rest_framework import serializers
from .models import UserProfile, CustomUser
from datetime import date 
import re
from utils.verification_code import verify_code
"""
#如果是继承serializers.ModelSerializer,就要定义 Meta类
    ModelSerializer 需要知道“绑定哪个model模型”，所以靠 Meta.model
#如果是继承serializers.Serializer(普通序列化器),就不需要Meta类，
    因为这是 纯用于输入验证或自定义逻辑的序列化器，不绑定任何模型
# serializers.CharField 是一种字段级验证类，方便多处复用
"""

class PhoneNumberField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs.setdefault('max_length', 11)
        kwargs.setdefault('min_length', 11)
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        # 先走父类基础验证（长度等）
        value = super().to_internal_value(data)
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError("请输入有效的11位手机号")
        return value
    

class SendCodeSerializer(serializers.Serializer):
    phone = PhoneNumberField()


class UserProfileSerializer(serializers.ModelSerializer):
    # 重新定义这两个字段的序列化行为
    # UserProfile中没有这个字段，所以我们明确告诉DRF框架，要在序列化器中 重新定义
    #     source='user.username' 的作用 —— 跨模型取值
    #     read_only=True 的作用 —— 只读字段，防止前端通过这个字段修改用户的手机号
    username = serializers.CharField(source='user.username', read_only=True)
    # UserProfile中有这个字段，但是 序列化器 自动生成的 ImageField 行为不符合你的需求， 我们告诉DRF框架，
    #    需要这个字段序列化时，是完整的 图片url
    avatar = serializers.ImageField(use_url=True)
    class Meta:
        model = UserProfile
        fields = [  # 指定哪些字段 参与 序列化/反序列化
            'id',
            'username', # 这个字段的序列化行为，是上面 控制的。我们在这里返回该字段，是因为它是逐渐，返回给前端，方便后续操作
            'nickname',  # 使用默认的序列化行为
            'avatar',
            'sex',
            'birthday',
            'education',
            'signature',
            'hobby',
            'updated_at',
        ]
        read_only_fields = ['id', 'username', 'updated_at']  # 这些字段 用户不能修改
    
    ## 所有validate_ 开头的方法，会在 实例.is_valid() 调用时，自动扫描调用
    def validate_nickname(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("昵称至少2个字符")
        return value
    def validate_birthday(self, value):
        if value > date.today():
            raise serializers.ValidationError("生日不能是未来日期")
        return value  # 校验通过，必须返回原值或修正后的值
    def update(self, instance, validated_data):  # 自定义了更新方法
        """
        param instance: 要更新的对象
        param validated_data: 校验后的数据
        """
        # 支持头像文件上传
        avatar = validated_data.pop('avatar', None)
        if avatar:
            instance.avatar = avatar

        for attr, value in validated_data.items():
            # 遍历剩余的字段，并设置到 instance 中
            setattr(instance, attr, value) 

        instance.save()  # 保存到数据库
        return instance
    
"""
关于几种验证方法的执行顺序：
1. 先执行 max_length，min_length 字段携带的基本验证器
2. 再按照 [定义顺序]，执行 字段级验证器(validate_ + 字段名)
3. 最后执行 validate() [对象级验证器]
"""

class RegisterSerializer(serializers.Serializer):
    # 重新定义这几个字段的序列化行为（附带基本的验证）
    phone = PhoneNumberField() # phone的默认验证
    code = serializers.CharField(min_length=6, max_length=6)
    password = serializers.CharField(min_length=6)
    password_confirm = serializers.CharField(min_length=6)

    # 字段级验证 就是 validate_ + 字段名
    def validate_phone(self, value): 
        # 检查是否已注册
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("该手机号已被注册")
        
        return value

    def validate_code(self, value): 
        phone = self.initial_data.get('phone')

        if not verify_code(phone, value):  # 你已实现的验证码校验
            raise serializers.ValidationError("验证码错误或已过期")
        return value

    # 对象级验证：data就是原始数据
    # 所有 validate_字段(方法) 都在 validate() 之前执行
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("两次密码不一致")
        return data