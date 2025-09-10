# utils/verification_code.py
import random
from django.core.cache import cache
from django.conf import settings

VERIFY_CODE_TIMEOUT = getattr(settings, 'VERIFY_CODE_TIMEOUT', 300)  # 默认5分钟

cache_key = "verify_code:{phone}"

# 必须一处编写，各处调用
def get_key(phone): return cache_key.format(phone=phone)

def generate_code(length=6):
    """生成指定位数的数字验证码"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def store_code(phone: str, code: str):
    """存储验证码到缓存（Redis）"""
    key = get_key(phone)
    cache.set(key, code, timeout=VERIFY_CODE_TIMEOUT)  # 缓存有效期,自动删除

def verify_code(phone: str, input_code: str) -> bool:
    """校验验证码"""
    key = get_key(phone)
    stored_code = cache.get(key)
    if stored_code and stored_code == input_code:
        cache.delete(key)  # 一次性验证码，校验后删除
        return True
    return False