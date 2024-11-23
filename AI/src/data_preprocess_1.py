import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

greenhouse_climate_data = pd.read_csv('./data/raw/GreenhouseClimateAICU.csv')
weather_data = pd.read_csv('./data/raw/Weather.csv')

merged_data = pd.merge(greenhouse_climate_data, weather_data, on='%time', suffixes=('_greenhouse', '_weather'))

columns_to_keep = [
    '%time', 'Tout', 'Rhout', 'Iglob', 'RadSum', 'Windsp', 'AbsHumOut',
    'VentLee', 'Ventwind', 'AssimLight', 'EnScr', 'BlackScr', 'PipeGrow', 'PipeLow', 'co2_dos',
    'Tair', 'Rhair', 'Tot_PAR', 'CO2air'
]

filtered_data = merged_data[columns_to_keep]

filtered_data = filtered_data.apply(pd.to_numeric, errors='coerce')

filtered_data.interpolate(method='linear', inplace=True)

filtered_data.to_csv('./data/processed/cleaned_merged_data.csv', index=False)

print("Saved as 'cleaned_merged_data.csv'.")