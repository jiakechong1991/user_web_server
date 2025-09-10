# accounts/services.py
from utils.verification import generate_code, store_code
from utils.sms import send_verification_code

def send_verification_code_service(phone: str) -> dict:
    """
    生成验证码 + 存储 + 发送
    返回: {'success': True, 'message': '...'}
    """
    code = generate_code()
    store_code(phone, code)

    # 发送短信（同步 or 异步？见下文）
    sent = send_verification_code(phone, code)

    if sent:
        return {'success': True, 'message': '验证码已发送'}
    else:
        return {'success': False, 'message': '短信发送失败，请重试'}