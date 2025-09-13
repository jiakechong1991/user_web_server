
#原理：整体采用  dj-rest-auth + django-allauth + djangorestframework-simplejwt 技术组合

access token：可存内存或轻量存储。 一半是 15分钟左右的时间。 就算被截获，最多只能用 15 分钟，之后失效
refresh token：必须加密存储。 生命周期是7天。 用户点击“退出登录” 将refresh token加入黑名单，彻底失效


# 工作流程（典型 JWT 认证）
用户登录
    │
    ▼
服务器返回 → { "access": "abc", "refresh": "xyz" }
    │
    ├── access 存入内存 → 用于后续 API 请求
    └── refresh 安全存储 → 用于未来刷新

15分钟后，access token 过期
    │
    ▼
客户端用 refresh token 请求：
POST /api/auth/refresh/
{ "refresh": "xyz" }

    │
    ▼
服务器验证 refresh 是否有效、未过期、未拉黑
    │
    ▼
返回新的 → { "access": "new123", "refresh": "new456" }（如果启用轮换）

###android中 登录流程
1. 当 API 返回 401 Unauthorized 时：
2. 尝试用 refresh token 调用 /api/auth/refresh/
    1. 成功 → 更新 access token，重试原请求
    2. 失败（refresh 也过期或无效）→ 跳转登录页


###
随着token在黑名单表中积累的越来越多，可以使用下面命令删除：
python manage.py flushexpiredtokens   # 将其挂到crontab上，每天定期进行(大用户量下)


#############操作API#############




