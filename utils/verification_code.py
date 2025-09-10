# utils/verification_code.py
import random
from django.core.cache import cache # 使用django的缓存
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

def send_sms(phone: str, template_code: str, params: dict) -> dict:
    """调用第三方服务，向手机发送短信"""
    print("{template_code}向{phone}发送短信验证码：{code}".format(
        template_code=template_code, phone=phone, code=params.get('code')))
    return {"code": "OK", "message": "OK"}

def send_verification_code(phone: str, code: str) -> bool:
    """
    发送验证码到手机
    返回 True/False 表示是否发送成功
    """
    try:
        # 调用第三方短信 API
        result = send_sms(
            phone=phone,
            template_code="SMS_123456789",
            params={"code": code}
        )
        if result.get('code') == 'OK':
            print(f"短信发送成功: {phone}")
            return True
        else:
            print(f"短信发送失败: {phone}, 原因: {result.get('message')}")
            return False
    except Exception as e:
        print(f"发送短信异常: {phone}")
        return False
    

if __name__ == '__main__':
    pass