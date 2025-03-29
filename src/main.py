from flask import Flask
from flask_restful import Resource, Api
from setup import setup_db


app = Flask(__name__)
api = Api(app)

class BundlesService(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(BundlesService, '/')

if __name__ == '__main__':
    with conn:
        setup_db(conn)

    app.run(host='0.0.0.0', port=5000, debug=True)
