from flask import Flask, request, render_template, jsonify
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

app = Flask(__name__)

# Load or train the model
def load_or_train_model():
    model_path = 'crop_model.pkl'
    
    if os.path.exists(model_path):
        with open(model_path, 'rb') as file:
            return pickle.load(file)
    
    # Load the dataset from CSV file
    try:
        df = pd.read_csv('crop_data.csv')
    except FileNotFoundError:
        print("Warning: crop_data.csv not found. Using random data instead.")
        # Fallback to random data if CSV is not found
        data = {
            'N': np.random.randint(0, 140, 2000),
            'P': np.random.randint(5, 145, 2000),
            'K': np.random.randint(5, 205, 2000),
            'temperature': np.random.uniform(8.83, 43.68, 2000),
            'humidity': np.random.uniform(14.26, 99.98, 2000),
            'ph': np.random.uniform(3.5, 9.94, 2000),
            'rainfall': np.random.uniform(20.21, 298.56, 2000),
            'label': np.random.choice(
                ['rice', 'wheat', 'mung beans', 'Tea', 'millet', 'maize', 'lentil', 'jute', 'coffee', 'cotton', 'ground nut', 'peas', 'rubber', 'sugarcane', 'tobacco', 'kidney beans', 'moth beans', 'coconut', 'black gram', 'adzuki beans', 'pigeon peas', 'chick peas', 'banana', 'grapes', 'apple', 'mango', 'muskmelon', 'orange', 'papaya', 'pomegranate', 'watermelon'],
                2000
            )
        }
        df = pd.DataFrame(data)
    
    X = df.drop('label', axis=1)
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Calculate and print accuracy
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy:.2f}")
    
    # Save the model
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)
    
    return model

# Load the model
model = load_or_train_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get values from the form
        features = {
            'N': float(request.form['nitrogen']),
            'P': float(request.form['phosphorus']),
            'K': float(request.form['potassium']),
            'temperature': float(request.form['temperature']),
            'humidity': float(request.form['humidity']),
            'ph': float(request.form['ph']),
            'rainfall': float(request.form['rainfall'])
        }
        
        # Create a DataFrame with the input features
        input_df = pd.DataFrame([features])
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        
        return jsonify({
            'success': True,
            'prediction': prediction,
            'message': f'The recommended crop is: {prediction}'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True,port=5008)
