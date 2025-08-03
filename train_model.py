# train_model.py
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pandas as pd
import numpy as np
import joblib

# Create sample data
data = {
    'Age': np.random.randint(18, 70, 100),
    'Sleep Duration': np.random.uniform(4, 10, 100),
    'Physical Activity Level': np.random.randint(1, 11, 100),
    'Stress Level': np.random.randint(1, 11, 100),
    'BMI Category': np.random.choice(['Underweight', 'Normal', 'Overweight', 'Obese'], 100),
    'Heart Rate': np.random.randint(60, 100, 100),
    'Daily Steps': np.random.randint(2000, 15000, 100),
    'Gender': np.random.choice(['Male', 'Female'], 100),
    'Occupation': np.random.choice(['Sedentary', 'Active', 'Very Active'], 100),
    'Sleep Quality': np.random.randint(1, 11, 100)  # Target
}

df = pd.DataFrame(data)

# Preprocessing
numeric_features = ['Age', 'Sleep Duration', 'Physical Activity Level', 
                   'Stress Level', 'Heart Rate', 'Daily Steps']
categorical_features = ['BMI Category', 'Gender', 'Occupation']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(), categorical_features)
    ])

# Model pipeline
model = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor())
])

# Train
model.fit(df.drop('Sleep Quality', axis=1), df['Sleep Quality'])

# Save
joblib.dump(model, 'sleep_quality_model.pkl')
joblib.dump(list(df.drop('Sleep Quality', axis=1).columns), 'feature_names.pkl')