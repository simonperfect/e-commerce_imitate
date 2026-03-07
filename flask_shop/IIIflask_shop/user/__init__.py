#放邏輯代碼    創建藍圖

from flask import Blueprint
from flask_restful import Api

#創建藍圖對象
user_bp = Blueprint('user',__name__,url_prefix='/user')    #增加前綴

#創建Api對象

user_api = Api(user_bp)


#引入視圖

 
from . import views


