# -*- coding:utf-8 -*-
import jwt
import json
from datetime import datetime

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE2MjcxMDgxLCJpYXQiOjE3MTYxODQ2ODEsImp0aSI6IjQyZDYxNDJjNzNjMjRkODZiZTdiMGU4YTJmMzJiNjhlIiwidXNlcl9pZCI6MiwidXNlcm5hbWUiOiIyNDA3NTAiLCJuYW1lIjoiXHU1MjE4XHU1MTQ2XHU1MTc1In0.WPBw881ucC94p6fzj4uiHvKqaxpLNsgQkwiiEbS0mFw"

payload = jwt.decode(token, options={"verify_signature": False})

if 'exp' in payload:
    expiration_time = datetime.utcfromtimestamp(payload['exp'])
    print("Token will expire at:", expiration_time)
else:
    print("Token does not have an expiration time.")

print(json.dumps(payload, ensure_ascii=False))
