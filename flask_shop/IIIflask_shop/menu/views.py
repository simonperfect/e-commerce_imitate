from IIIflask_shop.menu import menu_api
from flask_restful import Resource     #每個 URL 端點對應一個資源（Resource）
from IIIflask_shop import models
from flask import request




class Menus(Resource):  #目錄
    def get(self):
        #獲取前端頁面要求的數據類型,list ,tree    atgs 是 URL 查询参数 http://example.com/api?name=value&type=user   其中 name=value&type=user是args查詢參數
        type_=request.args.get('type_')
        #根據type決定 以這種類型返回
        if type_=='tree':
        # 通過模型獲取數據
            menu_list = models.Menu.query.filter(models.Menu.level==1).all()     #獲取所有 level 等於 1 的菜單項  這確實是第一層（level=1）的菜單，然後包含了它們的第二層子菜單。這是一個嵌套結構
            menu_data = []
            #遍歷數據
            for m in menu_list:
                menu_data.append(m.to_dict_tree())
            return {'status':200, 'msg':'got the menu','data':menu_data}
        else:
            menu_list = models.Menu.query.filter(models.Menu.level!=0).all()      #返回的數據會是平鋪的列表，而不是嵌套結構  
            menu_data=[]
            for m in menu_list:
                menu_data.append(m.to_dict_list())
            return {'status':200,'msg':'got the menu','data':menu_data}




menu_api.add_resource(Menus,'/menus/')


