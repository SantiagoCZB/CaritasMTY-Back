import pymssql

def get_db_connection():
    try:
        conn = pymssql.connect(
            server='10.14.255.65',
            user='SA',
            password='Shakira123.',
            database='Caritas-DB'
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None