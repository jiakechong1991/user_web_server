# accounts/services.py
from utils.verification_code import generate_code, store_code, send_verification_code


def send_verification_code_service(phone: str) -> dict:
    """
    生成验证码 + 存储 + 发送
    返回: {'success': True, 'message': '...'}
    """
    code = generate_code()  # 生成验证码
    store_code(phone, code)  # 存储验证码

    # 发送短信（同步 or 异步？见下文）
    sent = send_verification_code(phone, code)

    if sent:
        return {'success': True, 'message': '验证码已发送'}
    else:
        return {'success': False, 'message': '短信发送失败，请重试'}