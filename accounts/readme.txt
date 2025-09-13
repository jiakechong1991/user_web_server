
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
curl -X POST http://192.168.0.102:5609/api/auth/login/   -H "Content-Type: application/json"   -d '{
    "username": "jiakechong1991",
    "password": "qq16421225"
  }'


## 获得个人信息
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU3NzMyMjA1LCJpYXQiOjE3NTc3MzEzMDUsImp0aSI6ImY4ZjM2ZWU2OWYyYjQ4MmRiMmI0NzQwNjdkNGFhODdjIiwidXNlcl9pZCI6IjEifQ.NMIggF243_-q7vo7cS-SjitKrBCN4K0R6MSatYikI88"   "http://192.168.0.102:5609/api/accounts/profile/"



###获取验证码
curl -X POST http://192.168.0.102:5609/api/accounts/send_code/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "15313988692"
  }'


#####注册
curl -X POST http://192.168.0.102:5609/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "richudongfang",
    "phone": "15313988692",
    "password": "qq16421225",
    "password_confirm": "qq16421225",
    "code": "751017"
  }'


####更新资料
curl -X PATCH http://192.168.0.102:5609/api/accounts/profile/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU3NzMyMjA1LCJpYXQiOjE3NTc3MzEzMDUsImp0aSI6ImY4ZjM2ZWU2OWYyYjQ4MmRiMmI0NzQwNjdkNGFhODdjIiwidXNlcl9pZCI6IjEifQ.NMIggF243_-q7vo7cS-SjitKrBCN4K0R6MSatYikI88" \
  -H "Content-Type: application/json" \
  -d '{"nickname": "我的新昵称", "signature": "我的新个性签名"}'


###上传头像
curl -X PATCH http://192.168.0.102:5609/api/accounts/profile/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU3NzMyMjA1LCJpYXQiOjE3NTc3MzEzMDUsImp0aSI6ImY4ZjM2ZWU2OWYyYjQ4MmRiMmI0NzQwNjdkNGFhODdjIiwidXNlcl9pZCI6IjEifQ.NMIggF243_-q7vo7cS-SjitKrBCN4K0R6MSatYikI88" \
  -F "nickname=带头像更新" \
  -F "avatar=@/home/wxk/project/role_play/user_web_server/static/chen.jpg"


刷新： 一旦刷新，原本的refresh 也会失效，会重新生成一组新的access 和refresh token
curl -X POST http://192.168.0.102:5609/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1ODMzNzQ5NywiaWF0IjoxNzU3NzMyNjk3LCJqdGkiOiIyYTg2M2Q5ZTE4N2E0YTRlYjEyZjkzZTZmMGM3YmM5NSIsInVzZXJfaWQiOiIxIn0.i-_fatpM8DM777FveHpGPQpwUL26_Lh6OcsJYbCq72g"
  }'


#####访问头像
/media/avatar/chen.jpg
http://a2.richudongfang1642.cn:7902/media/avatar/chen.jpg


重置密码：/api/auth/password/reset/
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



