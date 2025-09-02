from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from setup_db import *
from retrieval import *
from model import *

app = Flask(__name__)
cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

conn = connect_db()

recipes_path = "../data/recipes.json"
sales_path = "../data/sample_sales_info_encripted.csv"

class UserService(Resource):
    def get(self, username):
        print("username", username)
        print("len(username)", len(username))
        user = retrieve_user(conn, username)
        return user
    
class RecommendService(Resource):
    def get(self, username):
        # Fetch recommended bundle_id's
        recommended_bundle_ids = get_recommendations_db(conn, username, num_recommendations=6)
        print("recommended_bundle_ids", recommended_bundle_ids)
        #TODO: select best bundles for the user
        return { 'bundles': retrieve_overviews(conn, recommended_bundle_ids) }

class BundleService(Resource):
    def get(self, username, bundle_id):
        return retrieve_bundle(conn, bundle_id)

api.add_resource(UserService, '/api/users/<string:username>')
api.add_resource(RecommendService, '/api/users/<string:username>/bundles')
api.add_resource(BundleService, '/api/users/<string:username>/bundles/<string:bundle_id>')

if __name__ == '__main__':
    setup_db(conn, cleanup=False)

    if os.path.exists(recipes_path) and os.path.exists(sales_path):
        model = compute_model(sales_path, recipes_path)
    else:
        print("Datasets não encontrados, ignorando criação do modelo.")
        model = None

    # model = compute_model("../data/sample_sales_info_encripted.csv", "../data/recipes.json")
    bundle_ids = get_recommendations(model, 839934211079)

    compute_model_db(conn, "../data/sample_sales_info_encripted.csv", "../data/recipes.json")
    bundle_ids = get_recommendations_db(conn, 839934211079)
    print(bundle_ids)

    app.run(host='0.0.0.0', port=5000, debug=True)
