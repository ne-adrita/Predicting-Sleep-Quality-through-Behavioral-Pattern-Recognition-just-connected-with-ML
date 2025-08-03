import joblib
import numpy as np
from sklearn.pipeline import Pipeline

class SleepQualityPredictor:
    def __init__(self):
        # Load the trained model
        self.model = joblib.load('sleep_quality_model.pkl')
        
        # Define expected features in order
        self.feature_order = [
            'gender', 'age', 'occupation',
            'sleep_duration', 'physical_activity',
            'stress_level', 'bmi_category',
            'heart_rate', 'daily_steps'
        ]
    
    def preprocess_input(self, input_data):
        """Convert input data to model-ready format"""
        # Convert to list in correct order
        processed = [input_data[feature] for feature in self.feature_order]
        return [processed]
    
    def predict(self, input_data):
        """Predict sleep quality score (1-10) with confidence"""
        try:
            processed_data = self.preprocess_input(input_data)
            raw_prediction = self.model.predict(processed_data)[0]
            
            # Ensure score is between 1-10
            final_score = min(10, max(1, round(raw_prediction)))
            
            return final_score
            
        except Exception as e:
            print(f"Prediction error: {e}")
            # Fallback heuristic
            return self.fallback_prediction(input_data)
    
    def fallback_prediction(self, input_data):
        """Simple heuristic when model fails"""
        base_score = 5
        # Adjust based on sleep duration
        base_score += (input_data['sleep_duration'] - 7) * 0.5
        # Adjust based on stress
        base_score -= input_data['stress_level'] * 0.2
        # Adjust based on activity
        base_score += min(2, input_data['physical_activity'] / 2000)
        return min(10, max(1, round(base_score)))