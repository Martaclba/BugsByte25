from flask import Flask
from flask_restful import Resource, Api
from setup import *
from model import *


app = Flask(__name__)
api = Api(app)

class UserService(Resource):
    def get(self, username):
        user = {
            'username': "paulo_figueira",
            'name': "Paulo Figueira",
        }

        return { 'users': users }
    
class RecommendService(Resource):
    def get(self, username):
        bundles = [{
            "bundle_id": 1,
            "title": "This is a title",
            "description": "...",
            "instructions":  "...",
            "items": [
                {
                    "item_id": 2,
                    "quantity": 1,
                    "product": "acucar",
                    "image_url": "...",
                },
                {
                    "item_id": 3,
                    "quantity": 2,
                    "product": "farinha",
                    "image_url": "...",
                },
            ]
        }]
    
        return { 'bundles': bundles }

class BundleService(Resource):
    def get(self, username):
        bundle_recommendation = {
            "bundle_id": 1, 
            "title": "...",
            "start_date": "...",
            "end_date": "...",
            "description": "...",
            "instructions":  "...",
            "items": [
                {
                    "quantity": 1,
                    "product": "acucar",
                    "image_url": "...",
                },
                ...
            ]
        }
    
        return bundle_recommendation

api.add_resource(UserService, '/api/users/<string:username>')
api.add_resource(RecommendService, '/api/users/<string:username>/bundles')
api.add_resource(BundleService, '/api/users/<string:username>/bundles/<string:bundle_id>')

if __name__ == '__main__':
    
    # Load and compute model, 
    #load_model("datasets/sample_prod_info.csv")
    
    conn = connect_db()
    setup_db(conn, cleanup=True)

    populate_users(conn, "datasets/sample_sales_info_encripted.csv")


    app.run(host='0.0.0.0', port=5000, debug=True)
