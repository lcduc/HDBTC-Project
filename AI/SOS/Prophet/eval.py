import pandas as pd
from prophet import Prophet
import pickle
import os
import sys
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

# Directory containing saved models
MODEL_DIR = "Models"

# Check for input argument
if len(sys.argv) != 2:
    print("Usage: python eval.py <input_csv>")
    sys.exit(1)

# Load input data
input_file = sys.argv[1]
data = pd.read_csv(input_file)
data["%time"] = pd.to_datetime(data["%time"])

evaluations = {}

# Load models and evaluate
for model_filename in os.listdir(MODEL_DIR):
    if model_filename.endswith(".pkl"):
        target = model_filename.replace("Prophet_Model_", "").replace(".pkl", "")
        model_path = os.path.join(MODEL_DIR, model_filename)
        
        print(f"Evaluating model: {target}")
        
        # Load model
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        
        # Create future dataframe for prediction
        future = model.make_future_dataframe(periods=30, freq="5min")
        forecast = model.predict(future)
        
        # Evaluate the model
        actual = data[target].values if target in data.columns else None
        if actual is not None:
            predicted = forecast["yhat"].iloc[:len(actual)].values
            mse = mean_squared_error(actual, predicted)
            mae = mean_absolute_error(actual, predicted)
            r2 = r2_score(actual, predicted)
            ratio = np.mean(predicted / actual)
            
            evaluations[target] = {
                "MSE": mse,
                "MAE": mae,
                "R²": r2,
                "Mean Prediction-to-Actual Ratio": ratio
            }
            
            print(f"Evaluation for {target}:")
            print(f"  Mean Squared Error (MSE): {mse}")
            print(f"  Mean Absolute Error (MAE): {mae}")
            print(f"  R²: {r2}")
            print(f"  Mean Prediction-to-Actual Ratio: {ratio}")

# Save evaluation results to CSV
evaluation_df = pd.DataFrame.from_dict(evaluations, orient='index')
evaluation_df.to_csv("Prophet_Evaluation.csv", index=True)
print("Evaluation results saved as 'Prophet_Evaluation.csv'.")
