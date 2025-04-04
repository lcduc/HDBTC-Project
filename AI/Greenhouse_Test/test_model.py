import pandas as pd
import joblib
import sys
import os


def test_models(input_file):
    """
    Test all models on the given input file and output predictions to the terminal.

    Parameters:
        input_file (str): Path to the input CSV file containing test data.
    """

    test_data = pd.read_csv(input_file)

    model_dir = "Model"

    models = {}
    for target_col in target_columns:
        model_path = os.path.join(
            model_dir, f"trained_model_{target_col}.pkl"
        )  # Updated file name
        feature_columns_path = os.path.join(
            model_dir, f"feature_columns_{target_col}.pkl"
        )

        models[target_col] = {
            "model": joblib.load(model_path),
            "feature_columns": joblib.load(feature_columns_path),
        }

    predictions = {}

    for target_col, model_info in models.items():

        test_inputs = test_data[model_info["feature_columns"]]

        predictions[target_col] = model_info["model"].predict(test_inputs)[
            0
        ]  # Get the first (and only) prediction

    output_dict = {**test_data.iloc[0].to_dict(), **predictions}

    print("\nPredictions:")
    for key, value in output_dict.items():
        print(f"{key}: {value}")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python test_models.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    target_columns = [
        col
        for col in pd.read_csv("ModelReadyDataset.csv").columns
        if col.endswith("_t+30min")
    ]

    test_models(input_file)
