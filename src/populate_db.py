from setup import *
import pandas as pd

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



if __name__ == '__main__':
    conn = connect_db()
    setup_db(conn)

    sales_df = pd.read_csv("../datasets/sample_sales_info_encripted.csv")
    # items_df = pd.read_csv("../datasets/sample_prod_info.csv")

    # Populate with users
    print("Populating database with users")
    populate_with_users(conn, sales_df)
    
    # Populate with bundles and blunde items
    print("Populating database with bundles")
    populate_with_users()

    # Populate with items
    print("Populating database with items data")
    # TODO: