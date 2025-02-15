# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

# Create the Model directory if it doesn't exist
model_dir = 'Model'
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

model_data = pd.read_csv('/Dataset/Processed/ModelReadyDataset.csv')


feature_columns = [col for col in model_data.columns if not col.endswith('_t+30min') and col != '%time']
target_columns = [col for col in model_data.columns if col.endswith('_t+30min')]

lag_features = []
for lag in range(1, 7):
    for col in feature_columns:
        lagged_col = f"{col}_lag{lag}"
        model_data[lagged_col] = model_data[col].shift(lag)
        lag_features.append(lagged_col)

model_data = model_data.dropna()

feature_columns.extend(lag_features)

X = model_data[feature_columns]
y = model_data[target_columns]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_train, y_train)


model_path = os.path.join(model_dir, 'trained_rf_model.pkl')
feature_columns_path = os.path.join(model_dir, 'feature_columns.pkl')

joblib.dump(rf_model, model_path)
joblib.dump(feature_columns, feature_columns_path)

print(f"Training complete. Saved at '{model_dir}' .")