# Database Design for Extract, Transform, Load (ETL) with Machine Learning.

This repository contains the implementation of a database design intended for ETL (Extract, Transform, Load) processes enhanced by Machine Learning (ML) solutions. This database application is designed for a fiction company specializing in providing Extract, Transform, and Load (ETL) solutions optimized by machine learning (ML) modeling techniques. Aimed at optimizing data processing workflows and enhancing predictive analytics for diverse materials data, the application facilitates the creation, tracking, and optimization of custom ML models and ETL scripts tailored to specific customer requirements.

The project is divided into two main parts: 
- `db_management` for database scripts and operations
- `user_interface` for the web interface to interact with the database.
  
## Database Design Process
---
A comprehensive guide on the database design stages including the E/R diagram design, and the relation normalization process is described [here](https://drive.google.com/file/d/1-THvLR2ViUpZy5h0Gv7GB_l9wgXHYJtZ/view?usp=sharing)

## Project Structure
```
DB-design-for-ETL-with-ML/
├── db_management/
│ ├── Generate_Fake_Data.py # Script to generate fake data for testing
│ ├── Populate_data.py # Script to populate the database with generated data
│ ├── Schema.sql # SQL schema definitions for the database
│ └── helpers.py # Helper functions for database management tasks
├── main.py # streamlit application entry point
├── app_helpers.py # Some utility helpers 
```

## db_management

This directory contains scripts and SQL definitions crucial for setting up, populating, and managing the database used in the ETL processes.

- `Generate_Fake_Data.py`: Generates fake data to simulate realistic database entries.
- `Populate_data.py`: Uses generated data to populate the database, ensuring it's ready for use.
- `Schema.sql`: Contains SQL commands to create the necessary database schema.
- `helpers.py`: Includes utility functions to assist in database management.

## user_interface

This part holds the streamlit application required for the web interface, allowing users to interact with the database.

- `main.py`: The main Flask application file that defines routes and views.
- `app_helpers.py`: Contains some helper methods to interact with the database.

## Getting Started

To get started with this project, clone the repository and navigate into the project directory:

```bash
git clone https://github.com/<your-username>/DB-design-for-ETL-with-ML.git
cd DB-design-for-ETL-with-ML
```
Then install all project dependancies using 
```
pip install -r requirments.txt
```

## Setting Up the Database

This project exploit PostgreSQL database instance hosted on Amazon RDS. Then, 

- Create the database schema using the provided `Schema.sql` file. 
- Populate the database with initial data using `Populate_data.py`.

## Running the Streamlit Application

After installing all necessary requirments, run the following command: 
```
streamlit run main.py
```
Visit [http://127.0.0.1:5000/](http://localhost:8501) in your browser to interact with the application.

