from django.db import models
from accounts.models import CustomUser
# Create your models here.



class AgentProfile(models.Model):
    # CASCADE: 删除用户，则自动删除用户资料
    # ForeignKey:一对多
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='agent_profile', verbose_name="所属用户")
    agent_name = models.CharField(unique=True, max_length=20, verbose_name="昵称")
    avatar = models.ImageField(upload_to='avatar', verbose_name="头像")
    sex = models.CharField(max_length=1, choices=(('m', '男'), ('f', '女')), verbose_name="性别")
    birthday = models.DateField(verbose_name="生日")
    # 不是所有角色都是现代的哈
    # education = models.CharField(max_length=50, blank=True, verbose_name="学历")
    signature = models.CharField(max_length=500, verbose_name="性格")
    hobby = models.CharField(max_length=500, blank=True, verbose_name="爱好")
    
    updated_at = models.DateTimeField(auto_now=True)  # 更新时间

    def __str__(self):
        return f"{self.user.username}的role: {self.agent_name} 的资料"

    class Meta:
        verbose_name = "角色资料"
        verbose_name_plural = "角色资料"
