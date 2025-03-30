import pandas as pd
import json
from sklearn.metrics.pairwise import cosine_similarity

def load_recipes(json_path):
    with open(json_path) as json_file:
        return json.load(json_file)
    
def get_recipes_features(recipes_data):
    features = set()
    for recipe in recipes_data["recipes"]:
        for ingredient in recipe["ingredients"]:
            features.add(ingredient["product"])
    return list(features)

def create_users_matrix(user_ids, features, sales_df):
    user_ai_df = pd.DataFrame(columns=features, index=user_ids, data=0)
    num_sales = len(sales_df.index)
    
    for line, sale in sales_df.iterrows():
        for feature in features:
            # This is the part where an LLM could intervene
            # If sale["product_dsc"] contains product string, set user to 1
            if feature in sale["product_dsc"].lower():
                user_ai_df.loc[int(sale["account_no"]), feature] += 1
        if line % 10000 == 0:
            print(f"create_users_matrix {line} / {num_sales}")

    # Non linear way of incrementing
    user_ai_df = user_ai_df.map(lambda x: 1 - (0.5 / x) if x > 0 else 0)

    return user_ai_df


def create_recipes_matrix(recipes_ids, features, recipes_data):
    item_ai_df = pd.DataFrame(columns=features, index=recipes_ids, data=0)

    for recipe_id, recipe in enumerate(recipes_data["recipes"]):
        for ingredient in recipe["ingredients"]:
            item_ai_df.loc[recipe_id, ingredient["product"]] = 1

    return item_ai_df

def create_cos_sim_matrix(users_df, recipes_df):
    cos_sim_matrix = cosine_similarity(users_df, recipes_df)
    cos_sim_df = pd.DataFrame(cos_sim_matrix, index=users_df.index, columns=recipes_df.index)
    return cos_sim_df


def compute_model(sales_csv_path, recipes_json_path):
    # Load recipes json into dict
    recipes_data = load_recipes(recipes_json_path)

    # Load sales into dataframe
    sales_df = pd.read_csv(sales_csv_path)

    # Create dataframe of users where rows are identified by usernames 
    user_ids = [int(user_id) for user_id in sales_df['account_no'].unique()]
    features = get_recipes_features(recipes_data)

    # Create users feature matrix
    user_ai_df = create_users_matrix(user_ids, features, sales_df)

    # Generate incrementing recipes ids
    recipes_ids = [id for id, _ in enumerate(recipes_data["recipes"])]
    
    # Create dataframe of items where rows are identified by item_id/sku
    recipes_ai_df = create_recipes_matrix(recipes_ids, features, recipes_data)

    # Create cosine similarity matrix
    cos_sim_df = create_cos_sim_matrix(user_ai_df, recipes_ai_df)
    # print(cos_sim_df)

    return cos_sim_df

# Return list of recommended bundle_id's
def get_recommendations(model, user_id, num_recommendations = 20):
    recommendations_similarities = model.loc[user_id].nlargest(num_recommendations)
    return list(recommendations_similarities.index)

# Vector database versions

def compute_model_db(conn, sales_csv_path, recipes_json_path):
    # Load recipes json into dict
    recipes_data = load_recipes(recipes_json_path)

    # Load sales into dataframe
    sales_df = pd.read_csv(sales_csv_path)

    # Create dataframe of users where rows are identified by usernames 
    user_ids = [int(user_id) for user_id in sales_df['account_no'].unique()]
    features = get_recipes_features(recipes_data)

    # Create users feature matrix
    user_ai_df = create_users_matrix(user_ids, features, sales_df)

    # Generate incrementing recipes ids
    recipes_ids = [id for id, _ in enumerate(recipes_data["recipes"])]
    
    # Create dataframe of items where rows are identified by item_id/sku
    recipes_ai_df = create_recipes_matrix(recipes_ids, features, recipes_data)

    # print("======== Users embeddings ========")
    print(user_ai_df.head(3))
    # print("======== Bundles embeddings ========")
    # print(recipes_ai_df)

    with conn.cursor() as cursor:
        cursor.execute("SET vector_type_project_format = JSON")
        num_users = len(user_ai_df.index)
        print("num users:", num_users)
        for idx, (username, user) in enumerate(user_ai_df.iterrows()):
            user_vec_str = f"[{', '.join(map(str, user.tolist()))}]"
            cursor.execute("INSERT IGNORE INTO users_vectors VALUES (%s, %s)", (username, user_vec_str))
            print(f"populating users_vectors {idx} / {num_users}")

        num_bundles = len(recipes_ai_df.index)
        print("num bundles:", num_bundles)
        for idx, (bundle_id, bundle) in enumerate(recipes_ai_df.iterrows()):
            bundle_vec_str = f"[{', '.join(map(str, bundle.tolist()))}]"
            cursor.execute("INSERT IGNORE INTO bundles_vectors VALUES (%s, %s)", (bundle_id, bundle_vec_str))
            print(f"populating bundles_vectors {idx} / {num_bundles}")

# Return list of recommended bundle_id's from the vector database
def get_recommendations_db(conn, user_id, num_recommendations = 20):
    with conn.cursor() as cursor:
        # Get the embedding vector of the user
        cursor.execute("SELECT * FROM users_vectors")
        rows = cursor.fetchall()
        for row in rows:
            print("ROW", row)

    return list(range(20))