import re
from django.core.exceptions import ValidationError
"""定义常用的公用 验证器"""


def validate_mobile(value):
    """校验手机号格式"""
    if not re.match(r'^1[3-9]\d{9}$', value):
        raise ValidationError('请输入有效的11位中国大陆手机号')

def validate_username(value):
    """用户名：8~16位，支持英文、数字"""
    if len(value) < 8 or len(value) > 16:
        raise ValidationError(
            '用户名长度必须在8到16位之间',code='invalid_length'
        )
    
    pattern = r'^[a-zA-Z0-9]+$'
    if not re.match(pattern, value):
        raise ValidationError(
            '用户名仅支持英文、数字',
            code='invalid_username'
        )
