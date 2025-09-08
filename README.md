# user_web_server


### 端口不能轻易修改，这些端口都是在frp中配置好远程访问的
python ./manage.py runserver  localhost:5609

超级账户：
python manage.py createsuperuser
账户：admin   密码：qq16421225



#登录：
curl -X POST http://127.0.0.1:5609/api/auth/login/   -H "Content-Type: application/json"   -d '{
    "username": "15313988691",
    "password": "new12345678"
  }'

#查看用户信息： 
 curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU3MzM4MzE4LCJpYXQiOjE3NTczMzY1MTgsImp0aSI6IjcwMmM0NjEwNjkyNTQ5YzJhN2Y0MzFiM2ZmMTg5NDZmIiwidXNlcl9pZCI6IjEifQ.BylcgAhsUzMmiOx7gWIFpqfQPh1SOqPTTgCioFWbvyE"   "http://127.0.0.1:5609/api/accounts/profile/"


注册：/api/auth/registration/
curl -X POST http://127.0.0.1:5609/api/auth/registration/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "15313988692",
    "password1": "qq16421225",
    "password2": "qq16421225"
  }'


重置密码：/api/auth/password/reset/


登出：  /api/auth/logout/

 curl -X POST http://127.0.0.1:5609/api/auth/logout/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU3MzM4OTY4LCJpYXQiOjE3NTczMzcxNjgsImp0aSI6IjA2MDQ0OTk3ZWU0NDRmN2Y5YWQ4MDkxZDc1NzVkMTUyIiwidXNlcl9pZCI6IjEifQ.BZigq7SNw1Q9XRYPwYUUwEGutKVJqQW8SCqyxnV4aJY" \
  -d '{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1ODU0Njc2OCwiaWF0IjoxNzU3MzM3MTY4LCJqdGkiOiJkZDMwODE4ODEwZWM0ZTYwYWJiZWJjOGU1YjBmN2VmMyIsInVzZXJfaWQiOiIxIn0.Rk6Kxj6hXLiPxHopN1vkA77hNRQt6UxfZ63cMHYYub4"
  }'


修改密码： 
curl -X POST http://127.0.0.1:5609/api/auth/password/change/ \
  -H "Content-Type: application/json" \
  -H "Authorization:  Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU3MzM4OTY4LCJpYXQiOjE3NTczMzcxNjgsImp0aSI6IjA2MDQ0OTk3ZWU0NDRmN2Y5YWQ4MDkxZDc1NzVkMTUyIiwidXNlcl9pZCI6IjEifQ.BZigq7SNw1Q9XRYPwYUUwEGutKVJqQW8SCqyxnV4aJY" \
  -d '{
    "old_password": "qq16421225",
    "new_password1": "new12345678",
    "new_password2": "new12345678"
  }'