

###获取agent 列表
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU3NzMzNTk3LCJpYXQiOjE3NTc3MzI2OTcsImp0aSI6IjE2OTQ5NDA0ZDJmZjQ4MGJiMjFmNTM4YzAwMTBjYjI3IiwidXNlcl9pZCI6IjEifQ.ZhMFtBTzMwD23ROmRpoCuhzrKBvDnxLBGBcUu0Lu5Oo"   "http://192.168.0.102:5609/api/agents/"

###创建agent
curl -X POST http://192.168.0.102:5609/api/agents/ \
  -H "Content-Type: application/json" \
  -H "Authorization:  Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU3NzM0NjY1LCJpYXQiOjE3NTc3MzM3NjUsImp0aSI6IjU0YTUwNDJlMzIxNjQwY2FiZTM3YWJlYmE2MTI5NTYxIiwidXNlcl9pZCI6IjEifQ.w49Eylqq0ocPP_pq4Mep9mMyqXAaiW8B2pAPMEqSXhE" \
  -d '{
    "agent_name": "钢铁侠",
    "sex": "m",
    "birthday": "1980-05-29",
    "signature": "天才、亿万富翁、花花公子、慈善家",
    "hobby": "造装甲、开派对、拯救世界"
  }'

###更新agent  PATCH /api/agents/<id>/
curl -X PATCH http://192.168.0.102:5609/api/agents/1/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU3NzM0NjY1LCJpYXQiOjE3NTc3MzM3NjUsImp0aSI6IjU0YTUwNDJlMzIxNjQwY2FiZTM3YWJlYmE2MTI5NTYxIiwidXNlcl9pZCI6IjEifQ.w49Eylqq0ocPP_pq4Mep9mMyqXAaiW8B2pAPMEqSXhE" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "钢铁侠3"
  }'



###获得agent详情  GET /api/agents/<id>/ 
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU3NzM0NjY1LCJpYXQiOjE3NTc3MzM3NjUsImp0aSI6IjU0YTUwNDJlMzIxNjQwY2FiZTM3YWJlYmE2MTI5NTYxIiwidXNlcl9pZCI6IjEifQ.w49Eylqq0ocPP_pq4Mep9mMyqXAaiW8B2pAPMEqSXhE"   "http://192.168.0.102:5609/api/agents/1/"



###上传头像
curl -X PATCH http://192.168.0.102:5609/api/agents/1/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU3NzM0NjY1LCJpYXQiOjE3NTc3MzM3NjUsImp0aSI6IjU0YTUwNDJlMzIxNjQwY2FiZTM3YWJlYmE2MTI5NTYxIiwidXNlcl9pZCI6IjEifQ.w49Eylqq0ocPP_pq4Mep9mMyqXAaiW8B2pAPMEqSXhE" \
  -F "avatar=@/home/wxk/project/role_play/user_web_server/static/chen.jpg"


###删除agent  DELETE /api/agents/1/ 
curl -X DELETE -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU3NzM0NjY1LCJpYXQiOjE3NTc3MzM3NjUsImp0aSI6IjU0YTUwNDJlMzIxNjQwY2FiZTM3YWJlYmE2MTI5NTYxIiwidXNlcl9pZCI6IjEifQ.w49Eylqq0ocPP_pq4Mep9mMyqXAaiW8B2pAPMEqSXhE"   "http://192.168.0.102:5609/api/agents/1/"




