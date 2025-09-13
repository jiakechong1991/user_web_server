# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .validators import validate_mobile,validate_username

# 我们将用户模型，拆分成两个模型， 一个是用户模型(用于登录验证)， 一个是用户信息模型
# 认证归认证，资料归资料，解耦和开


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, phone, email=None):
        if not username:
            raise ValueError('必须提供用户名')
        if not phone:  
            raise ValueError('必须提供手机号')

        email = self.normalize_email(email) if email else None

        user = self.model(
            username=username,
            phone=phone,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, phone, email=None):
        if not username:
            raise ValueError('必须提供用户名')
        if not phone:  
            raise ValueError('必须提供手机号')
        user = self.create_user(
            username=username,
            password=password,
            phone=phone,
            email=email or f'{username}@admin.local'
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# django只提供了“骨架”用户模型(AbstractBaseUser)， 但是不包含创建用户方法， 
# 创建用户模型时，需要继承 AbstractBaseUser， 也必须继承后user的Manager类，辅助创建用户
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # 唯一字段：username，既是登录账号
    username = models.CharField(
        max_length=16,
        # primary_key=True,
        unique=True,  # 唯一字段,不允许重复
        verbose_name="账户名称",
        help_text="英文数字混合",
        validators=[MinLengthValidator(8), MaxLengthValidator(16), validate_username]  # 强制格式校验
    )
    phone = models.CharField(
        max_length=11,
        # unique=True,  # 电话号码 后期可能修改
        # null=True, # 允许为空
        #  blank=True, # 允许表单为空
        verbose_name="手机号",
        help_text="请输入11位中国大陆手机号",
        validators=[validate_mobile]  # 强制格式校验
    )
    email = models.EmailField(blank=True, null=True, verbose_name="邮箱")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()  # 配置管理类
    
    #默认情况下，Django 所有模型都有一个 objects = models.Manager()，用于执行数据库查询（如 User.objects.all()）
    #因为你继承的是 AbstractBaseUser，它不包含默认的 create_user() 和 create_superuser() 方法 
    # —— 而这些方法是 Django 用户系统（尤其是命令行[python manage.py createsuperuser]和 Admin）必须依赖的。
    

    USERNAME_FIELD = 'username'  # 指定 这个字段 作为 登录时用的唯一标识字段
    # 
    REQUIRED_FIELDS = ['phone']  # 创建 账户时必须要提供的其他字段(必须是CustomUser有的字段)

    def __str__(self): # 控制print时，该类对象的显示字符串
        return self.username

    class Meta:  # 用于控制在django admin中显示 这个类的名称
        # （Django Admin 自动生成界面时，会读取 Meta 类中的这些配置）
        verbose_name = "用户"
        verbose_name_plural = "用户"


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=20, verbose_name="昵称")
    avatar = models.ImageField(upload_to='avatar', verbose_name="头像")
    sex = models.CharField(max_length=1, choices=(('m', '男'), ('f', '女')), verbose_name="性别")
    birthday = models.DateField(verbose_name="生日")
    education = models.CharField(max_length=50, blank=True, verbose_name="学历")
    signature = models.CharField(max_length=100, verbose_name="个性签名")
    hobby = models.CharField(max_length=100, blank=True, verbose_name="爱好")
    
    updated_at = models.DateTimeField(auto_now=True)  # 更新时间

    def __str__(self):
        return f"{self.user.username} 的资料"








