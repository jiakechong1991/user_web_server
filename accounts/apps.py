from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # django启动时，不会自动加载 signals.py，必须手动导入，才能注册信号
        #   ready() 方法在 Django 应用初始化完成时调用
        #   import accounts.signals → 执行 signals.py → @receiver 装饰器生效 → 注册回调函数到信号系统
        import accounts.signals