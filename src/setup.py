import singlestoredb as s2

DB_NAME = "db_jorge_dc4ac"
SINGLESTOREDB_URL = "jorge-45214:MQ2ASEdSu3amqhSxt27AznS3Z6f5Dxru@svc-3482219c-a389-4079-b18b-d50662524e8a-shared-dml.aws-virginia-6.svc.singlestore.com:3333/db_jorge_dc4ac"

conn = s2.connect(SINGLESTOREDB_URL)

def setup_db():
    with conn.cursor() as cur:
        cur.execute('USE %s' % DB_NAME)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(32) UNIQUE PRIMARY KEY,
            name VARCHAR(64)
        )
        """)
        print("Created users table")