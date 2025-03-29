import pandas as pd

def populate_users(conn, sales_csv_path):
    # # Execute the insert query
    # cursor.execute("""
    #     INSERT INTO users (username, name)
    #     VALUES (. "Default Name")
    #     """,
    #     ()
    # )
    
    users_df = pd.read_csv(path)
    print(users_df)

    # Commit the transaction
    conn.commit()