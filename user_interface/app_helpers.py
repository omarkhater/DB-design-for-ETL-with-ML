import psycopg2
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from configparser import ConfigParser
# Function to build the schema dynamically from the database
            
config = ConfigParser()
config.read('../config.ini')

conn_params = {
    "user": config.get('database', 'user'),
    "password": config.get('database', 'password'),
    "host": config.get('database', 'host'),
    "port": config.get('database', 'port'),
}

def build_table_schemas():
    query = """
    SELECT table_name, column_name
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position;
    """
    df_schema = fetch_data(query)
    table_schemas = {}
    for index, row in df_schema.iterrows():
        if row['table_name'] in table_schemas:
            table_schemas[row['table_name']].append(row['column_name'])
        else:
            table_schemas[row['table_name']] = [row['column_name']]
    return table_schemas

# Generic function to insert data into any table
def insert_data(table, data):
    conn = create_db_connection()
    if conn is not None:
        cur = conn.cursor()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders});"
        try:
            cur.execute(query, list(data.values()))
            conn.commit()
            st.success("Data added successfully.")
        except psycopg2.Error as e:
            st.error(f"Error inserting data into table {table}: {e}")
        finally:
            cur.close()
            conn.close()

# Function to create database connection
def create_db_connection():
    try:
        conn = psycopg2.connect(**conn_params)
        return conn
    except psycopg2.Error as e:
        st.error(f"Error connecting to PostgreSQL database: {e}")
        return None

# Function to fetch data from the database
def fetch_data(query):
    conn = create_db_connection()
    if conn is not None:
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    else:
        return pd.DataFrame()

def plot_engineer_productivity():
    query = """
    SELECT engineerid, COUNT(modelid) AS model_count
    FROM engineermodel
    GROUP BY engineerid
    ORDER BY model_count DESC;
    """
    df = fetch_data(query)
    if not df.empty:
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x='engineerid', y='model_count')
        plt.title('Engineer Productivity Trends')
        plt.xlabel('Engineer ID')
        plt.ylabel('Number of Models Developed')
        st.pyplot(plt)
    else:
        st.info("No data available for this analysis.")

def plot_customer_project_volume():
    query = """
    SELECT customerid, COUNT(*) AS model_count
    FROM Model
    GROUP BY customerid
    ORDER BY model_count DESC;
    """
    df = fetch_data(query)
    if not df.empty:
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x='customerid', y='model_count')
        plt.title('Customer Project Volume')
        plt.xlabel('Customer ID')
        plt.ylabel('Number of Models Developed')
        st.pyplot(plt)
    else:
        st.info("No data available for this analysis.")
        
def execute_query(query, select=True):
    conn = create_db_connection()
    if conn is not None:
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                if select:
                    df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
                    return df
                else:
                    conn.commit()  # Commit to save the changes for non-select queries
            if not select:
                return "Query executed successfully."
        except Exception as e:
            return f"Failed to execute query: {e}"
        finally:
            conn.close()
    else:
        return "Connection to database failed."
    
def get_table_columns(table_name):
    query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' AND table_schema = 'public';"
    df = execute_query(query)
    if not df.empty:
        return df['column_name'].tolist()
    else:
        return []