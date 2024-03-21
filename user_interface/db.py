import psycopg2
from contextlib import contextmanager
from psycopg2 import Error
from configparser import ConfigParser

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

