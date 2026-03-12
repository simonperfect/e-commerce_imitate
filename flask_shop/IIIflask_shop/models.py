#創建數據庫表格
from extensions import db

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class BaseModel(object):      # object 是所有類的基類   
    create_time = db.Column(db.DateTime,default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now,onupdate=datetime.now)

class Userform(db.Model,BaseModel):        # 繼承自父類：BaseModel   db.Model 的元類會處理這個類定義
    __tablename__ = 't_users'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(32), unique = True ,nullable = False)
    pwd = db.Column(db.Text)
    nick_name = db.Column(db.String(32))
    phone = db.Column(db.String(11))
    email = db.Column(db.String(32))


    #建立用戶與角色的關係  1對多  一個用戶擁有多個角色
    role_id = db.Column(db.Integer,db.ForeignKey('t_role.id'))


    



#密碼優化：      將密碼加密例如原本密碼是password: 123456     加密後變成pwd: 1a3b5c6 
    @property    # 1. getter - 讀取屬性時調用      e.g.hashed = user.password   print(hashed.password) 
    def password(self):             #用戶在設置密碼的時候認爲在操作的字段是password 其實數據庫保存是pwd
        return self.pwd
    
    @password.setter                    #setter - 設置屬性時調用  e.g.user.password = "123"
    def password(self,pwd):   
        self.pwd = generate_password_hash(pwd)   #數據加密完  1a3b5c6

    def checkpassword(self,pwd):
        if not self.pwd:
            return False
        return check_password_hash(self.pwd,pwd)    #檢查加密後的密碼是否正確
    
    def to_dict(self):
        return{
            'id': self.id,
            'name':self.name,
            'nick_name':self.nick_name,
            'phone':self.phone,
            'email':self.email,
            'role_name':self.role.name if self.role else'' ,          #because Role function bellow already set the backref it means that Userfrom here can use role as a  reference
            'role_id':self.role.id if self.role else '',
        }


    
    #connect Menu and Role s' third table
trm = db.Table('t_roles_menus',
               db.Column('role_id',db.Integer,db.ForeignKey('t_role.id')),
               db.Column('menu_id',db.Integer,db.ForeignKey('t_menus.id')),
               )

class Menu(db.Model):
    __tablename__ = 't_menus'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(32),unique=True,nullable =False)
    path =  db.Column(db.String(32)) 
    level = db.Column(db.Integer,default=1)
    pid = db.Column(db.Integer,db.ForeignKey('t_menus.id'))   
    children = db.relationship('Menu')

    roles = db.relationship('Role', secondary=trm, back_populates='menus')


    def to_dict_tree(self):
        return{
        'id':self.id,
        'name':self.name,   
        'path':self.path,
        'level':self.level,
        'pid':self.pid,
        'children':[child.to_dict_tree() for child in self.children]      #因爲每一個點都有child 所以套很多個  這裏是獲取這個父節點的所有子節點
        
        }

    def to_dict_list(self):
        return{
        'id':self.id,
        'name':self.name,   
        'path':self.path,
        'level':self.level,
        'pid':self.pid,
        
        }
    

 
class Role(db.Model):
    __tablename__ = 't_role'
    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    name = db.Column(db.String(32), unique=True,nullable=False)
    desc = db.Column(db.String(128 ))

    #角色和用戶的關係 一對多  多個用戶擁有同一個角色 反向查找  
    users = db.relationship('Userform',backref='role')

    #来建立多对多关系
    menus = db.relationship('Menu', secondary=trm, back_populates='roles')


    def to_dict(self):
        return{
            'id':self.id,
            'name':self.name,
            'desc':self.desc, 
            #'menu':[m.to_dict_list() for m in self.menus],     #method 1当通过 Flask API 返回数据时，必须是 JSON 格式    list
            #'menu': [m.to_dict_tree() for m in self.menus if m.level== 1]    # method2 tree  m.to_dict_tree()是獲取這個父節點的所有子節點  但是我們只需要獲取role這個角色的menu  不是menu的子節點 例如我們menu3 有自己子節點31 32 而我們的role只有31 這句會返回31和32  但實際上只有31    所以我們用方法三
            'menu':self.get_menu_dict()   #method 3

        } 

    def get_menu_dict(self):   #get the authority of this role 
        
        menu_list = []
        menus = sorted(self.menus,key=lambda temp:temp.id)    #sort the list data  by id   temp is menu
        for m in menus:
            if m.level==1:
                first_dict = m.to_dict_list()    # m = Menu(id=1, name='management', level=1, pid=-1)
                first_dict['children']=[]        # m = Menu(id=1, name='management', level=1, pid=-1, children=[])
                for m2 in self.menus: 
                    #test whether it is secondary menu , and pid is the same as the first_dict id
                    if m2.level==2 and m2.pid == m.id:
                        first_dict['children'].append(m2.to_dict_list())
                menu_list.append(first_dict)
        return menu_list
                

class Category(db.Model):
    __tablename__ = 't_category'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    name = db.Column(db.String(100),nullable=False)
    level = db.Column(db.Integer,default=1)
    pid = db.Column(db.Integer,db.ForeignKey('t_category.id'))   #children node's parents' id 

    children = db.relationship('Category')
    attrs = db.relationship('Attribute', backref='category')

    def to_dict(self):
        return {
            'id':self.id, 
            'name':self.name,
            'level':self.level,
            'pid':self.pid,
        }


class Attribute(db.Model):
    __tablename__='t_attribute'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32),nullable=False)
    val = db.Column(db.String(255))
    _type= db.Column(db.Enum('static','dynamic', name='attribute_type_enum'))  #a row that can just store static or dynamic this two value

    cid = db.Column(db.Integer, db.ForeignKey('t_category.id'))


    def to_dict(self):
        return {
            'id':self.id, 
            'name':self.name,
            'val':self.val,
            'type':self._type,
            'cid':self.cid,
        }    
    


class Product(db.Model):
  __tablename__ = 't_product'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(512), nullable=False)
  price = db.Column(db.Float, default=0)
  number = db.Column(db.Integer, default=0)
  introduce = db.Column(db.Text)
  big_img = db.Column(db.String(255)) 
  small_img = db.Column(db.String(255)) 
  state = db.Column(db.Integer) 
  is_promote = db.Column(db.Integer) 
  hot_number = db.Column(db.Integer) 
  weight = db.Column(db.Integer)

  cid_one = db.Column(db.Integer, db.ForeignKey('t_category.id'))
  cid_two = db.Column(db.Integer, db.ForeignKey('t_category.id'))
  cid_three = db.Column(db.Integer, db.ForeignKey('t_category.id'))

  category = db.relationship('Category', foreign_keys=[cid_three])

  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'price': self.price,
      'number': self.number,
      'introduce': self.introduce,
      'big_img': self.big_img,
      'small_img': self.small_img,
      'state': self.state,
      'is_promote': self.is_promote,
      'hot_number': self.hot_number,
      'weight': self.weight,
      'cid_one': self.cid_one,
      'cid_two': self.cid_two,
      'cid_three': self.cid_three,
      'category': [a.to_dict() for a in self.category.attrs],
     }
