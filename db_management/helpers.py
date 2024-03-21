from faker import Faker
import random

fake = Faker()
# 1
def generate_engineers(n):
    return [
        {
            "EngineerID": i,
            "FirstName": fake.first_name(),
            "LastName": fake.last_name(),
            "Email": fake.unique.email(),
            "Phone": fake.phone_number(),
            "Role": random.choice(["Data Engineer", "Machine Learning Engineer", "Software Engineer", 'Data Scientist'])
        } for i in range(1, n+1)
    ]
# 2
def generate_metrics1(n, model_range):
    metrics_list = ["Accuracy", "Precision", "Recall", "F1-Score", "R2", "RMSE", "Bias"]
    return [
        {
            "MetricID": i,
            "ModelID": random.randint(1, model_range),
            "MetricName": random.choice(metrics_list),
        } for i in range(1, n+1)
    ]
# 3
def generate_metrics2(n, model_range):
    metrics_list = ["Accuracy", "Precision", "Recall", "F1-Score", "R2", "RMSE", "Bias"]
    return [
        {
            "ModelID": random.randint(1, model_range),
            "MetricName": random.choice(metrics_list),
            "MetricValue": round(random.uniform(0, 1), 4)  # Adding MetricValue directly to metrics1 for simplicity
        } for i in range(1, n+1)
    ]
# 4
def generate_customers(n):
    return [
        {
            "CustomerID": i,
            "Name": fake.company(),
            "Contact": fake.phone_number(),
            "Priority": random.randint(1, 3)
        } for i in range(1, n+1)
    ]
# 5
def generate_datasets(n):
    return [
        {
            "DatasetID": i,
            "Material": random.choice(["Plastic", "Metal", "Glass"]),
            "CollectionDate": fake.date(),
            "DataDescription": fake.text(max_nb_chars=200)
        } for i in range(1, n+1)
    ]
# 6
def generate_models(n, dataset_range, engineer_range, customer_range):
    return [
        {
            "ModelID": i,
            "DatasetID": random.randint(1, dataset_range),
            "EngineerID": random.randint(1, engineer_range),
            "CustomerID": random.randint(1, customer_range),
            "Description": fake.text(max_nb_chars=200)
        } for i in range(1, n+1)
    ]
# 7
def generate_etl_scripts(n):
    return [
        {
            "ScriptName": fake.word(),
            "ScriptVersion": random.choice(["1.0", "1.1", "2.0"]),
            "Description": fake.sentence()
        } for _ in range(n)
    ]
# 8
def generate_training(n, model_range):
    algorithms = ["Linear Regression", "Random Forest", "SVM"]
    return [
        {
            "TrainingID": i,
            "ModelID": random.randint(1, model_range),
            "X_Preprocessing": random.choice(["StandardScaler", "MinMaxScaler"]),
            "Y_preprocessing": random.choice(["LogTransform", "None"]),
            "Algorithm": random.choice(algorithms)
        } for i in range(1, n+1)
    ]
# 9
def generate_dataset_model(n, dataset_range, model_range):
    return [
        {
            "DatasetID": random.randint(1, dataset_range),
            "ModelID": random.randint(1, model_range)
        } for _ in range(n)
    ]
# 10
def generate_engineer_model(n, engineer_range, model_range):
    return [
        {
            "EngineerID": random.randint(1, engineer_range),
            "ModelID": random.randint(1, model_range)
        } for _ in range(n)
    ]
# 11
def generate_etl_script_to_training(n, training_range):
    return [
        {
            "ScriptName": fake.word(),  # Note: This assumes script names can be non-unique. Adjust if necessary.
            "ScriptVersion": random.choice(["1.0", "1.1", "2.0"]),
            "TrainingID": random.randint(1, training_range)
        } for _ in range(n)
    ]
# 12
def generate_dataset_to_training(n, dataset_range, training_range):
    return [
        {
            "DatasetID": random.randint(1, dataset_range),
            "TrainingID": random.randint(1, training_range)
        } for _ in range(n)
    ]

def generate_etl_parameters(n, etl_scripts):
    parameters = []
    for i in range(1, n+1):
        chosen_script = random.choice(etl_scripts)  # Pick a random script from the generated list
        parameter = {
            "ParameterID": i,
            "ParameterName": fake.word(),
            "ScriptName": chosen_script['ScriptName'],  # Use the script name from the chosen script
            "ScriptVersion": chosen_script['ScriptVersion'],  # Use the script version from the chosen script
            "ParameterValue": fake.word()
        }
        parameters.append(parameter)
    return parameters
