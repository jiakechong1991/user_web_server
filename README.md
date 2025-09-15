# user_web_server


### 端口不能轻易修改，这些端口都是在frp中配置好远程访问的
python ./manage.py runserver  localhost:5609
python ./manage.py runserver  192.168.0.102:5609

http://a2.richudongfang1642.cn:7902/admin
curl -X POST http://a2.richudongfang1642.cn:7902/api/accounts/send_code/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "15313988692"
  }'

curl -X POST http://192.168.0.102:5609/api/accounts/send_code/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "15313988692"
  }'

超级账户：
python manage.py createsuperuser
账户：admin   密码：qq16421225


