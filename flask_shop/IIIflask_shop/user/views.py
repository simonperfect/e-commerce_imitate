#charset=utf-8
import sys
import os

# 添加路徑（這是最關鍵的！）
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# 現在開始導入
from flask import request
from flask_restful import Resource, reqparse
import re

# 導入項目內的模塊
from user import user_bp, user_api
from models import db
from models import Userform  # 假設你的模型類叫 Userform
from utils.token import generate_token, verify_token, login_required
#創建視圖
@user_bp.route('/')
def index():
    return 'Hello user!'



#用戶登入功能
@user_bp.route('/login/',methods = ['POST'])   #POST：提交/创建数据
def login():
    '''獲取用戶名''' 
    #name = request.form.get('name')    #content_type: application/x-www-form-urlencoded   form
    name = request.get_json().get('name')   #content_type:  application/json     json

    '''獲取密碼'''
    pwd = request.get_json().get('pwd')


    '''判斷是否正確'''
    #判斷傳遞數據完整
    if not all([name,pwd]):      #e.g.  all([True,False])    返回False      true true 返回true   也就是name 和 pwd其中一個是false 的話  就會return
        return {'status':400,'msg':'參數不完整'}
    else:
        #查詢數據庫   通過用戶名獲取用戶對象
        user = Userform.query.filter(Userform.name == name).first()

        if user:   #如果user有值的話
            #判斷密碼是否正確
            if user.checkpassword(pwd):
                #生產一個token
                token = generate_token({'id':user.id})
                #獲取token解析的值
                print(verify_token(token))
                return {'msg':'登錄成功', 'data': {'token':token},"status":200}
            else:
                return {'msg':'用戶名或者密碼錯誤', 'status': 400}
        else:
            return {'msg':'用戶名或者密碼錯誤','status':400 }
    


#注冊用戶
class Regist_users(Resource):   #get數據是獲取數據list 
    def get(self):         #這裏get 用了兩部分 parser.add_argument  和 arg.get('name')  上面直接是request.get_json().get('name')  雖然這種寫法更簡短但是兩步的可以設置更多參數例如default
        # create requestparser object      
        parser = reqparse.RequestParser()    #是 Flask-RESTful 套件中用於解析 HTTP 請求參數的工具
        # get user list   問訪問者要訪問多少條用戶數據
        parser.add_argument('pnum',type=int, default=1,help='wrong page',location='args')   #default默認返回第一頁
        parser.add_argument('psize',type=int, default=10,location='args')    #每一頁顯示多少數據
        parser.add_argument('name',type=str, location='args')     #以名稱搜索   location='args' URL 查詢參數

        args = parser.parse_args()    #解析參數

        name = args.get('name')   #獲取裏面的數據
        pnum = args.get('pnum')
        psize = args.get('psize')

        #獲取用戶列表
        if name:
            user_list = Userform.query.filter(Userform.name.like(f'%{name}%')).paginate(page=pnum,per_page=psize)     #.paginate(pnum, psize) 是一個常見的分頁方法
        else:  #不傳name
            user_list = Userform.query.paginate(page=pnum,per_page=psize)
        data = {
            'total':user_list.total,
            'pnum':pnum,
            'data':[u.to_dict() for u in user_list.items]
        }
        return {'status':200,'msg':'User are founded' ,'data':data}

            
    def post(self):   #post請求是追加數據
        #注冊用戶
        #接受用戶信息
        name = request.get_json().get('name')
        pwd = request.get_json().get('pwd')
        #輸入兩次密碼  驗證密碼
        real_pwd = request.get_json().get('real_pwd')
        
        phone = request.get_json().get('phone')
        email = request.get_json().get('email')
        nick_name = request.get_json().get('nick_name')

        #驗證數據合法性
        if not all([name,pwd,real_pwd]):
            return {'msg':'參數不完整', 'status':400 }
        
        #判斷兩次密碼一直心懷
        if pwd != real_pwd:
            return {'msg': '兩次密碼不一致' ,'status': 400} 
                   
        #判斷用戶名是否合法
        if len(name)<2:
            return{'msg':'用戶名不合法','status':400}
        
        #判斷手機號合法    以大陸 開頭1 第二個數字（3-9） 後面跟九個數字
        if not re.match(r'^1[3-9]\d{9}$', phone):   
            return{'msg':'手機號不合法','status':400}
        
        #判斷郵箱是否合法    在網上搜尋郵箱正則PHP  
        if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            return{'msg':'郵箱不合法','status':400}
        
        #recieve role_id
        role_id = request.get_json().get('role_id')
        
        #判斷是否有重複的用戶
        try:
            user = Userform.query.filter(Userform.name == name).first()
            if user:
                return{'msg':'用戶名已經存在','status':400}
        except Exception as e:
            print(e)

        #創建用戶對象   
        if role_id:  #if there have role id 
            user = Userform(name=name, password=pwd,nick_name=nick_name,phone=phone,email=email,role_id=role_id)
        else:    
            user = Userform(name=name, password=pwd,nick_name=nick_name,phone=phone,email=email)
        #保存數據
        db.session.add(user)
        db.session.commit()
        return {'msg': '注冊成功', 'status':200} 
        
user_api.add_resource(Regist_users,'/register/')

 
 #單體數據内容   個人
class User(Resource):
    def get(self,id):
        user = Userform.query.get(id)
        if user:
            return {'status':200,'msg':'Query successful','data':user.to_dict()} 
        else:
            return{'status':404,'msg':'User not found'}
        

    def put(self,id):   #修改用戶信息
        try:
            user = Userform.query.get(id)
            #   create RequestParser object to recieve data
            parser = reqparse.RequestParser()   
            # 定义允许接收的参数
            parser.add_argument('nick_name',type=str)
            parser.add_argument('phone', type=str)
            parser.add_argument('email',type=str)
            
            #add role id
            parser.add_argument('role_id',type=int)

            # 4. 解析请求参数
            args = parser.parse_args()

            # 5. 条件更新（只更新有值的字段）
            if args.get('nick_name'):
                user.nick_name = args.get('nick_name')
            if args.get('phone'):
                user.phone = args.get('phone')
            if args.get('email'):
                user.email = args.get('email')
            if args.get('role_id'):
                user.role_id = args.get('role_id')
            

            # 6. 保存到数据库
            db.session.commit()
            return {'status':200 ,'msg':'modified','data':user.to_dict()}
        except Exception as e:
            print(e)
            return {'status':400,'msg':'modify error'}


         
    def delete(self,id):
        try:
            user = Userform.query.get(id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return {'status':200,'msg':'deleted'}
            else:
                return {'status':404,'msg':'User not found'}
        except Exception as e:
            print(e)
            return {'status':400,'msg':'delete error'}
user_api.add_resource(User,'/user/<int:id>/')


# reset password
@user_bp.route('/reset_pwd/<int:id>/')   #爲什麽不用restful方法也就是add_resource 這是因爲這個只是很簡單的一個方法  沒有上面那麽複雜的depete put post等等的function
def reset_pwd(id):
    try:
        user = Userform.query.get(id)
        user.password = '123456'
        db.session.commit()
        return {'status':200, 'msg':'verification successful, the password is 123456'}
    except Exception as e:
        print(e)
        return {'status':400, 'msg':'reset failed'}







@user_bp.route('/test/',methods=['GET'])
@login_required
def test_login_required():
    return{'status':200, 'msg':'通過驗證'}
