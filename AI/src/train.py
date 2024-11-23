from Model import Model
from Dataloader import TimeSeriesDataset
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import os

save_dir = "./models"
os.makedirs(save_dir, exist_ok=True)
model_save_path = os.path.join(save_dir, "LSTMNETATT_model.pth")

model_data = pd.read_csv('./data/processed/ModelReadyDataset.csv')
model_data['%time'] = pd.to_datetime(model_data['%time'])
feature_columns = ['Tout', 'Rhout', 'Iglob', 'RadSum', 'Windsp', 'AbsHumOut',
                   'VentLee', 'Ventwind', 'AssimLight', 'EnScr', 'BlackScr',
                   'PipeGrow', 'PipeLow', 'co2_dos']
target_columns = ['Tair_t+30min', 'Rhair_t+30min', 'Tot_PAR_t+30min', 'CO2air_t+30min']

X = model_data[feature_columns].values
y = model_data[target_columns].values

window_size = 6
X_seq, y_seq = [], []
for i in range(len(X) - window_size):
    X_seq.append(X[i:i + window_size])
    y_seq.append(y[i + window_size])
X_seq, y_seq = np.array(X_seq), np.array(y_seq)

train_size = int(len(X_seq) * 0.9)
X_train, X_test = X_seq[:train_size], X_seq[train_size:]
y_train, y_test = y_seq[:train_size], y_seq[train_size:]

train_dataset = TimeSeriesDataset(torch.tensor(X_train, dtype=torch.float32), torch.tensor(y_train, dtype=torch.float32))
test_dataset = TimeSeriesDataset(torch.tensor(X_test, dtype=torch.float32), torch.tensor(y_test, dtype=torch.float32))

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32)

args = {
    'cuda': False,
    'window': window_size,
    'hidRNN': 64,
    'hidCNN': 32,
    'hidSkip': 8,
    'CNN_kernel': 3,
    'skip': 2,
    'highway_window': 5,
    'dropout': 0.2,
    'model': 'attn',
    'attn_score': 'scaled_dot',
    'output_fun': None
}

data_args = {'m': X_train.shape[2]}
model = Model(args, data_args)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

num_epochs = 100
for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()
        y_pred = model(X_batch)
        y_pred = y_pred[:, :y_batch.shape[1]] 
        loss = criterion(y_pred, y_batch)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {total_loss / len(train_loader):.4f}")

torch.save(model.state_dict(), model_save_path)
print(f"Model saved at {model_save_path}")

