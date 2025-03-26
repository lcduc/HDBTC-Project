import pandas as pd
import joblib
import sys
import os
import requests
import json
import pymysql
from datetime import datetime

# API Base URL
API_URL = os.getenv("API_URL", "http://14.225.205.88:8000/currentData?greenhouseID=")

# Database connection details
DB_HOST = os.getenv("DB_HOST", "mysql-container")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Binhlol707")
DB_NAME = os.getenv("DB_NAME", "Greenhouse")

MODEL_DIR = "/app/Model"

# Define target prediction columns
TARGET_COLUMNS = ["Tair_t+30min", "Rhair_t+30min", "Tot_PAR_t+30min", "CO2air_t+30min"]

def fetch_latest_sensor_data(greenhouse_id):
    """
    Fetch the latest sensor data from the API.
    Ensures the feature names match the model expectations.
    """
    try:
        response = requests.get(f"{API_URL}{greenhouse_id}", timeout=5)
        response.raise_for_status()
        data = response.json()

        # Convert JSON fields into a structured dictionary
        structured_data = {}
        for key, value in data.items():
            if isinstance(value, str):
                try:
                    structured_data.update(json.loads(value))  # Convert nested JSON strings into a dict
                except json.JSONDecodeError:
                    print(f"?? Error decoding JSON for key: {key}")
            else:
                structured_data[key] = value

        # **Ensure correct feature names (case-sensitive)**
        rename_mapping = {
            "VentWind": "Ventwind",  # Fix capitalization
            "co2air": "CO2air"  # Fix lowercase "co2air" to match model
        }

        # Apply renaming
        structured_data = {rename_mapping.get(k, k): v for k, v in structured_data.items()}

        return structured_data

    except requests.exceptions.RequestException as e:
        print(f"? Error fetching data from API: {e}")
        sys.exit(1)

def load_models():
    """
    Load all trained models and their feature column lists.
    """
    models = {}
    for target_col in TARGET_COLUMNS:
        model_path = os.path.join(MODEL_DIR, f"trained_model_{target_col}.pkl")
        feature_columns_path = os.path.join(MODEL_DIR, f"feature_columns_{target_col}.pkl")

        try:
            models[target_col] = {
                'model': joblib.load(model_path),
                'feature_columns': joblib.load(feature_columns_path)
            }
        except FileNotFoundError as e:
            print(f"Error loading model for {target_col}: {e}")
            sys.exit(1)

    return models

def insert_predictions_into_db(greenhouse_id, predictions):
    """
    Insert predictions into the predicted_data table.
    """
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = connection.cursor()

        # Get current timestamp
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M:%S')

        # Prepare the SQL insert statement
        sql = """
        INSERT INTO predicted_data 
        (greenhouseID, date, time, temperature, humidity, lightIntensity, co2) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        # Extract relevant predictions
        cursor.execute(sql, (
            greenhouse_id,
            current_date,
            current_time,
            predictions.get("Tair_t+30min", None),
            predictions.get("Rhair_t+30min", None),
            predictions.get("Tot_PAR_t+30min", None),
            predictions.get("CO2air_t+30min", None)
        ))

        # Commit changes
        connection.commit()
        print(f"? Predictions successfully inserted for Greenhouse {greenhouse_id}")

    except pymysql.MySQLError as e:
        print(f"? Error inserting predictions into database: {e}")
    finally:
        cursor.close()
        connection.close()

def fetch_threshold_for_greenhouse(greenhouse_id):
    """
    Fetch the latest threshold data for the given greenhouse from the database.
    """
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = connection.cursor()

        # Get the latest threshold values for the greenhouse
        sql = """
        SELECT parameter, threshold, uncertainty
        FROM threshold
        WHERE greenhouseID = %s
        ORDER BY date DESC LIMIT 1;
        """
        cursor.execute(sql, (greenhouse_id,))
        threshold_data = cursor.fetchone()

        if threshold_data:
            threshold = {
                'parameter': threshold_data[0],
                'threshold': threshold_data[1],
                'uncertainty': threshold_data[2]
            }
            return threshold
        else:
            print(f"? No threshold data found for Greenhouse {greenhouse_id}")
            return None
    except pymysql.MySQLError as e:
        print(f"? Error fetching threshold data: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def compare_with_threshold_and_create_alert(greenhouse_id, predictions):
    """
    Compare the predictions with the threshold and insert an alert if necessary.
    """
    # Get the threshold for the greenhouse
    threshold = fetch_threshold_for_greenhouse(greenhouse_id)

    if threshold:
        # Loop through each predicted parameter
        for param in predictions:
            if param == threshold['parameter']:
                prediction_value = predictions[param]
                threshold_value = threshold['threshold']
                uncertainty = threshold['uncertainty']

                # Compare the prediction with the threshold considering the uncertainty
                if prediction_value > threshold_value + uncertainty or prediction_value < threshold_value - uncertainty:
                    # Create an alert entry
                    create_alert(greenhouse_id, param, prediction_value, threshold_value, uncertainty)
                else:
                    print(f"? {param} is within the threshold")

def create_alert(greenhouse_id, parameter, prediction_value, threshold_value, uncertainty):
    """
    Insert an alert entry into the `alert` table.
    """
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = connection.cursor()

        # Get current timestamp
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M:%S')

        # Determine the change type and severity
        change_type = "above" if prediction_value > threshold_value else "below"
        difference = abs(prediction_value - threshold_value)
        severity = "high" if difference > (uncertainty * 2) else "medium"  # Example: if the difference is more than twice the uncertainty, set to "high"

        # Prepare SQL statement to insert an alert
        sql = """
        INSERT INTO alert (predictionID, thresholdID, date, time, changeType, difference, severity)
        VALUES (NULL, NULL, %s, %s, %s, %s, %s);
        """
        cursor.execute(sql, (current_date, current_time, change_type, difference, severity))

        # Commit changes
        connection.commit()
        print(f"? Alert created for {parameter} in Greenhouse {greenhouse_id}")
    except pymysql.MySQLError as e:
        print(f"? Error inserting alert into database: {e}")
    finally:
        cursor.close()
        connection.close()

def run_inference(greenhouse_id):
    """
    Fetch real-time data from API and perform inference using trained models, then save to database.
    """
    # Fetch latest data from API
    sensor_data = fetch_latest_sensor_data(greenhouse_id)

    # Convert the data into a Pandas DataFrame
    input_data = pd.DataFrame([sensor_data])

    # Load models
    models = load_models()

    # Store predictions
    predictions = {}

    for target_col, model_info in models.items():
        # Ensure all required feature columns are present
        missing_features = [col for col in model_info['feature_columns'] if col not in input_data.columns]
        if missing_features:
            print(f"?? Warning: Missing features for {target_col}: {missing_features}")
            continue

        # Extract the necessary features
        test_inputs = input_data[model_info['feature_columns']]

        # Run inference and store results
        predictions[target_col] = model_info['model'].predict(test_inputs)[0]

    # Insert predictions into database
    insert_predictions_into_db(greenhouse_id, predictions)

    # Compare predictions with thresholds and insert alerts if necessary
    compare_with_threshold_and_create_alert(greenhouse_id, predictions)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python inference.py <greenhouse_id>")
        sys.exit(1)

    greenhouse_id = sys.argv[1]
    run_inference(greenhouse_id)
