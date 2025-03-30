from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from setup import *
from retrieval import *
from model import *
import json


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

        return { 'users': user }
    
class RecommendService(Resource):
    def get(self, username):
        #TODO: select best bundles for the user
        return { 'bundles': retrieve_overviews(conn, [1,2,3,4,5]) }

class BundleService(Resource):
    def get(self, username, bundle_id):
        return retrieve_bundle(conn, bundle_id)

api.add_resource(UserService, '/api/users/<string:username>')
api.add_resource(RecommendService, '/api/users/<string:username>/bundles')
api.add_resource(BundleService, '/api/users/<string:username>/bundles/<string:bundle_id>')


def populate_data(conn, recipes_path):
    try:
        with open(recipes_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        recipes = data.get("recipes", [])
        print(f"\nCarregando {len(recipes)} receitas do JSON...\n")


        with conn.cursor() as cur:
            # for bundle_id, recipe in enumerate(recipes):
            for bundle_id, recipe in enumerate(recipes, start=1):
                name = recipe["name"]
                description = recipe["description"]
                image_url = recipe["image_url"]
                instructions = "\n".join(recipe["instructions"])

                cur.execute("""
                    INSERT IGNORE INTO bundles (bundle_id, name, description, instructions, image_url)
                    VALUES (%s, %s, %s, %s, %s)
                """, (bundle_id, name, description, instructions, image_url))

                for ingr_id, ingredient in enumerate(recipe["ingredients"]):
                    product = ingredient["product"]
                    quantity = ingredient["quantity"]

                    # Verificar se o item já existe
                    # cur.execute("SELECT item_id FROM items WHERE name = %s", (product,))
                    # result = cur.fetchone()

                    # if result:
                    #     item_id = result[0]  # Se já existir, obtém o ID
                    #     print("\n\nitem_id = result[0] -> ", item_id, "\n\n")
                    # else:
                    #     # Inserir novo item na tabela `items`
                    #     # cur.execute("INSERT INTO items (name) VALUES (%s)", (product,))
                    #     item_id = cur.lastrowid
                    #     print("\n\nitem_id = cur.lastrowid -> ", item_id, "\n\n")

                    # Inserir relação na tabela `bundle_items`
                    cur.execute("""
                        INSERT IGNORE INTO bundle_items (bundle_id, ingredient, quantity)
                        VALUES (%s, %s, %s)
                    """, (bundle_id, product, quantity))


        conn.commit()
        print("✅ Base de dados populada com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao popular a base de dados: {e}")
    finally:
        conn.close()  # Garante que a conexão é fechada


if __name__ == '__main__':
    conn = connect_db()
    setup_db(conn, cleanup=False)

    # Populate database with datasets
    model = compute_model(conn, "../datasets/sample_sales_info_encripted.csv", "../datasets/recipes.json")
    bundle_ids = get_recommendations(model, 839934211079)

    app.run(host='0.0.0.0', port=5000, debug=True)
