import sys
import os

# 添加路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# 導入第三方庫
from flask import request
from flask_restful import Resource, reqparse

# 導入項目模塊
from category import cate_api, attr_api
from models import db
from models import Category, Attribute


class Categorys(Resource):
    def get(self):
        
        level = request.args.get('level')
        pnum = request.args.get('pnum')
        psize = request.args.get('psize')
        if level:
            level = int(level)
        else:
            level=3

            

        base_query = models.Category.query.filter(models.Category.level==1)
        if all([pnum,psize]):
            # pagination
            cates = base_query.paginate(page=int(pnum),per_page=int(psize))
        else:
            cates = base_query.all()

        cate_list = self.to_tree(cates,level)
        # for c in cates:
        #     first_dict = c.to_dict()
        #     first_dict['children']=[]
        #     #level2
        #     for sc in c.children:
        #         second_dict = sc.to_dict()
        #         second_dict['children']=[]
        #         #level 3
        #         for tc in sc.children:
        #             third_dict = tc.to_dict()
        #             second_dict['children'].append(third_dict)
        #         first_dict['children'].append(second_dict)

        #     cate_list.append(first_dict)
        return {'status':200,'msg':'get the category successfully','data':cate_list} 
    def to_tree(self,info:list,level):
        info_list=[]
        for i in info:
            i_dict = i.to_dict()
            if i.level<level:
                i_dict['children']=self.to_tree(i.children,level)
            info_list.append(i_dict)
        return info_list



    def post(self):
        try:
            parser = reqparse.RequestParser()

            parser.add_argument('name',type=str,required=True)
            parser.add_argument('level', type=int, required=True)
            parser.add_argument('pid', type=int)

            args = parser.parse_args()
            #test whether it has pid
            if args.get('pid'):
                c = models.Category(name=args.get('name'),level=args.get('level'),pid=args.get('pid'))
            else:
                c = models.Category(name=args.get('name'),level=args.get('level'))
            
            db.session.add(c)
            db.session.commit()
            return {'status':200,'msg':'Category added successfully'}
        
        except Exception as e:
            print(e)
            return{'status':500,'msg':'failed to add category'}
        
cate_api.add_resource(Categorys,'/categorys/')



class Attributes(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cid',type=int,required=True,location='args')   #location=args here to show that we are using url to get the cid
        parser.add_argument('_type',type=str,required=True,location='args')

        args = parser.parse_args()
        cate = models.Category.query.get(args.get('cid'))
        attrs_list=[]
        if args.get('_type') == 'static':
            attrs_list = [a.to_dict() for a in cate.attrs if a._type == 'static']
        elif args.get('_type') == 'dynamic':
            attrs_list = [a.to_dict() for a in cate.attrs if a._type == 'dynamic']

        return {'status':200,'msg':'got the attribution successfully','data':attrs_list}
    

    def post(self):     #add resource
        try:
            parser = reqparse.RequestParser()

            parser.add_argument('name',type=str,required=True)   #it defaults to find the data from content json  so we do not need to add lcoation
            parser.add_argument('val',type=str)
            parser.add_argument('_type',type=str)
            parser.add_argument('cid',type=int,required=True)

            args = parser.parse_args()

            if args.get('val'):
                c = models.Attribute(name=args.get('name'),val=args.get('val'),_type=args.get('_type'),cid=args.get('cid'))
            else:
                c = models.Attribute(name=args.get('name'),_type=args.get('_type'),cid=args.get('cid'))

            db.session.add(c)
            db.session.commit()

            return{'status':200,'msg':'add the attribute successfully'}
        
        except Exception as e:
            print(e)
            return {'status':500,'msg':'failed to add attribute'}
        
attr_api.add_resource(Attributes,'/attributes/')



class Attribute(Resource):     #inividual
    def get(self,id):
        try:
            attr = models.Attribute.query.get(id)
            return{'static':200,'msg':'got the attribute successfully','data':attr.to_dict()}
        
        except Exception as e:
            print(e)
            return{'status':500,'msg':'failed to get the attribute'}
        
    def put(self,id):
        try:
            attr = models.Attribute.query.get(id)
            parser = reqparse.RequestParser()

            parser.add_argument('name',type=str)
            parser.add_argument('val',type=str)
            parser.add_argument('_type',type=str)
            parser.add_argument('cid',type=int) 

            args = parser.parse_args()
            if args.get('name'):
                attr.name = args.get('name')
            if args.get('val'):
                attr.val = args.get('val')
            if args.get('_type'):
                attr._type = args.get('_type')
            if args.get('cid'):
                attr.cid = args.get('cid')

            db.session.commit()
            return{'status':200,'msg':'edit the attribution successfully '}
        
        except Exception as e:
            print(e)
            return {'status':500,'msg':'failed to edit the attribution'}
    def delete(self,id):
        try:
            attr = models.Attribute.query.get(id)

            db.session.delete(attr)
            db.session.commit()
            return{'status':200,'msg':'delete the attribution successfully'}
        except Exception as e:
            print(e)
            return{'status':500,'msg':'failed to delete the attribution'}
        
attr_api.add_resource(Attribute,'/attribute/<int:id>/')        