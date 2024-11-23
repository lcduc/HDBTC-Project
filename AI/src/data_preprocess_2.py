import pandas as pd

interpolated_data = pd.read_csv('./data/processed/cleaned_merged_data.csv')

interpolated_data['%time'] = pd.to_datetime(interpolated_data['%time'], unit='D', origin='1899-12-30')
interpolated_data['%time'] = interpolated_data['%time'].dt.strftime('%Y-%m-%d %H:%M:%S')


prediction_horizon = 6 
target_columns = ['Tair', 'Rhair', 'Tot_PAR', 'CO2air']
feature_columns = [col for col in interpolated_data.columns if col not in target_columns and col != '%time']

for target in target_columns:
    interpolated_data[f'{target}_t+30min'] = interpolated_data[target].shift(-prediction_horizon)

model_data = interpolated_data.dropna()

model_data.to_csv('./data/processed/ModelReadyDataset.csv', index=False)

print("Data prepared for modeling and saved as 'ModelReadyDataset.csv'.")
