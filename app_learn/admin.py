from django.contrib import admin

# Register your models here.
from .models import TQuestion

admin.site.register(TQuestion)  # 在管理界面，添加一个对该模型类的管理页面(包括基本的增删改查功能)