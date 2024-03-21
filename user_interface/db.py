import psycopg2
from contextlib import contextmanager
from psycopg2 import Error
from configparser import ConfigParser
from psycopg2.extras import DictCursor

config = ConfigParser()
config.read('config.ini')

conn_params = {
    "user": config.get('database', 'user'),
    "password": config.get('database', 'password'),
    "host": config.get('database', 'host'),
    "port": config.get('database', 'port'),
}
# Assuming you have a function to get the database connection based on your environment variables
@contextmanager
def get_db_connection():
    conn = psycopg2.connect(**conn_params)
    try:
        yield conn
    finally:
        conn.close()


def insert_new_model(dataset_id, engineer_id, customer_id, description):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Model (DatasetID, EngineerID, CustomerID, Description) 
                    VALUES (%s, %s, %s, %s);
                    """, (dataset_id, engineer_id, customer_id, description))
                conn.commit()
        return True, "Model added successfully."
    except Error as e:
        return False, e.pgerror  # Or e.pgerror for PostgreSQL specific error message

def get_all_models():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Model;")
                models = cursor.fetchall()
        return models, None
    except Error as e:
        return [], e.pgerror

def execute_custom_query(query):
    results = []
    error = None
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query)
                if query.strip().upper().startswith("SELECT"):
                    # Fetch rows as dictionaries
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    for row in rows:
                        # Convert each tuple to a dictionary
                        row_dict = dict(zip(columns, row))
                        results.append(row_dict)
                else:
                    # For non-SELECT queries, perform the operation without returning results
                    conn.commit()
    except psycopg2.Error as e:
        error = str(e)
    
    return results, error
