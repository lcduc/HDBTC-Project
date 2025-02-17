import pandas as pd
from prophet import Prophet
import pickle
import numpy as np
import os

# Create directory to save models
MODEL_DIR = "Models"
os.makedirs(MODEL_DIR, exist_ok=True)

# Load data
model_data = pd.read_csv("ModelReadyDataset.csv")

# Convert the time column to datetime
model_data["%time"] = pd.to_datetime(model_data["%time"])

# Initialize dictionaries to store forecasts and evaluations
forecasts = {}
evaluations = {}

# Train and save models
for target in [col for col in model_data.columns if col.endswith("_t+30min")]:
    print(f"Training Prophet model for target: {target}")
    
    # Prepare data for Prophet
    df = model_data[["%time", target]].rename(columns={"%time": "ds", target: "y"})
    
    # Train Prophet model
    model = Prophet()
    model.fit(df)
    
    # Save model
    model_path = os.path.join(MODEL_DIR, f"Prophet_Model_{target}.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    print(f"Model for {target} saved at {model_path}")
    
    # Create future dataframe for prediction
    future = model.make_future_dataframe(periods=30, freq="5min")
    
    # Generate forecast
    forecast = model.predict(future)
    forecasts[target] = forecast
    
    # Print last few rows of the forecast
    print(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"].tail()])

# Combine all forecasts into a single dataframe
combined_forecast = pd.DataFrame({"ds": forecasts[next(iter(forecasts))]["ds"]})
for target, forecast in forecasts.items():
    combined_forecast[target + "_yhat"] = forecast["yhat"]

# Save combined forecasts to a CSV file
combined_forecast.to_csv("Prophet_Multivariate_Forecast.csv", index=False)
print("Combined forecast saved as 'Prophet_Multivariate_Forecast.csv'.")
