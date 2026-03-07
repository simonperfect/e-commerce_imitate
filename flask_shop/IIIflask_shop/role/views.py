import sys
import os

# 添加路徑（和之前一樣）
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# 導入第三方庫
from flask import request
from flask_restful import Resource, reqparse

# 導入項目模塊
from role import role_api, role_bp
from models import db
from models import Role as RoleModel  # 避免和下面的 Resource 類重名
from models import Menu


class Roles(Resource):
    def get(self):  
        '''get the role list '''
        try: 
            roles = Role.query.all()     #get data from database
            role_list = [role.to_dict() for role in roles]
            return {'status':200, 'msg':'got character list' , 'data':role_list}
        except Exception as e:
            return{'status':500,',msg':'failed to get the character list'}
    def post(self):
        '''add role'''
        try:
            name = request.get_json().get('name')     #因爲http 的時候要傳入數據content-type=application/json 的數據  所以這裏要.get_json().get('')
            desc = request.get_json().get('desc')
            role = Role(name=name,desc=desc) #如果name 不是unique的話  name=name就會報錯 就會去except那行
            db.session.add(role)
            db.session.commit()
            return{'status':200,'msg':'added successfully'}
        except Exception as e:
            return {'status':500,'msg':'failed to add this role'}

role_api.add_resource(Roles,'/roles/')



class Role(Resource):     #individual edit
    def delete(self,id):
        try:
            role = Role.query.get(id)
            db.session.delete(role)
            db.session.commit()
            return {'status':200,'msg':'deleted successfully'}
        except Exception as e:
            return {'status':500,'msg':'failed to delete'}

    def put(self,id):   #update data
        try:
            role = Role.query.get(id)
            # create RequestParser object used to get the data
            parser = reqparse.RequestParser()
            #add parameter
            parser.add_argument('name',type=str,required=True,help='please input the character name', location='json')
            parser.add_argument('desc',type=str, location='json')


            args = parser.parse_args()   #Content-Type: application/json
            if args.get('name'):
                role.name =  args['name']
            if args.get('desc'):
                role.desc =  args['desc']
            db.session.commit()
            return {'status':200,'msg':'successfully editing!'}
        except Exception as e:
            db.session.rollback()  # ❌ 缺少事务回滚！
            return {'status':500,'msg':f'failed to edit: {str(e)}'}  # ❌ 缺少具体错误信息


role_api.add_resource(Role,'/role/<int:id>/')





@role_bp.route('/role/<int:rid>/<int:mid>/')    #delete role menu autority
def del_menu(rid:int,mid:int):
    #search the current role
    role = Role.query.get(rid)
    
    #search the current menu of this role 
    menu = Menu.query.get(mid)

    #to test whether role and menu are exists
    if all([role,menu]):
        if menu in role.menus:
            role.menus.remove(menu)
            # test whether current menu is parent node
            if menu.level == 1:
                #delete all current role's child node
                for temp in menu.children:
                    if temp in role.menus:
                        role.menus.remove(temp)
        db.session.commit()
        return {'status':200,'msg':'delete the role successfully'}
    else:
        return {'status':500,'msg':'role or menu are not exists'}




@role_bp.route('/role/<int:rid>/',methods=['POST'])
def set_menu(rid:int):    # assignment authority to role 
    try:
        role = Role.query.get(rid)
        mids = request.get_json().get('mids')

        #clear all authority
        role.menus = []
        mids = mids.split(',')
        for m in mids:
            if m: 
                #get the authority
                try:
                    menu = Menu.query.get(int(m))
                    #add the authority to role 
                    role.menus.append(menu)
                except Exception as e:
                    return{'status':500,'msg':'failed to get the authority'}
                

        # bellow here is to set it we choose the parents node the child node will be chose automatically
        selected_menus = Menu.query.filter(Menu.id.in_(mids)).all()   #filter the id which is  in menus mids
        
        # add the child node automatically
        all_menus_to_add = set(selected_menus)   #create a  set
        
        for menu in selected_menus:
            # if we choose the level one will choose level two
            if menu.level == 1:
                for child in menu.children:
                    all_menus_to_add.add(child)
        
        # add it to the tole
        for menu in all_menus_to_add:
            role.menus.append(menu)

        db.session.commit()

        return {'status':200,'msg':'assign the authority successfully'}
    
    except Exception as e:
        return{'status':200,'msh':'failed to assignment authority'}



