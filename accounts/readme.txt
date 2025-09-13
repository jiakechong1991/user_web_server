
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





#登录：
curl -X POST http://192.168.0.102:5609/api/auth/login/   -H "Content-Type: application/json"   -d '{
    "username": "jiakechong1991",
    "password": "qq16421225"
  }'

注册：/api/auth/registration/
curl -X POST http://192.168.0.102:5609/api/auth/registration/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "15313988692",
    "password1": "qq16421225",
    "password2": "qq16421225"
  }'


重置密码：/api/auth/password/reset/

刷新：
curl -X POST http://192.168.0.102:5609/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1Nzk0NDU5MiwiaWF0IjoxNzU3MzM5NzkyLCJqdGkiOiIyMTNiZDgwZGYyOTI0Mzc1YTUyNjU2NmMyNzUzMjBmNiIsInVzZXJfaWQiOiIxIn0.wkgfOjtRmv3LU7G0Xgd5VwYsBCB6eY9YUKCbKvQ_Uzg"
  }'

登出：  /api/auth/logout/

 curl -X POST http://192.168.0.102:5609/api/auth/logout/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU3MzM4OTY4LCJpYXQiOjE3NTczMzcxNjgsImp0aSI6IjA2MDQ0OTk3ZWU0NDRmN2Y5YWQ4MDkxZDc1NzVkMTUyIiwidXNlcl9pZCI6IjEifQ.BZigq7SNw1Q9XRYPwYUUwEGutKVJqQW8SCqyxnV4aJY" \
  -d '{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1ODU0Njc2OCwiaWF0IjoxNzU3MzM3MTY4LCJqdGkiOiJkZDMwODE4ODEwZWM0ZTYwYWJiZWJjOGU1YjBmN2VmMyIsInVzZXJfaWQiOiIxIn0.Rk6Kxj6hXLiPxHopN1vkA77hNRQt6UxfZ63cMHYYub4"
  }'


修改密码： 
curl -X POST http://192.168.0.102:5609/api/auth/password/change/ \
  -H "Content-Type: application/json" \
  -H "Authorization:  Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU3MzM4OTY4LCJpYXQiOjE3NTczMzcxNjgsImp0aSI6IjA2MDQ0OTk3ZWU0NDRmN2Y5YWQ4MDkxZDc1NzVkMTUyIiwidXNlcl9pZCI6IjEifQ.BZigq7SNw1Q9XRYPwYUUwEGutKVJqQW8SCqyxnV4aJY" \
  -d '{
    "old_password": "qq16421225",
    "new_password1": "new12345678",
    "new_password2": "new12345678"
  }'



###查询用户的信息（只要带着自己的token就行）
 curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU3NDI3Njg4LCJpYXQiOjE3NTc0MjY3ODgsImp0aSI6ImFmNzMxN2MxYjQ4MDQ5MTVhZjdhNDVkZDYwMmE3ZGY2IiwidXNlcl9pZCI6IjEifQ.0o9NQoDfwZ5swvvRnGEBiMlALzTsTfmPwmPgqLL3tEw"   "http://192.168.0.102:5609/api/accounts/profile/"

####更新资料
curl -X PATCH http://192.168.0.102:5609/api/accounts/profile/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU3NDI1NTE2LCJpYXQiOjE3NTc0MjQ2MTYsImp0aSI6IjMwMzYyZjkyZjU0NTQzOTE4MGMzYmFhYzYyM2RlZmQyIiwidXNlcl9pZCI6IjEifQ.COQIVRf3I8QefDp2AmCGTsOUAOks2kmdAOuyxTmrYKs" \
  -H "Content-Type: application/json" \
  -d '{"nickname": "我的新昵称", "signature": "我的新个性签名"}'


###上传头像
curl -X PATCH http://192.168.0.102:5609/api/accounts/profile/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU3NDI3MDk0LCJpYXQiOjE3NTc0MjYxOTUsImp0aSI6ImZlNGQ4N2Y0YzU1NTRiZWU5MmFlN2JiODQ4OGJjMGNjIiwidXNlcl9pZCI6IjEifQ.Ip21SbXrmcFKKCYlAcFJCwHhhYl9Af56vCgFVdycZyo" \
  -F "nickname=带头像更新" \
  -F "avatar=@/home/wxk/project/role_play/user_web_server/static/chen.jpg"

#####访问头像
/media/avatar/chen.jpg
http://a2.richudongfang1642.cn:7902/media/avatar/chen.jpg
