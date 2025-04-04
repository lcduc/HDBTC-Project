import torch
import pandas as pd
import numpy as np
from torch.utils.data import DataLoader
from src.Model import Model
from src.Dataloader import TimeSeriesDataset

# Load the data
csv_file_path = "./data/processed/cleaned_merged_data.csv"
data = pd.read_csv(csv_file_path)

if "%time" in data.columns:
    data["%time"] = pd.to_datetime(data["%time"])

feature_columns = [
    "Tout",
    "Rhout",
    "Iglob",
    "RadSum",
    "Windsp",
    "AbsHumOut",
    "VentLee",
    "Ventwind",
    "AssimLight",
    "EnScr",
    "BlackScr",
    "PipeGrow",
    "PipeLow",
    "co2_dos",
]

# Features as input (X)
X = data[feature_columns].values
window_size = 6  # Number of past time steps to consider for prediction

# Create a sequence for the most recent time step (only one row for the next prediction)
X_seq = X[-window_size:]  # Get the last `window_size` rows
X_seq = np.expand_dims(
    X_seq, axis=0
)  # Add batch dimension (1, window_size, num_features)

# Convert to tensor
X_seq = torch.tensor(X_seq, dtype=torch.float32)

# Print shape of X_seq
print(f"Shape of X_seq: {X_seq.shape}")  # Should be (1, window_size, num_features)

# Load the trained model
args = {
    "cuda": False,
    "window": window_size,
    "hidRNN": 64,
    "hidCNN": 32,
    "hidSkip": 8,
    "CNN_kernel": 3,
    "skip": 2,
    "highway_window": 5,
    "dropout": 0.2,
    "model": "attn",
    "attn_score": "scaled_dot",
    "output_fun": None,
}

data_args = {"m": X_seq.shape[2]}  # Correctly access the number of features (14)
print(f"X_seq size(2): {X_seq.size(2)}")  # Should output 14 (number of features)

model = Model(args, data_args)
model_save_path = "./models/LSTMNETATT_model.pth"
model.load_state_dict(torch.load(model_save_path))
model.eval()  # Set the model to evaluation mode

# Make prediction for the next 5 minutes (1 row)
with torch.no_grad():
    y_pred = model(X_seq)

# Convert the prediction from tensor to numpy
y_pred = y_pred.numpy()

# Print the full output to inspect which values are predicted
print("Full prediction output (14 values):")
print(y_pred)

target_indices = [
    0,
    1,
    2,
    13,
]
y_pred = y_pred[:, target_indices]  # Slice to keep only the desired targets

# Print the sliced prediction for the next 5 minutes
print("Prediction for the next 5 minutes (only target values):")
print(y_pred)

# Save the predictions to CSV (assuming you want to store the results)
target_columns = ["Tout", "Iglob", "Rhout", "co2_dos"]  # Define your target columns
output_csv_path = "./data/predictions.csv"
pd.DataFrame(y_pred, columns=[f"Pred_{col}" for col in target_columns]).to_csv(
    output_csv_path, index=False
)

print(f"Prediction saved to {output_csv_path}")
