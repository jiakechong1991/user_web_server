
from datetime import datetime
from django.utils import timezone
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
    birthday = models.DateField(blank=True, null=True, verbose_name="生日")  # 只需要生日，年份统一是1970年，因为不用年份
    age = models.IntegerField(blank=True, null=True, verbose_name="年龄")
    # 不是所有角色都是现代的哈
    # education = models.CharField(max_length=50, blank=True, verbose_name="学历")
    # 最后我们利用LLM来从人设 中 进行结构化
    character_setting = models.CharField(blank=True, null=True, max_length=500, verbose_name="人设")
    
    updated_at = models.DateTimeField(auto_now=True)  # 更新时间
    is_deleted = models.BooleanField(default=False, verbose_name="是否软删除")

    def __str__(self):
        return f"{self.user.username}的role: {self.agent_name} 的资料"

    class Meta:
        verbose_name = "角色资料"
        verbose_name_plural = "角色资料"
        
    def to_dict(self):
        return {
            "user_name": self.user.username,
            "agent_id": self.id, 
            "name": self.agent_name,
            "sex": self.get_sex_display(),
            "age": self.age,  # 可能存在架空角色，所以直接让用户输入
            "birthday": self.birthday.strftime("%m月%d日") if self.birthday else "",
            "character_setting": self.character_setting,
            # 将时间按照时区转换为当前时区
            "create_time": timezone.localtime(self.updated_at).strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": timezone.localtime(self.updated_at).strftime("%Y-%m-%d %H:%M:%S"),
        }
