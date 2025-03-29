from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
#from setup import *
#from model import *


app = Flask(__name__)
cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

class UserService(Resource):
    def get(self, username):
        user = {
            'username': "paulo_figueira",
            'name': "Paulo Figueira",
        }

        return user
    
class RecommendService(Resource):
    def get(self, username):
        bundles = [{
            "bundle_id": 1,
            "title": "This is a title",
            "description": "This description describes the described bundle",
            "image_url": "https://www.noracooks.com/vegan-cheddar-cheese/",
        }]
    
        return { 'bundles': bundles }

class BundleService(Resource):
    def get(self, username, bundle_id):
        bundle_recommendation = {
            "bundle_id": 1, 
            "title": "This is a title",
            "start_date": "01/08/2003",
            "end_date": "01/08/2083",
            "description": "This description describes the described bundle",
            "instructions":  "These instructions instruct the user how to use the products of the bundle",
            "image_url": "/receita.jpg",
            "items": [
                {
                    "quantity": 1,
                    "product": {
                        "product_id": "9876",
                        "name": "acucar",
                        "base_price": 1.23,
                        "price": 0.99,
                        "image_url": "/receita.jpg",
                    },
                },{
                    "item_id": 3,
                    "quantity": 2,
                    "product": {
                        "product_id": "9879",
                        "name": "farinha",
                        "base_price": 1.23,
                        "price": 1.23,
                        "image_url": "/receita.jpg",
                    },
                },
            ]
        }
    
        return bundle_recommendation

api.add_resource(UserService, '/api/users/<string:username>')
api.add_resource(RecommendService, '/api/users/<string:username>/bundles')
api.add_resource(BundleService, '/api/users/<string:username>/bundles/<string:bundle_id>')

if __name__ == '__main__':
    
    # Load and compute model, 
    #load_model("datasets/sample_prod_info.csv")
    
    #conn = connect_db()
    #setup_db(conn, cleanup=True)

    #populate_users(conn, "datasets/sample_sales_info_encripted.csv")


    app.run(host='0.0.0.0', port=5000, debug=True)
