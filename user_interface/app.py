from flask import Flask, render_template, request, redirect, url_for
import db  # Make sure to implement the necessary functions in db.py

app = Flask(__name__)

@app.route('/add_model', methods=['GET', 'POST'])
def add_model():
    error_message = None
    if request.method == 'POST':
        dataset_id = request.form.get('dataset_id')
        engineer_id = request.form.get('engineer_id')
        customer_id = request.form.get('customer_id')
        description = request.form.get('description')
        
        success, message = db.insert_new_model(dataset_id, engineer_id, customer_id, description)
        if success:
            return redirect(url_for('home'))
        else:
            error_message = message

    return render_template('add_model.html', error=error_message)

@app.route('/list_models')
def list_models():
    models, error = db.get_all_models()
    if error or not models:
        # Handle empty or error state here
        print(f"No models found or error: {error}")
        error = error or "No models available."
        return render_template('list_models.html', error=error)
    return render_template('list_models.html', models=models)


@app.route('/execute_query', methods=['GET', 'POST'])
def execute_query():
    if request.method == 'POST':
        query = request.form.get('query')
        results, error = db.execute_custom_query(query)

        # Check if no results returned and no error occurred
        if not results and not error:
            message = "No returned data for the provided query."
            return render_template('execute_query.html', message=message, query=query)
        return render_template('execute_query.html', results=results, error=error, query=query)
    
    return render_template('execute_query.html')

@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
