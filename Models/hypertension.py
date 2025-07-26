import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from scipy import stats
from flask import Flask, request, jsonify, render_template

# Load trained model and scaler
model = joblib.load("hypertension_model.pkl")
scaler = joblib.load("hypertension_scaler.pkl")

# ================================================
# PREPROCESSING FOR NEW HYPERTENSION DATA
# ================================================

# Define valid physiological ranges for each feature
PHYSIOLOGICAL_RANGES = {
    'age': (0, 120),
    'salt_intake': (0, 50),  # grams/day
    'stress_score': (0, 10),
    'sleep_duration': (0, 24),  # hours
    'bmi': (10, 60),  # kg/m²
}

# Encoding maps (same as your training)
ENCODING_MAPS = {
    'family_history': {'Yes': 1, 'No': 0},
    'smoking_status': {'Smoker': 1, 'Non-Smoker': 0}
}

def preprocess_hypertension(input_data, impute_with_mode=True, cap_outliers=True):

    # Convert to DataFrame
    X = pd.DataFrame([input_data])
    
    # Handle Missing Values
    numerical_cols = ['age', 'salt_intake', 'stress_score', 'sleep_duration', 'bmi']
    categorical_cols = list(ENCODING_MAPS.keys())
    
    for col in X.columns:
        if X[col].isnull().any():
            if col in numerical_cols:
                skewness = X[col].skew()
                if abs(skewness) < 1:  # Normal distribution
                    X[col] = X[col].fillna(X[col].mean())
                else:  # Skewed distribution
                    X[col] = X[col].fillna(X[col].median())

            elif col in categorical_cols:
                if impute_with_mode:
                    X[col] = X[col].fillna(X[col].mode()[0])
                else:
                    X[col] = X[col].fillna('Unknown')
    
    # Outlier Capping (IQR Method)
    for col in numerical_cols:
        if col in X:
            q1 = X[col].quantile(0.25)
            q3 = X[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            # Cap outliers
            X[col] = np.where(X[col] < lower_bound, lower_bound, X[col])
            X[col] = np.where(X[col] > upper_bound, upper_bound, X[col])
            
            # Log transform if still skewed
            if abs(X[col].skew()) > 1:
                X[col] = np.log1p(X[col])
    
    # Encoding
    for col, mapping in ENCODING_MAPS.items():
        if col in X:
            # Handle unseen categories
            valid_cats = set(mapping.keys())
            X[col] = X[col].apply(lambda x: mapping.get(x, -1))  # -1 for unknown
    
    # Duplicates (for batch processing)
    # Not applicable for single prediction, but:
    # X = X.drop_duplicates()
    
    return X

# ================================================
# PREDICTION FUNCTION
# ================================================

def predict_hypertension(user_input):
    """
    Args:
        user_input: Dict of user-provided values (e.g., from web form)
    Returns:
        dict: {'probability': float, 'message': str}
    """
    try:
        # Preprocess
        processed_data = preprocess_hypertension(user_input)
        
        # Predict
        proba = model.predict_proba(processed_data)[0][1]  # P(class=1)
        pred = int(proba >= 0.5)  # Threshold at 0.5
        proba_percent = proba * 100
        
        # Interpret result
        messages = {
            0: "Low risk of hypertension",
            1: "High risk of hypertension - consult a doctor"
        }
        
        return {
            'prediction': pred,
            'risk_percent': round(proba_percent, 3),
            'message': messages[pred]
        }
    
    except Exception as e:
        return {'error': str(e)}

# ================================================
# FLASK APP
# ================================================

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def home():
    return render_template('Models\hypertension.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        result = predict_hypertension(data)
        return jsonify({
            'prediction': result['prediction'],
            'risk_percent': result['risk_percent'],
            'message': result['message']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)

    # user_data = {
    #     'age': 45,
    #     'salt_intake': 9.5,
    #     'stress_score': 7,
    #     'sleep_duration': 6.2,
    #     'bmi': 28.1,
    #     'family_history': 'Yes',
    #     'smoking_status': 'Non-Smoker'
    # }
    
    # risk_percent = predict_hypertension(user_data)
    # print("Hypertension Risk Percentage:", risk_percent)