from .models import AgentProfile
from rest_framework import serializers
from datetime import date 


class AgentProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.ImageField(use_url=True, required=False)
    class Meta:
        model = AgentProfile
        fields = [  # 指定哪些字段 参与 序列化/反序列化
            'id',
            'username', # 这个字段的序列化行为，是上面 控制的。我们在这里返回该字段，是因为它是主键，返回给前端，方便后续操作
            'agent_name',  # 使用默认的序列化行为
            'avatar',
            'sex',
            'birthday',
            'age',
            'character_setting',
        ]
        read_only_fields = ['id', 'username', 'updated_at']  # 这些字段 用户不能修改
    
    ## 所有validate_ 开头的方法，会在 实例.is_valid() 调用时，自动扫描调用
    def validate_agent_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("昵称至少2个字符")
        return value
    
    ####只要是有效的生日都行，因为可能是架空的角色
    # def validate_birthday(self, value):
    #     if value > date.today():
    #         raise serializers.ValidationError("生日不能是未来日期")
    #     return value  # 校验通过，必须返回原值或修正后的值
    
    def create(self, validated_data):
        # 确保 user 由视图传入，不在 API 中暴露
        return AgentProfile.objects.create(**validated_data)
    
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

        