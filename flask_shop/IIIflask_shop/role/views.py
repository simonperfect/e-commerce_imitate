import sys
import os

# 添加路徑（和之前一樣）
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# 導入第三方庫
from flask import request, current_app
from flask_restful import Resource, reqparse

# 導入項目模塊
from role import role_api, role_bp
from extensions import db
# 注意：不在模塊級別導入 Role，而是在函數內部導入

class Roles(Resource):
    def get(self):  
        '''get the role list '''
        try:
            with current_app.app_context():
                from models import Role
                print(f"Role 類型: {type(Role)}")
                print(f"Role 是否有 query: {hasattr(Role, 'query')}")
                
                roles = Role.query.all()
                role_list = [role.to_dict() for role in roles]
                return {'status': 200, 'msg': 'got character list', 'data': role_list}
        except Exception as e:
            print(f"錯誤: {e}")
            import traceback
            traceback.print_exc()
            return {'status': 500, 'msg': 'failed to get the character list'}
    
    def post(self):
        '''add role'''
        try:
            with current_app.app_context():
                from models import Role
                name = request.get_json().get('name')
                desc = request.get_json().get('desc')
                role = Role(name=name, desc=desc)
                db.session.add(role)
                db.session.commit()
                return {'status': 200, 'msg': 'added successfully'}
        except Exception as e:
            print(f"錯誤: {e}")
            return {'status': 500, 'msg': 'failed to add this role'}

role_api.add_resource(Roles, '/roles/')

class Role(Resource):
    def delete(self, id):
        try:
            with current_app.app_context():
                from models import Role
                role = Role.query.get(id)
                db.session.delete(role)
                db.session.commit()
                return {'status': 200, 'msg': 'deleted successfully'}
        except Exception as e:
            print(f"錯誤: {e}")
            return {'status': 500, 'msg': 'failed to delete'}

    def put(self, id):
        try:
            with current_app.app_context():
                from models import Role
                role = Role.query.get(id)
                parser = reqparse.RequestParser()
                parser.add_argument('name', type=str, required=True, help='please input the character name', location='json')
                parser.add_argument('desc', type=str, location='json')

                args = parser.parse_args()
                if args.get('name'):
                    role.name = args['name']
                if args.get('desc'):
                    role.desc = args['desc']
                db.session.commit()
                return {'status': 200, 'msg': 'successfully editing!'}
        except Exception as e:
            db.session.rollback()
            print(f"錯誤: {e}")
            return {'status': 500, 'msg': f'failed to edit: {str(e)}'}

role_api.add_resource(Role, '/role/<int:id>/')

@role_bp.route('/role/<int:rid>/<int:mid>/')
def del_menu(rid: int, mid: int):
    try:
        with current_app.app_context():
            from models import Role, Menu
            role = Role.query.get(rid)
            menu = Menu.query.get(mid)

            if all([role, menu]):
                if menu in role.menus:
                    role.menus.remove(menu)
                    if menu.level == 1:
                        for temp in menu.children:
                            if temp in role.menus:
                                role.menus.remove(temp)
                db.session.commit()
                return {'status': 200, 'msg': 'delete the role successfully'}
            else:
                return {'status': 500, 'msg': 'role or menu are not exists'}
    except Exception as e:
        print(f"錯誤: {e}")
        import traceback
        traceback.print_exc()
        return {'status': 500, 'msg': 'error occurred'}

@role_bp.route('/role/<int:rid>/', methods=['POST'])
def set_menu(rid: int):
    try:
        with current_app.app_context():
            from models import Role, Menu
            role = Role.query.get(rid)
            mids = request.get_json().get('mids')

            role.menus = []
            mids = mids.split(',')
            for m in mids:
                if m:
                    try:
                        menu = Menu.query.get(int(m))
                        role.menus.append(menu)
                    except Exception as e:
                        print(f"添加菜單錯誤: {e}")
                        return {'status': 500, 'msg': 'failed to get the authority'}

            selected_menus = Menu.query.filter(Menu.id.in_(mids)).all()
            all_menus_to_add = set(selected_menus)

            for menu in selected_menus:
                if menu.level == 1:
                    for child in menu.children:
                        all_menus_to_add.add(child)

            for menu in all_menus_to_add:
                if menu not in role.menus:
                    role.menus.append(menu)

            db.session.commit()
            return {'status': 200, 'msg': 'assign the authority successfully'}
    except Exception as e:
        print(f"錯誤: {e}")
        import traceback
        traceback.print_exc()
        return {'status': 500, 'msg': 'failed to assignment authority'}