import pandas as pd
from statsmodels.tsa.api import VAR
import pickle


model_data = pd.read_csv('/Dataset/Processed/ModelReadyDataset.csv')
target_columns = [col for col in model_data.columns if col.endswith('_t+30min')]
feature_columns = [col for col in model_data.columns if col not in target_columns and col != '%time']

var_data = model_data[feature_columns + target_columns]

train_size = int(len(var_data) * 0.9)
train_data = var_data.iloc[:train_size]

var_model = VAR(train_data)
var_results = var_model.fit(maxlags=6)

with open('/Model/VAR_Model.pkl', 'wb') as f:
    pickle.dump(var_results, f)

print("Model trained and saved as 'VAR_Model.pkl'.")