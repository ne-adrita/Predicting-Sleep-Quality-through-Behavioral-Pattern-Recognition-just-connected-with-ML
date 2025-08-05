import pickle
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# 1. Define the correct path to your CSV file
csv_path = "model/Sleep_Data_Sampledremoved_Dis.csv"

# 2. Verify the file exists
if not os.path.exists(csv_path):
    print(f"Error: File not found at {csv_path}")
    print("Please verify:")
    print(f"1. The file exists at this location")
    print(f"2. The filename is exactly: 'Sleep_Data_Sampledremoved_Dis.csv'")
    exit()

# 3. Load the data
try:
    data = pd.read_csv(csv_path)
    print("Data loaded successfully!")
    print(f"Shape: {data.shape}")
except Exception as e:
    print(f"Error loading CSV file: {e}")
    exit()

# 4. Prepare features and target
X = data.iloc[:, :-1]  # Features
y = data.iloc[:, -1]   # Target (Sleep_Quality)

# 5. Identify categorical columns
categorical_cols = X.select_dtypes(include=['object']).columns
numerical_cols = X.select_dtypes(exclude=['object']).columns

# 6. Create preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numerical_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ])

# 7. Create and train model
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

# 8. Save the model
model_path = "/Users/noshinebnatadrita/Documents/ML with Frontend/model.pkl"
try:
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    print(f"Model successfully saved to:\n{model_path}")
    print(f"File size: {os.path.getsize(model_path)/1024:.2f} KB")
except Exception as e:
    print(f"Error saving model: {e}")

    import pickle

with open("model.pkl", "rb") as f:
    loaded_model = pickle.load(f)

# Example prediction
new_data = [...]  # Your input features
prediction = loaded_model.predict([new_data])