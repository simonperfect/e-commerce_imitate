import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from flask import request, current_app
from flask_restful import Resource, reqparse

from product import product_api
from extensions import db

# 不要在模塊級別導入 Product，而是在函數內部導入
class Products(Resource):
    def get(self):
        'search product list for blur'
        
        # 在應用上下文中導入和使用
        with current_app.app_context():
            from models import Product
            
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, location='args')
            args = parser.parse_args()
            name = args.get('name')
            
            if name:
                product_list = Product.query.filter(Product.name.like(f'%{name}%')).all()
            else:
                product_list = Product.query.all()
            
            return {
                'status': 200,
                'msg': 'got the product list successfully',
                'data': [i.to_dict() for i in product_list]
            }

product_api.add_resource(Products, '/products/')

class Product(Resource):
    def delete(self, id):
        try:
            with current_app.app_context():
                from models import Product
                product = Product.query.get(id)
                db.session.delete(product)
                db.session.commit()
                return {'status': 200, 'msg': "delete the product successfully"}
        except Exception as e:
            return {'status': 500, 'msg': 'fail to delete'}

product_api.add_resource(Product, '/product/<int:id>/')