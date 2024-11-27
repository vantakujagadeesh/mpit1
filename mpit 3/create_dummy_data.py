import pandas as pd
import numpy as np

# Create dummy data
data = {
    'temperature': [
        28, 32, 35, 30,  # Summer samples
        5, 2, -1, 3,     # Winter samples
        15, 18, 12, 17,  # Spring samples
        22, 19, 21, 20   # Fall samples
    ],
    'humidity': [
        65, 70, 75, 68,  # Summer
        80, 85, 82, 78,  # Winter
        60, 65, 63, 67,  # Spring
        72, 70, 73, 71   # Fall
    ],
    'rainfall': [
        45, 52, 40, 48,  # Summer
        20, 25, 15, 22,  # Winter
        90, 85, 95, 88,  # Spring
        60, 55, 65, 58   # Fall
    ],
    'daylight_hours': [
        14, 14.5, 14.2, 14.3,  # Summer
        9, 8.5, 8.8, 9.2,      # Winter
        11, 11.5, 11.2, 11.8,  # Spring
        12, 12.5, 12.2, 12.8   # Fall
    ],
    'season': [
        'Summer', 'Summer', 'Summer', 'Summer',
        'Winter', 'Winter', 'Winter', 'Winter',
        'Spring', 'Spring', 'Spring', 'Spring',
        'Fall', 'Fall', 'Fall', 'Fall'
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('weather_data.csv', index=False) 