# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile


###信号函数
# [作用]：这是 使用 django的信号机制， 创建用户时，自动创建用户资料
# 装饰器：监听CustomUser模型的post_save信号
# post_save: 模型实例.save() 成功执行之后触发的信号
# sender: 只监听 CustomUser 模型的保存事件（避免其他模型触发
@receiver(post_save, sender=CustomUser)  
def create_user_profile(sender, instance, created, **kwargs):  # 你自定义的回调函数，名字可自定义
    """
    param1:触发信号的模型类（这里是CustomUser）
    param2：被保存的具体模型实例（如刚创建的用户对象）
    param3:布尔值，True表示这是“新建”而非“更新”

    """
    if created: # 只有新建用户时才创建资料，避免重复创建
        UserProfile.objects.create(  # 创建并关联资料对象
            user=instance,
            nickname=f"用户{instance.username}",
            sex='m',
            birthday='1990-01-01',
            signature="这家伙很懒，什么也没留下~",
            # avatar 可以留空，或设置默认头像路径
        )
