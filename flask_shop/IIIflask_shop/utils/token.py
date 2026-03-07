'''
1需要加密的數據
    userid 
2加密的算法
    pip install pyjwt==2.6.0
3加密的密鑰
    SECRET_KEY
'''

import jwt
from flask import current_app     #獲取當前flask的應用對象
import time
from functools import wraps
from flask import request

#生成token 

def generate_token(data):
    #設置數據過期時間
    data.update({'exp': time.time() + 60*60*24})   #三秒過期  3600秒就是1小時後過期 
    #傳入的數據是字典
    '''1需要加密的數據'''
    token = jwt.encode(data,current_app.config['SECRET_KEY'],algorithm='HS256')   #獲取flask config 裏面的secret_key   ， algorithm='HS256' 指的是 HMAC with SHA-256 哈希算法，常用于 JWT（JSON Web Token） 的签名验证。
    return token

#解密token
def verify_token(token):
    try:
        data = jwt.decode(token,current_app.config['SECRET_KEY'],algorithms=['HS256'])
    except Exception as e:
        return None
    return data



#必須登入才可以操作
def login_required(view_func):
    @wraps(view_func)            
    def verify_token_info(*args,**kwargs):
        #獲取用戶傳來的token
        token = request.headers.get('token')

        #驗證token
        if verify_token(token): 
            return view_func(*args,**kwargs)
        else:
            return{'msg':'token無效', 'status':401}    #前端會用到 401

        #返回函數
    return verify_token_info





