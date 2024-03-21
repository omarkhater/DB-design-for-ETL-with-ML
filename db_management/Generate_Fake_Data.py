from helpers import *

# Generate data
N_MODELS = 5000  # Adjust based on the scale of your project
engineers = generate_engineers(10)
customers = generate_customers(50)
datasets = generate_datasets(300)
models = generate_models(N_MODELS, len(datasets), len(engineers), len(customers))
etl_scripts = generate_etl_scripts(50)
metrics1 = generate_metrics1(2000, N_MODELS)
metrics2 = generate_metrics2(2000, N_MODELS)
# Ensure ETLParameters is related to etl_scripts
etl_parameters = generate_etl_parameters(200, etl_scripts)  # Generate 200 parameters for these scripts
training = generate_training(2000, N_MODELS)

# For join tables, make sure to adjust to the range of created IDs
dataset_model = [{"DatasetID": random.randint(1, len(datasets)), "ModelID": m['ModelID']}
                 for m in random.sample(models, 600)]
engineer_model = [{"EngineerID": random.randint(1, len(engineers)), "ModelID": m['ModelID']}
                  for m in random.sample(models, 600)]
# Determine the maximum sample size based on the smaller of the two lists
max_sample_size = min(len(etl_scripts), len(training))

# Sample up to max_sample_size items from both lists
sampled_etl_scripts = random.sample(etl_scripts, max_sample_size)
sampled_training = random.sample(training, max_sample_size)  # Assuming you want to sample training as well

etl_script_to_training = [{
    "ScriptName": script['ScriptName'], 
    "ScriptVersion": script['ScriptVersion'],
    "TrainingID": t['TrainingID']
} for script, t in zip(sampled_etl_scripts, sampled_training)]

# Ensure not to sample more than the available items in the training list
sample_size = min(600, len(training))  # Choose the smaller between desired sample size and list length

dataset_to_training = [{
    "DatasetID": random.randint(1, len(datasets)),
    "TrainingID": t['TrainingID']
} for t in random.sample(training, sample_size)]


