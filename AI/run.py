import pandas as pd
import mysql.connector
import subprocess


def run_script(script_path):
    """Run a Python script."""
    try:
        result = subprocess.run(
            ["python", script_path], capture_output=True, text=True, check=True
        )
        print(f"Script output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running script {script_path}:\n{e.stderr}")
        raise


def insert_db(predictions_df):
    """Insert predictions into database."""
    db_config = {
        "host": "your_host",
        "user": "your_user",
        "password": "your_password",
        "database": "greenhouse_data",
    }

    # Connect to the MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Insert data into the table for each row in the predictions DataFrame
    insert_query = """
        INSERT INTO environmental_conditions (Tair, Rhair, Tot_PAR, CO2air)
        VALUES (%s, %s, %s, %s)
    """

    for index, row in predictions_df.iterrows():
        cursor.execute(
            insert_query,
            (
                row["Tair"],
                row["Rhair"],
                row["Tot_PAR"],
                row["CO2air"],
            ),
        )

    conn.commit()
    cursor.close()
    conn.close()


def main():
    # Step 1: Run data and model scripts
    print("Running data processing script...")
    run_script("src/data_preprocess_1.py")  # Replace with the actual script name
    print("Running model prediction script...")
    run_script("src/data_preprocess_2.py")  # Replace with the actual script name

    # Step 2: Load predictions from CSV file
    print("Loading predictions from predictions.csv...")
    predictions_df = pd.read_csv(
        "./data/predictions.csv"
    )  # Replace with actual CSV file path

    # Step 3: Insert predictions into the database
    print("Inserting predictions into the database...")
    insert_db(predictions_df)

    # Step 4: Print predictions to confirm
    print("Predictions inserted successfully:")
    print(predictions_df)


if __name__ == "__main__":
    main()
