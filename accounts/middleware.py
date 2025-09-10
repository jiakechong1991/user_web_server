# accounts/middleware.py

from django_ratelimit.exceptions import Ratelimited
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

"""
验证码的限流配置中 block=True → 抛出 Ratelimited 异常 → 在进入 DRF 视图前就被 Django 拦截 
→ DRF 的 EXCEPTION_HANDLER 无效 → 所以你必须在 Django 层（不是 DRF 层）捕获这个异常！
所以选择 加一个中间件处理 Ratelimited 异常
"""

class RatelimitJsonMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, Ratelimited):
            return JsonResponse(
                {
                    "error": "刷新太频繁了，请一会再申请验证码",
                    "code": "RATE_LIMITED"
                },
                status=429,  # HTTP 429 Too Many Requests
                json_dumps_params={'ensure_ascii': False}  # 支持中文
            )
        return None  # 其他异常交给后续中间件处理