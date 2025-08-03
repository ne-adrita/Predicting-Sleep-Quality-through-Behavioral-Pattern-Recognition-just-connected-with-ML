from sklearn.ensemble import RandomForestRegressor
import numpy as np
import joblib

# Create dummy training data
X = np.random.rand(100, 9)  # 100 samples, 9 features
y = np.random.randint(1, 11, 100)  # Random scores between 1-10

# Create and train a simple model
model = RandomForestRegressor(n_estimators=10)
model.fit(X, y)

# Save the model
joblib.dump(model, 'sleep_quality_model.pkl')
print("Dummy model created successfully!")