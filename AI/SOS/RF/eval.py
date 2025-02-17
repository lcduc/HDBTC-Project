# evaluate_model.py
import pandas as pd
import joblib
import sys
import os

def evaluate_model(test_data_path, output_file):
    model_dir = 'Model'

    model_path = os.path.join(model_dir, 'trained_rf_model.pkl')
    feature_columns_path = os.path.join(model_dir, 'feature_columns.pkl')

    rf_model = joblib.load(model_path)  
    feature_columns = joblib.load(feature_columns_path)  

    test_data = pd.read_csv(test_data_path)

    missing_features = set(feature_columns) - set(test_data.columns)
    if missing_features:
        raise ValueError(f"Test data is missing the following features: {missing_features}")

    X_test = test_data[feature_columns]

    y_pred = rf_model.predict(X_test)

    with open(output_file, 'w') as f:
        for pred in y_pred:
            f.write(','.join(map(str, pred)) + '\n')

    print(f"Predictions saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python evaluate_model.py <test_data_path> <output_file>")
        sys.exit(1)

    test_data_path = sys.argv[1]
    output_file = sys.argv[2]

    evaluate_model(test_data_path, output_file)