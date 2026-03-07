#弄前端的菜單   目錄


from flask import Blueprint
from flask_restful import Api

#Blueprint（藍圖）是 Flask 中用來組織大型應用的模組化工具


menu_bp = Blueprint('menu',__name__,url_prefix='/menu')


#create api object
menu_api = Api(menu_bp)


#import logic module views
from . import views

