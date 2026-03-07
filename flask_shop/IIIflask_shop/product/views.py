import sys
import os

# 添加路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# 導入第三方庫
from flask import request, jsonify
from flask_restful import Resource, reqparse

# 導入項目模塊
from product import product_api
from models import db
from models import Product 


class Products(Resource):
    def get(self):
        'search product list for blur'
        parser = reqparse.RequestParser()

        parser.add_argument('name',type=str,location='args')

        args = parser.parse_args()

        name = args.get('name')

        if name:
            product_list = models.Product.query.filter(models.Product.name.like(f'%{name}%')).all()
        else:
            product_list = models.Product.query.all()
        return{
            'status':200,
            'msg':'got the product list successfully',
            'data':[i.to_dict() for i in product_list]

        }

product_api.add_resource(Products,'/products/')


class Product(Resource):
    def delete(self,id):
        try:
            product = models.Product.query.get(id)
            db.session.delete(product)
            db.session.commit()
            return {'status':200,'msg':"delete the product successfully"}

        except Exception as e:
            return {
                'status':500,
                'msg':'fail to delete',

            }
product_api.add_resource(Product,'/product/<int:id>/')