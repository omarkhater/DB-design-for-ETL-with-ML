import psycopg2
from Generate_Fake_Data import *
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

db_config = {
    "user": config.get('database', 'user'),
    "password": config.get('database', 'password'),
    "host": config.get('database', 'host'),
    "port": config.get('database', 'port'),
}

def run_schema_creation(conn, schema_file_path):
    cur = conn.cursor()
    with open(schema_file_path, 'r') as file:
        schema_sql = file.read()
        # Assuming that SQL commands are separated by semicolons,
        # and there are no semicolons within the commands themselves
        commands = schema_sql.split(';')
        for command in commands:
            if command.strip():  # Ensure the command is not empty
                cur.execute(command)
    conn.commit()
    cur.close()

def insert_data(conn, data, query, table_name):
    print(f"Inserting data into {table_name} table...")
    try:
        cur = conn.cursor()
        for item in data:
            cur.execute(query, item)
        conn.commit()
        cur.close()
        print("Data inserted successfully!")
    except Exception as e:
        print(f"Error inserting data into {table_name} table: {e}")
    return
def main(create_schema = False):

    # Establish database connection
    schema_file_path = 'Schema.sql'
    conn = psycopg2.connect(**db_config)
    if create_schema:
        print(f"Creating schema from {schema_file_path}")
        run_schema_creation(conn, schema_file_path)
        print("Schema created successfully!")
    
    # Table insert queries and data
    table_operations = [
        (engineers, "INSERT INTO Engineer (EngineerID, FirstName, LastName, Email, Phone, Role) VALUES (%(EngineerID)s, %(FirstName)s, %(LastName)s, %(Email)s, %(Phone)s, %(Role)s)", "Engineer"),
        (customers, "INSERT INTO Customers (CustomerID, Name, Contact, Priority) VALUES (%(CustomerID)s, %(Name)s, %(Contact)s, %(Priority)s)", "Customers"),
        (datasets, "INSERT INTO Dataset (DatasetID, Material, CollectionDate, DataDescription) VALUES (%(DatasetID)s, %(Material)s, %(CollectionDate)s, %(DataDescription)s)", "Dataset"),
        (models, "INSERT INTO Model (ModelID, DatasetID, EngineerID, CustomerID, Description) VALUES (%(ModelID)s, %(DatasetID)s, %(EngineerID)s, %(CustomerID)s, %(Description)s)", "Model"),
        (etl_scripts, "INSERT INTO ETLScript (ScriptName, ScriptVersion, Description) VALUES (%(ScriptName)s, %(ScriptVersion)s, %(Description)s)", "ETLScript"),
        (etl_parameters, "INSERT INTO ETLParameters (ParameterID, ParameterName, ScriptName, ScriptVersion, ParameterValue) VALUES (%(ParameterID)s, %(ParameterName)s, %(ScriptName)s, %(ScriptVersion)s, %(ParameterValue)s)", "ETLParameters"),
        (training, "INSERT INTO Training (TrainingID, ModelID, X_Preprocessing, Y_preprocessing, Algorithm) VALUES (%(TrainingID)s, %(ModelID)s, %(X_Preprocessing)s, %(Y_preprocessing)s, %(Algorithm)s)", "Training"),
        (dataset_model, "INSERT INTO DatasetModel (DatasetID, ModelID) VALUES (%(DatasetID)s, %(ModelID)s)", "DatasetModel"),
        (engineer_model, "INSERT INTO EngineerModel (EngineerID, ModelID) VALUES (%(EngineerID)s, %(ModelID)s)", "EngineerModel"),
        (etl_script_to_training, "INSERT INTO ETLScriptToTraining (ScriptName, ScriptVersion, TrainingID) VALUES (%(ScriptName)s, %(ScriptVersion)s, %(TrainingID)s)", "ETLScriptToTraining"),
        (dataset_to_training, "INSERT INTO DatasetToTraining (DatasetID, TrainingID) VALUES (%(DatasetID)s, %(TrainingID)s)", "DatasetToTraining"),
        # New entries for Metrics1 and Metrics2, ensuring they follow the structure
        (metrics1, "INSERT INTO Metrics1 (MetricID, ModelID, MetricName) VALUES (%(MetricID)s, %(ModelID)s, %(MetricName)s)", "Metrics1"),
        (metrics2, "INSERT INTO Metrics2 (ModelID, MetricName, MetricValue) VALUES (%(ModelID)s, %(MetricName)s, %(MetricValue)s)", "Metrics2"),
    ]


    # Execute insertion for each table
    for data, query, table_name in table_operations:
        insert_data(conn, data, query, table_name)
    # Close the connection
    conn.close()

if __name__ == "__main__":
    main(create_schema = True)
