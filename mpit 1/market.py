from flask import Flask, render_template, request
import pickle
import numpy as np
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('crop_data.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS crops
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  type_id INTEGER NOT NULL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS predictions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  crop_type INTEGER,
                  season INTEGER,
                  production FLOAT,
                  demand INTEGER,
                  predicted_price FLOAT,
                  prediction_date TIMESTAMP)''')
    
    # Insert sample crop data if not exists
    c.execute("SELECT COUNT(*) FROM crops")
    if c.fetchone()[0] == 0:
        crops = [
            (1, 'Rice', 0),
            (2, 'Wheat', 1),
            (3, 'Corn', 2),
            (4, 'Potato', 3),
            (5, 'Tomato', 4),
            (6, 'Onion', 5)
        ]
        c.executemany('INSERT INTO crops VALUES (?,?,?)', crops)
    
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('crop_data.db')
    c = conn.cursor()
    
    # Fetch crop types for dropdown
    c.execute("SELECT * FROM crops")
    crops = c.fetchall()
    
    # Fetch recent predictions
    c.execute("""SELECT c.name, p.predicted_price, p.prediction_date 
                 FROM predictions p 
                 JOIN crops c ON p.crop_type = c.type_id 
                 ORDER BY p.prediction_date DESC LIMIT 5""")
    recent_predictions = c.fetchall()
    
    conn.close()
    return render_template('index.html', crops=crops, recent_predictions=recent_predictions)

@app.route('/predict', methods=['POST'])
def predict():
    # Get values from the form
    features = [float(x) for x in request.form.values()]
    features_array = [np.array(features)]
    
    # For demonstration, using dummy prediction
    prediction = 1500 + (features[0] * 100) + (features[1] * 200) + (features[2] * 0.5) + (features[3] * 150)
    
    # Store prediction in database
    conn = sqlite3.connect('crop_data.db')
    c = conn.cursor()
    
    c.execute("""INSERT INTO predictions 
                 (crop_type, season, production, demand, predicted_price, prediction_date)
                 VALUES (?, ?, ?, ?, ?, ?)""",
              (int(features[0]), int(features[1]), features[2], int(features[3]), 
               prediction, datetime.now()))
    
    # Get crop name
    c.execute("SELECT name FROM crops WHERE type_id = ?", (int(features[0]),))
    crop_name = c.fetchone()[0]
    
    conn.commit()
    conn.close()
    
    return render_template('index.html', 
                         prediction_text=f'Predicted Price for {crop_name}: ₹{prediction:.2f}')

if __name__ == '__main__':
    init_db()
    app.run(debug=True,port=8008)
