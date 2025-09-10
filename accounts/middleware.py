# accounts/middleware.py

from django_ratelimit.exceptions import Ratelimited
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

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