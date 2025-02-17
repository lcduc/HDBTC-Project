# evaluate_model.py
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import sys
import os

def evaluate_model(dataset_path, model_dir):
    # Load dataset
    model_data = pd.read_csv(dataset_path)

    # Prepare target and feature columns
    target_columns = [col for col in model_data.columns if col.endswith('_t+30min')]
    feature_columns = [col for col in model_data.columns if col not in target_columns and col != '%time']

    # Create VAR dataset
    var_data = model_data[feature_columns + target_columns]

    # Split data into training and testing sets
    train_size = int(len(var_data) * 0.9)
    test_data = var_data.iloc[train_size:]

    # Check for NaN values in test data
    if test_data.isna().any().any():
        raise ValueError("Test data contains NaN values. Please clean the data before proceeding.")

    # Load the trained model from the directory
    model_path = os.path.join(model_dir, 'VAR_Model.pkl')
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found in directory: {model_dir}")

    with open(model_path, 'rb') as f:
        var_results = pickle.load(f)

    # Make predictions
    y_pred = var_results.forecast(var_data.values[-var_results.k_ar:], steps=len(test_data))
    y_pred = pd.DataFrame(y_pred, columns=var_data.columns, index=test_data.index)

    # Evaluate model performance
    for target in target_columns:
        mse = mean_squared_error(test_data[target], y_pred[target])
        r2 = r2_score(test_data[target], y_pred[target])
        print(f"Target: {target}")
        print(f"Mean Squared Error: {mse}")
        print(f"R^2 Score: {r2}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python evaluate_model.py <dataset_path> <model_dir>")
        sys.exit(1)

    dataset_path = sys.argv[1]
    model_dir = sys.argv[2]
    evaluate_model(dataset_path, model_dir)