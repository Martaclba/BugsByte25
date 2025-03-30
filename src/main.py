from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from setup import *
#from model import *
from retrieval import *


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
        #TODO: select best bundles for the user
        return { 'bundles': retrieve_overviews(conn, ["1", "2", "3", "4", "5"]) }

class BundleService(Resource):
    def get(self, username, bundle_id):
        return retrieve_bundle(conn, bundle_id)

api.add_resource(UserService, '/api/users/<string:username>')
api.add_resource(RecommendService, '/api/users/<string:username>/bundles')
api.add_resource(BundleService, '/api/users/<string:username>/bundles/<string:bundle_id>')

if __name__ == '__main__':
    
    # Load and compute model, 
    #load_model("datasets/sample_prod_info.csv")
    
    conn = connect_db()
    setup_db(conn, cleanup=False)

    #populate_users(conn, "datasets/sample_sales_info_encripted.csv")
    #print(retrieve(conn, ["1", "2"]))

    app.run(host='0.0.0.0', port=5000, debug=True)
