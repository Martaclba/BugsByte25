import singlestoredb as s2

# DB_NAME = "db_marta_abaa0"
# SINGLESTOREDB_URL = "marta-1dc51:BmIJ7OrbDUA0agVkgXo0ofm34lQzIcWs@svc-3482219c-a389-4079-b18b-d50662524e8a-shared-dml.aws-virginia-6.svc.singlestore.com:3333/db_marta_abaa0"

DB_NAME = "db_jorge_dc4ac"
SINGLESTOREDB_URL = "jorge-45214:MQ2ASEdSu3amqhSxt27AznS3Z6f5Dxru@svc-3482219c-a389-4079-b18b-d50662524e8a-shared-dml.aws-virginia-6.svc.singlestore.com:3333/db_jorge_dc4ac"

def connect_db():
    conn = s2.connect(SINGLESTOREDB_URL)
    return conn

def clean_db(conn):
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS users")
        print("Deleted users table")

        # cur.execute("DROP TABLE IF EXISTS bundles")
        # print("Deleted bundles table")

        # cur.execute("DROP TABLE IF EXISTS bundle_items")
        # print("Deleted bundle_items table")

        # cur.execute("DROP TABLE IF EXISTS items")
        # print("Deleted items table")

        ##### Drop vector tables #####

        # cur.execute("DROP TABLE IF EXISTS bundles_vectors")
        # print("Deleted bundles_vectors table")

        # cur.execute("DROP TABLE IF EXISTS users_vectors")
        # print("Deleted users_vectors table")

        # print("Deleted normalize function")
        # cur.execute("DROP FUNCTION IF EXISTS normalize")

        # pass
        
        

def setup_db(conn, cleanup=False):
    if cleanup:
        clean_db(conn)
        
    with conn.cursor() as cur:
        cur.execute('USE %s' % DB_NAME)

        # Create users table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(32) PRIMARY KEY,
            name VARCHAR(64)
        )
        """)
        print("Created users table")

        # Create bundles table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS bundles (
            bundle_id INT PRIMARY KEY,
            name VARCHAR(128),
            description VARCHAR(256),
            instructions TEXT,
            image_url VARCHAR(256)
        )
        """)
        print("Created bundles table")

        # Create items table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            item_id INT PRIMARY KEY,
            name VARCHAR(64),
            image_url VARCHAR(256),
            price_index FLOAT
        )
        """)
        print("Created items table")

        # Create bundle items table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS bundle_items (
            bundle_id INT,
            ingredient VARCHAR(32),
            quantity INT,
            PRIMARY KEY (bundle_id, ingredient)
        )
        """)
        print("Created bundle items table")

        # Create vector tables
        # NOTE: For now 'embedding' vector size (num of ingredients will be hardcoded).
        #       Since we dont have the time to make it more dynamic atm.
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users_vectors(
            username VARCHAR(32) PRIMARY KEY,
            embedding VECTOR(111)
        )
        """)
        print("Created users vectors table")
        
        # NOTE: For now 'embedding' vector size (num of ingredients will be hardcoded).
        #       Since we dont have the time to make it more dynamic atm.
        cur.execute("""
        CREATE TABLE IF NOT EXISTS bundles_vectors(
            bundle_id INT PRIMARY KEY,
            embedding VECTOR(111)
        )
        """)
        print("Created users vectors table")

        cur.execute("""
            CREATE OR REPLACE FUNCTION normalize(v VECTOR(111)) RETURNS VECTOR(111) AS 
            DECLARE 
                squares VECTOR(111) = vector_mul(v,v); 
                length FLOAT = sqrt(vector_elements_sum(squares));
            BEGIN 
                RETURN scalar_vector_mul(1/length, v);
            END
        """)
        print("Created normalize function")

    return conn