from flask import Flask, render_template, request, redirect, url_for, session, flash
import joblib
import numpy as np
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-123'  # Change for production!

# Initialize sleep quality predictor
try:
    from model_loader import SleepQualityPredictor
    predictor = SleepQualityPredictor()
    print("✅ Sleep quality model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    predictor = None

def validate_age(age):
    return 18 <= age <= 120

def validate_sleep_duration(hours):
    return 3 <= hours <= 12

def generate_recommendations(score, input_data):
    """Generate personalized sleep recommendations"""
    recommendations = []
    
    # Sleep duration analysis
    sleep_duration = input_data.get('sleep_duration', 7)
    if sleep_duration < 6:
        recommendations.append("🚨 Increase sleep to 7-9 hours (current: {:.1f}h)".format(sleep_duration))
    elif sleep_duration > 9:
        recommendations.append("⚠️ Slightly reduce sleep to 7-9 hours (current: {:.1f}h)".format(sleep_duration))
    else:
        recommendations.append("✅ Good sleep duration: {:.1f} hours".format(sleep_duration))
    
    # Stress analysis
    stress = input_data.get('stress_level', 5)
    if stress >= 7:
        recommendations.append("🧘 Try meditation or deep breathing exercises before bed (stress: {}/10)".format(stress))
    elif stress >= 5:
        recommendations.append("🌿 Consider relaxation techniques (stress: {}/10)".format(stress))
    
    # Physical activity analysis
    activity = input_data.get('physical_activity', 30)
    if activity < 30:
        recommendations.append("🏃 Increase daily activity to at least 30 minutes (current: {} mins)".format(activity))
    else:
        recommendations.append("👍 Good activity level: {} mins/day".format(activity))
    
    # BMI analysis
    bmi_map = {0: "Underweight", 1: "Normal", 2: "Overweight", 3: "Obese"}
    bmi_status = bmi_map.get(input_data.get('bmi_category', 1), "Unknown")
    if input_data.get('bmi_category', 1) >= 2:
        recommendations.append("🍏 Consider dietary improvements (BMI status: {})".format(bmi_status))
    
    # Heart rate analysis
    heart_rate = input_data.get('heart_rate', 70)
    if heart_rate > 80:
        recommendations.append("❤️ Lower resting heart rate through cardio (current: {} bpm)".format(heart_rate))
    
    # General tips based on score
    if score < 6:
        recommendations.append("⏰ Maintain consistent sleep schedule")
        recommendations.append("🌙 Create bedtime routine (reading, warm bath)")
        recommendations.append("📱 Avoid screens 1 hour before bed")
    elif score < 8:
        recommendations.append("🔍 Small improvements could optimize your sleep")
    else:
        recommendations.append("🌟 Excellent habits! Maintain your routine")
    
    return recommendations

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not email or not password:
            flash('Please fill in all fields', 'error')
        else:
            session['logged_in'] = True
            session['email'] = email
            session['login_time'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            return redirect(url_for('userinfo'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/userinfo', methods=['GET', 'POST'])
def userinfo():
    if not session.get('logged_in'):
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            age = int(request.form.get('age', 0))
            if not validate_age(age):
                flash('Please enter a valid age (18-120)', 'error')
                return redirect(url_for('userinfo'))
            
            session['user_info'] = {
                'gender': int(request.form.get('gender', 0)),
                'age': age,
                'occupation': int(request.form.get('occupation', 0))
            }
            return redirect(url_for('lifestyle'))
        except ValueError:
            flash('Invalid input format', 'error')
    
    return render_template('userinfo.html')

@app.route('/lifestyle', methods=['GET', 'POST'])
def lifestyle():
    if not session.get('logged_in') or not session.get('user_info'):
        flash('Please complete user info first', 'warning')
        return redirect(url_for('userinfo'))
    
    if request.method == 'POST':
        try:
            sleep_duration = float(request.form.get('sleep_duration', 0))
            if not validate_sleep_duration(sleep_duration):
                flash('Sleep duration should be 3-12 hours', 'error')
                return redirect(url_for('lifestyle'))
            
            session['lifestyle_data'] = {
                'sleep_duration': sleep_duration,
                'physical_activity': int(request.form.get('physical_activity', 0)),
                'stress_level': int(request.form.get('stress_level', 5))
            }
            return redirect(url_for('vitals'))
        except ValueError:
            flash('Please enter valid numbers', 'error')
    
    return render_template('lifestyle.html')

@app.route('/vitals', methods=['GET', 'POST'])
def vitals():
    if not session.get('logged_in') or not session.get('user_info') or not session.get('lifestyle_data'):
        flash('Please complete previous steps first', 'warning')
        return redirect(url_for('lifestyle'))
    
    if request.method == 'POST':
        try:
            session['vitals_data'] = {
                'bmi_category': int(request.form.get('bmi_category', 1)),
                'heart_rate': int(request.form.get('heart_rate', 70)),
                'daily_steps': int(request.form.get('daily_steps', 5000))
            }
            return redirect(url_for('predict'))
        except ValueError:
            flash('Please enter valid health metrics', 'error')
    
    return render_template('vitals.html')

@app.route('/predict')
def predict():
    if not session.get('logged_in'):
        flash('Session expired. Please login again.', 'warning')
        return redirect(url_for('login'))
    
    # Check if we have all required data
    required_sessions = ['user_info', 'lifestyle_data', 'vitals_data']
    if not all(key in session for key in required_sessions):
        missing = [key for key in required_sessions if key not in session]
        flash(f'Missing data: {", ".join(missing)}', 'error')
        return redirect(url_for('userinfo'))
    
    # Combine all data
    input_data = {
        **session['user_info'],
        **session['lifestyle_data'],
        **session['vitals_data']
    }
    
    # Get prediction
    try:
        if predictor:
            quality_score = predictor.predict(input_data)
            model_used = "AI Prediction Model"
        else:
            quality_score = min(10, max(1, round(
                5 + 
                (input_data.get('sleep_duration', 7) - 7) * 0.5 -
                input_data.get('stress_level', 5) * 0.2 +
                input_data.get('physical_activity', 5000) / 1000
            )))
            model_used = "Basic Heuristic"
        
        # Generate recommendations
        recommendations = generate_recommendations(quality_score, input_data)
        
        # Prepare data for display
        display_data = {
            'gender': ["Male", "Female", "Other"][input_data.get('gender', 0)],
            'age': input_data.get('age', 30),
            'occupation': ["Student", "Professional", "Healthcare", "Retired"][input_data.get('occupation', 0)],
            'sleep_duration': "{:.1f} hours".format(input_data.get('sleep_duration', 7)),
            'physical_activity': "{} minutes".format(input_data.get('physical_activity', 30)),
            'stress_level': "{}/10".format(input_data.get('stress_level', 5)),
            'bmi_category': ["Underweight", "Normal", "Overweight", "Obese"][input_data.get('bmi_category', 1)],
            'heart_rate': "{} bpm".format(input_data.get('heart_rate', 70)),
            'daily_steps': "{:,} steps".format(input_data.get('daily_steps', 5000)),
            'model_used': model_used
        }
        
        return render_template('predict.html',
                            score=quality_score,
                            input_data=display_data,
                            recommendations=recommendations)
    
    except Exception as e:
        print(f"Prediction error: {e}")
        flash('Error generating prediction. Please try again.', 'error')
        return redirect(url_for('vitals'))

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')