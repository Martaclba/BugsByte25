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
    
    # TODO: Remove head to work with all data
    for line, sale in sales_df.head(10000).iterrows():
        for feature in features:
            # This is the part where an LLM could intervene
            # If sale["product_dsc"] contains product string, set user to 1
            if feature in sale["product_dsc"].lower():
                user_ai_df.loc[int(sale["account_no"]), feature] += 1

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


def compute_model(conn, sales_csv_path, recipes_json_path):

    ######## Compute model ########
    
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
    print(cos_sim_df)

    ######## Store model in vectordatabase ########

    with conn.cursor() as cursor:
        cursor.execute("SET vector_type_project_format = JSON;")
        # cursor.execute()

    return cos_sim_df


# TODO: Once this is working, implement this but with singlestore vector database
# Return list of recommended bundle_id's
def get_recommendations(model, user_id, num_recommendations = 20):
    recommendations_similarities = model.loc[user_id].nlargest(num_recommendations)
    return list(recommendations_similarities.index)