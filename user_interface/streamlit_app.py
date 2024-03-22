import streamlit as st
from app_helpers import (
    build_table_schemas,fetch_data, plot_engineer_productivity, 
    plot_customer_project_volume, get_table_columns, execute_query, 
    insert_data
    )
def main():
    
    table_schemas = build_table_schemas()

    st.sidebar.title("Database Operations")
    options = ["About", "Visualize Data", "Add Data", "Top N Engineers by Models Developed", "Data Insights and Trends",
               "QueryMe!", "Drop Data", "Quit"]
    action = st.sidebar.selectbox("Select an action:", options)


    if action == "About":
        st.title("About This Project")
        st.markdown("""
        ### Application Goal

        This project is designed to offer a comprehensive suite of tools for 
        managing and analyzing data within a database, tailored specifically 
        for a company specializing in ETL solutions and machine learning modeling. 
        It aims to enhance productivity, data management, and insight generation through a user-friendly interface.
        
        ### Features Overview

        - **Visualize Data**: Explore and visualize data from different tables in the database, providing insights into the stored information.

        - **Add Data**: Easily add new records to any table in the database, facilitating the expansion of the dataset with new information.

        - **Top N Engineers by Models Developed**: Discover the most productive engineers based on the number of models they've contributed to, highlighting key performers.

        - **Data Insights and Trends**: Gain valuable insights and identify trends across various datasets, including model performance, engineer productivity, and more.

        - **QueryMe!**: Execute custom queries on the database for flexible data exploration and analysis. This feature offers powerful insights tailored to specific user queries.

        - **Drop Data**: Carefully remove data from the database based on specific criteria, providing controlled management of stored information.

        - **Quit**: Exit the application safely.
        """
        )
        
    elif action == "Visualize Data":
        st.title("Visualize Data")
        table_name = st.selectbox("Select a table to visualize:", list(table_schemas.keys()))
        query = f"SELECT * FROM {table_name};"
        df = fetch_data(query)
        st.dataframe(df)

    elif action == "Add Data":
        st.title("Add Data")
        table_name = st.selectbox("Select a table to add data:", list(table_schemas.keys()))
        
        # Dynamically generate form based on table schema
        with st.form(key=f"{table_name}Form"):
            data = {}
            for field in table_schemas[table_name]:
                data[field] = st.text_input(f"{field}", key=f"{field}")
            
            submit_button = st.form_submit_button(label="Submit")
            if submit_button:
                # Filter out fields that were not filled
                data = {key: value for key, value in data.items() if value}
                insert_data(table_name, data)

    elif action == "Average Model Performance Metrics":
        query = """
        SELECT modelid, AVG(value) as avg_value
        FROM metrics1
        GROUP BY modelid;
        """
        df = fetch_data(query)
        st.title("Average Model Performance Metrics")
        st.dataframe(df)

    elif action == "Top N Engineers by Models Developed":
        n = st.sidebar.number_input("Enter N:", min_value=1, value=5)
        query = f"""
        SELECT engineerid, COUNT(modelid) as models_count
        FROM engineermodel
        GROUP BY engineerid
        ORDER BY models_count DESC
        LIMIT {n};
        """
        df = fetch_data(query)
        st.title(f"Top {n} Engineers by Models Developed")
        st.dataframe(df)

    elif action == "Customer Prioritization":
        query = """
        SELECT c.id, c.name, COUNT(m.id) as models_count, c.priority_level
        FROM customers c
        JOIN Model m ON c.id = m.customerid
        GROUP BY c.id
        ORDER BY c.priority_level DESC, models_count DESC;
        """
        df = fetch_data(query)
        st.title("Customer Prioritization by Models Developed")
        st.dataframe(df)

    elif action == "Comparison of Dataset Sizes":
        size = st.sidebar.number_input("Enter size (in MB):", min_value=0, value=100)
        query = f"""
        SELECT * FROM Dataset
        WHERE size > {size};
        """
        df = fetch_data(query)
        st.title(f"Datasets Larger Than {size} MB")
        st.dataframe(df)

    elif action == "Models without Training Data":
        query = """
        SELECT m.id, m.description
        FROM Model m
        LEFT JOIN Training t ON m.id = t.model_id
        WHERE t.model_id IS NULL;
        """
        df = fetch_data(query)
        st.title("Models without Associated Training Data")
        st.dataframe(df)
    
    elif action == "QueryMe!":
        st.title("Custom SQL Query")
        query = st.text_area("Write your SQL query here:", height=150)
        execute_button = st.button("Execute")
        
        if execute_button and query:
            try:
                df = fetch_data(query)
                if not df.empty:
                    st.dataframe(df)
                else:
                    st.info("Query executed successfully, but no data was returned.")
            except Exception as e:
                st.error(f"Failed to execute query: {str(e)}")
                
            
    elif action == "Data Insights and Trends":
        st.title("Data Insights and Trends")
        analysis_type = st.selectbox("Select Analysis Type", ["Engineer Productivity Trends", "Customer Project Volume", ])
    
        if analysis_type == "Engineer Productivity Trends":
            plot_engineer_productivity()
        elif analysis_type == "Customer Project Volume":
            plot_customer_project_volume()

    elif action == "Drop Data":
        st.title("Drop Data")

        # Step 1: Select a table
        table_name = st.selectbox("Select a table:", ["Select a table"] + list(table_schemas.keys()))
        
        if table_name != "Select a table":
            # Step 2: Select a column from the chosen table
            columns = get_table_columns(table_name)
            column_name = st.selectbox("Select a column:", ["Select a column"] + columns)
            
            # Step 3: Enter a value to match for deletion
            if column_name != "Select a column":
                value_to_delete = st.text_input(f"Enter the value for {column_name} to delete rows:")
                
                st.session_state['delete_result'] = None

                # Button to execute the drop data action
                delete_button = st.button("Delete Rows")
                    
                if delete_button and value_to_delete:
                    confirm = st.checkbox("I understand this action cannot be undone and confirm the deletion.")
                    
                    if confirm:
                        query = f"DELETE FROM {table_name} WHERE {column_name} = %s;"
                        result = execute_query(query, params=(value_to_delete,), select=False)
                        if result["success"]:
                            if result["rows_affected"] > 0:
                                st.session_state['delete_result'] = f"Rows deleted successfully. {result['rows_affected']} rows affected."
                            else:
                                st.session_state['delete_result'] = "No rows were deleted. Please check the value and try again."
                        else:
                            st.session_state['delete_result'] = f"Failed to delete rows: {result['error']}"
                          
                 # Display the deletion result if it exists
                if st.session_state['delete_result']:
                    st.info(st.session_state['delete_result'])       
                    
    elif action == "Quit":
        st.title("Thank you for using the app!")
        st.stop()

if __name__ == "__main__":
    main()
