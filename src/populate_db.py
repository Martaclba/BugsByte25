from setup_db import *
import pandas as pd
import json
from model import *

def populate_with_users(conn, users_df):
    with conn.cursor() as cursor:
        print("Gonna insert", len(users_df['account_no'].unique()), "users")
        for line, account_no in enumerate(users_df['account_no'].unique()):
            cursor.execute("""
                INSERT IGNORE INTO users (username, name)
                VALUES (%s, "Default Name")
                """,
                (account_no)
            )
            print(line)

def populate_with_bundles(conn, recipes_path):
    try:
        with open(recipes_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        recipes = data.get("recipes", [])
        print(f"Loading bundles {len(recipes)} from json ...\n")

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


        # FIXME: Im pretty sure this is not needed since the 'raii-like' python with statement does this commit when out of scope
        # only remove/test this when theres time
        conn.commit()
        print("Populated with bundles")

    except Exception as e:
        print(f"❌ Erro ao popular a base de dados: {e}")
    finally:
        conn.close()  # Garante que a conexão é fechada


if __name__ == '__main__':
    conn = connect_db()
    setup_db(conn, cleanup=False)

    sales_df = pd.read_csv("../datasets/sample_sales_info_encripted.csv")
    # items_df = pd.read_csv("../datasets/sample_prod_info.csv")

    # Populate with users
    print("Populating database with users")
    # populate_with_users(conn, sales_df)
    
    # Populate with bundles and blunde items
    print("Populating database with bundles")
    # populate_with_bundles(conn, "recipes.json")

    # Populate with items
    print("Populating database with items data")
    # TODO:

    # Populate vector tables with model
    compute_model_db(conn, "../datasets/sample_sales_info_encripted.csv", "../datasets/recipes.json")