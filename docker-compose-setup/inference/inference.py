import pandas as pd
import joblib
import sys
import os
import requests
import json
import pymysql
from datetime import datetime

# API Base URL
API_URL = os.getenv("API_URL", "http://fastapi-server:8000/currentData?greenhouseID=")

# Database connection details
DB_HOST = os.getenv("DB_HOST", "mysql-container")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Binhlol707")
DB_NAME = os.getenv("DB_NAME", "Greenhouse")

MODEL_DIR = "/app/Model"

# Define target prediction columns
TARGET_COLUMNS = ["Tair_t+30min", "Rhair_t+30min", "Tot_PAR_t+30min", "CO2air_t+30min"]

# Mapping between model prediction keys and threshold API keys
PREDICTION_TO_THRESHOLD_KEY = {
    "Tair_t+30min": "temperature",
    "Rhair_t+30min": "humidity",
    "Tot_PAR_t+30min": "lightIntensity",
    "CO2air_t+30min": "co2"
}

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
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = connection.cursor()

        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M:%S')

        sql = """
        INSERT INTO predicted_data 
        (greenhouseID, date, time, temperature, humidity, lightIntensity, co2) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            greenhouse_id, current_date, current_time,
            predictions.get("Tair_t+30min"),
            predictions.get("Rhair_t+30min"),
            predictions.get("Tot_PAR_t+30min"),
            predictions.get("CO2air_t+30min")
        ))
        connection.commit()
        prediction_id = cursor.lastrowid  # ✅ Get inserted ID
        print(f"? Predictions successfully inserted for Greenhouse {greenhouse_id} [ID: {prediction_id}]")
        return prediction_id

    except pymysql.MySQLError as e:
        print(f"? Error inserting predictions: {e}")
        return None
    finally:
        cursor.close()
        connection.close()


def fetch_thresholds_from_api(greenhouse_id):
    """
    Fetch threshold values for all parameters from the FastAPI container.
    """
    try:
        url = f"http://fastapi-server:8000/getthreshold?greenhouseID={greenhouse_id}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"? Error fetching thresholds from API: {e}")
        return {}


def compare_with_threshold_and_create_alert(greenhouse_id, predictions, prediction_id):
    try:
        response = requests.get(f"http://fastapi-server:8000/getthreshold?greenhouseID={greenhouse_id}", timeout=5)
        response.raise_for_status()
        thresholds = response.json()
    except requests.RequestException as e:
        print(f"? Error fetching thresholds from API: {e}")
        return

    for pred_key, pred_value in predictions.items():
        threshold_key = PREDICTION_TO_THRESHOLD_KEY.get(pred_key)
        if not threshold_key or threshold_key not in thresholds:
            print(f"? No threshold found for {pred_key}")
            continue

        threshold_info = thresholds[threshold_key]
        threshold_value = threshold_info["threshold"]
        uncertainty = threshold_info["uncertainty"]
        threshold_id = threshold_info["thresholdID"]

        if pred_value > threshold_value + uncertainty or pred_value < threshold_value - uncertainty:
            create_alert(greenhouse_id, pred_key, pred_value, threshold_value, uncertainty, threshold_id, prediction_id)
        else:
            print(f"? {pred_key} is within threshold.")


def create_alert(greenhouse_id, parameter, prediction_value, threshold_value, uncertainty, threshold_id, prediction_id):
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = connection.cursor()

        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M:%S')
        change_type = "exceed" if prediction_value > threshold_value else "drop under"
        difference = abs(prediction_value - threshold_value)
        severity = "high" if difference > (uncertainty * 2) else "medium"

        sql = """
        INSERT INTO alert (predictionID, thresholdID, date, time, changeType, difference, severity)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(sql, (
            prediction_id, threshold_id,
            current_date, current_time,
            change_type, difference, severity
        ))
        connection.commit()
        print(f"? Alert created for {parameter} in Greenhouse {greenhouse_id}")
    except pymysql.MySQLError as e:
        print(f"? Error inserting alert: {e}")
    finally:
        cursor.close()
        connection.close()

def run_inference(greenhouse_id):
    sensor_data = fetch_latest_sensor_data(greenhouse_id)
    input_data = pd.DataFrame([sensor_data])
    models = load_models()
    predictions = {}

    for target_col, model_info in models.items():
        missing_features = [col for col in model_info['feature_columns'] if col not in input_data.columns]
        if missing_features:
            print(f"?? Warning: Missing features for {target_col}: {missing_features}")
            continue
        test_inputs = input_data[model_info['feature_columns']]
        predictions[target_col] = model_info['model'].predict(test_inputs)[0]

    prediction_id = insert_predictions_into_db(greenhouse_id, predictions)
    if prediction_id:
        compare_with_threshold_and_create_alert(greenhouse_id, predictions, prediction_id)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python inference.py <greenhouse_id>")
        sys.exit(1)

    greenhouse_id = sys.argv[1]
    run_inference(greenhouse_id)
