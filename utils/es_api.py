# -*- coding: utf-8 -*-
import requests
import json
import base64
from copy import deepcopy


def create_person_info_es(payload):
    """调用更后端服务的/es/update_person_info  创建person_info"""
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "CustomUserAgent/1.0"           # 示例：自定义用户代理
    }

    url_prefix = "http://localhost:5097"
    
    assert "user_name" in payload and "agent_id" in payload, u"payload参数错误,必须包含user_name和agent_id字段"
    old_payload = deepcopy(payload)
    del old_payload["agent_id"]
    del old_payload["user_name"]
    # 重新整理格式：
    new_payload = {
        "user_name": payload["user_name"],
        "agent_id": payload["agent_id"],
        "base_info": old_payload,
    }
    
    print(new_payload)

    # 发送 POST 请求
    url = url_prefix + "/es/update_person_info"
    response = requests.post(url, json=new_payload, headers=headers)
    
    # 检查响应状态码
    if response.status_code == 200:
        return response.json()
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(f"错误信息: {response.text}")
        return {}





if __name__ == '__main__':
    pass