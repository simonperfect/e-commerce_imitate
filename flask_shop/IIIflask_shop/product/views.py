from flask_restful import Resource,reqparse

from IIIflask_shop import models
from IIIflask_shop.product import product_api
from IIIflask_shop import db



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