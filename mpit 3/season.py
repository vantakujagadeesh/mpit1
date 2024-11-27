from flask import Flask, request, jsonify, render_template
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# Load the dataset
def load_dataset():
    try:
        data = pd.read_csv('weather_data.csv')
        return data
    except FileNotFoundError:
        print("Error: weather_data.csv not found. Please run create_dummy_data.py first.")
        return None

# Train the model
def train_model():
    data = load_dataset()
    if data is None:
        return
    
    X = data.drop('season', axis=1)
    y = data['season']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Test the model
    X_test_scaled = scaler.transform(X_test)
    accuracy = model.score(X_test_scaled, y_test)
    print(f"Model accuracy: {accuracy * 100:.2f}%")
    
    # Save the model and scaler
    with open('season_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

# Load the model and scaler
def load_model():
    with open('season_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    return model, scaler

# Train the model when the application starts
train_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.get_json()
        
        # Extract features
        features = np.array([[
            float(data['temperature']),
            float(data['humidity']),
            float(data['rainfall']),
            float(data['daylight_hours'])
        ]])
        
        # Load model and scaler
        model, scaler = load_model()
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        
        # Get prediction probability
        proba = model.predict_proba(features_scaled)[0]
        confidence = float(max(proba) * 100)
        
        return jsonify({
            'status': 'success',
            'prediction': prediction,
            'confidence': f"{confidence:.2f}%"
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True,port=5001)
