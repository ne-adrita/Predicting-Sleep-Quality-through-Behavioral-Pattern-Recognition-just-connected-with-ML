from flask import Flask, request, render_template
import pickle
import pandas as pd

app = Flask(__name__)

# Load the model
try:
    model = pickle.load(open("model.pkl", "rb"))
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# Define all expected columns (adjust based on your model)
REQUIRED_COLUMNS = [
    'Person ID', 'Gender', 'Age', 'Occupation', 'Sleep Duration',
    'Physical Activity Level', 'Stress Level', 'BMI Category',
    'Blood Pressure', 'Heart Rate', 'Daily Steps'
]

@app.route("/")
def home():
    return render_template("index.html", 
                         input_data={col: "" for col in REQUIRED_COLUMNS},
                         prediction_text="")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get form data and create complete input
        form_data = request.form.to_dict()
        
        # Create DataFrame with all required columns
        input_data = {col: form_data.get(col, 0) for col in REQUIRED_COLUMNS}
        input_df = pd.DataFrame([input_data])
        
        # Convert numerical fields
        numerical_cols = ['Person ID', 'Age', 'Sleep Duration', 
                         'Physical Activity Level', 'Stress Level',
                         'Heart Rate', 'Daily Steps']
        for col in numerical_cols:
            input_df[col] = pd.to_numeric(input_df[col])
        
        # Make prediction
        prediction = model.predict(input_df)
        sleep_quality = prediction[0]
        
        quality_map = {1: "Poor", 2: "Fair", 3: "Good", 4: "Excellent"}
        quality_text = quality_map.get(sleep_quality, str(sleep_quality))
        
        return render_template("index.html",
                            input_data=input_data,
                            prediction_text=f"Predicted Sleep Quality: {quality_text}")
    
    except Exception as e:
        return render_template("index.html",
                            input_data=form_data,
                            prediction_text=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True, port=5001)