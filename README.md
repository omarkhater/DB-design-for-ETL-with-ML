# DB Design for ETL with ML

This repository contains the implementation of a database design intended for ETL (Extract, Transform, Load) processes enhanced by Machine Learning (ML) functionalities. The project is divided into two main directories: `db_management` for database scripts and operations, and `user_interface` for the web interface to interact with the database.

## Project Structure
```
DB-design-for-ETL-with-ML/
├── db_management/
│ ├── Generate_Fake_Data.py # Script to generate fake data for testing
│ ├── Populate_data.py # Script to populate the database with generated data
│ ├── Schema.sql # SQL schema definitions for the database
│ └── helpers.py # Helper functions for database management tasks
│
└── user_interface/
├── app.py # Flask application entry point
├── db.py # Database interaction functions for the Flask app
└── templates/ # HTML templates for the web interface
├── home.html # Home page template
├── add_model.html # Template for adding new models
└── list_models.html # Template for listing all models
```

## db_management

This directory contains scripts and SQL definitions crucial for setting up, populating, and managing the database used in the ETL processes.

- `Generate_Fake_Data.py`: Generates fake data to simulate realistic database entries.
- `Populate_data.py`: Uses generated data to populate the database, ensuring it's ready for use.
- `Schema.sql`: Contains SQL commands to create the necessary database schema.
- `helpers.py`: Includes utility functions to assist in database management.

## user_interface

This directory holds the Flask application and templates required for the web interface, allowing users to interact with the database.

- `app.py`: The main Flask application file that defines routes and views.
- `db.py`: Contains functions that the Flask app uses to interact with the database.
- `templates/`: Stores HTML templates for the web interface.
  - `home.html`: The landing page providing an overview and links to other functionalities.
  - `add_model.html`: A form for adding new ML models to the database.
  - `list_models.html`: Displays a list of all models currently stored in the database.

## Getting Started

To get started with this project, clone the repository and navigate into the project directory:

```bash
git clone https://github.com/<your-username>/DB-design-for-ETL-with-ML.git
cd DB-design-for-ETL-with-ML
```

## Setting Up the Database
Create your database using the provided `Schema.sql` file.
Populate the database with initial data using `Populate_data.py`.

## Running the Flask Application

Ensure you have Flask installed, and then run `app.py` from the user_interface directory:

cd user_interface
flask run

Visit http://127.0.0.1:5000/ in your browser to interact with the application.

