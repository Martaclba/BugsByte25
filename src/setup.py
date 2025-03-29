import singlestoredb as s2

DB_NAME = "db_jorge_dc4ac"
SINGLESTOREDB_URL = "jorge-45214:MQ2ASEdSu3amqhSxt27AznS3Z6f5Dxru@svc-3482219c-a389-4079-b18b-d50662524e8a-shared-dml.aws-virginia-6.svc.singlestore.com:3333/db_jorge_dc4ac"

def connect_db():
    conn = s2.connect(SINGLESTOREDB_URL)
    return conn

def clean_db(conn):
    with conn.cursor() as cur:
        print("Deleted users table")
        cur.execute("DROP TABLE IF EXISTS users")
        print("Deleted bundles table")
        cur.execute("DROP TABLE IF EXISTS bundles")
        print("Deleted items table")
        cur.execute("DROP TABLE IF EXISTS items")
        print("Deleted bundle_items table")
        cur.execute("DROP TABLE IF EXISTS bundle_items")

def setup_db(conn, cleanup=False):
    if cleanup:
        clean_db(conn)
        
    with conn.cursor() as cur:
        cur.execute('USE %s' % DB_NAME)

        # Create users table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(32) UNIQUE PRIMARY KEY,
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
            image_url VARCHAR(256)
        )
        """)
        print("Created items table")

        # Create bundle items table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS bundle_items (
            bundle_id INT PRIMARY KEY,
            ingredient VARCHAR(32),
            quantity INT
        )
        """)
        print("Created bundle items table")
    return conn


