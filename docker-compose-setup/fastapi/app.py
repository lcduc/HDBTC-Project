from fastapi import FastAPI, HTTPException
import pymysql
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
import os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all domains
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# Database connection details
# MYSQL_HOST = "localhost"
# MYSQL_PORT = 3306
# MYSQL_USER = "admin"
# MYSQL_PASSWORD = "Binhlol707"
# MYSQL_DATABASE = "Greenhouse"

MYSQL_HOST = os.getenv("DB_HOST", "mysql-container")
MYSQL_PORT = int(os.getenv("DB_PORT", 3306))
MYSQL_USER = os.getenv("DB_USER", "admin")
MYSQL_PASSWORD = os.getenv("DB_PASSWORD", "Binhlol707")
MYSQL_DATABASE = os.getenv("DB_NAME", "Greenhouse")

@app.get("/calculate_monthly_averages/{greenhouseID}")
def calculate_monthly_averages(greenhouseID: int):
    """
    Returns exactly 12 months of:
    - Historical sensor data
    - Predicted data (missing months filled with 0)
    """

    try:
        connection = pymysql.connect(
            host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER,
            password=MYSQL_PASSWORD, database=MYSQL_DATABASE
        )

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Get the last 12 months
            months_list = []
            current_year = datetime.now().year
            current_month = datetime.now().month

            for i in range(12):
                year = current_year if current_month - i > 0 else current_year - 1
                month = (current_month - i) % 12 or 12
                months_list.append((year, month))

            # Create a temporary table with the last 12 months
            cursor.execute("CREATE TEMPORARY TABLE last_12_months (year INT, month INT);")
            insert_values = ", ".join([f"({y}, {m})" for y, m in months_list])
            cursor.execute(f"INSERT INTO last_12_months (year, month) VALUES {insert_values};")

            # Query for historical data (ensuring all months are included)
            historical_sql = """
                SELECT 
                    l.year, 
                    l.month, 
                    COALESCE(AVG(JSON_UNQUOTE(JSON_EXTRACT(value, '$.Tair'))), 0) AS avg_temperature,
                    COALESCE(AVG(JSON_UNQUOTE(JSON_EXTRACT(value, '$.Rhair'))), 0) AS avg_humidity,
                    COALESCE(AVG(JSON_UNQUOTE(JSON_EXTRACT(value, '$.Tot_PAR'))), 0) AS avg_light,
                    COALESCE(AVG(JSON_UNQUOTE(JSON_EXTRACT(value, '$.co2air'))), 0) AS avg_co2
                FROM last_12_months l
                LEFT JOIN sensor_data s 
                    ON YEAR(s.recorded_date) = l.year AND MONTH(s.recorded_date) = l.month
                    AND s.device_id IN (SELECT device_id FROM device_list WHERE greenhouse_id = %s)
                GROUP BY l.year, l.month
                ORDER BY l.year DESC, l.month DESC;
            """
            cursor.execute(historical_sql, (greenhouseID,))
            historical_results = cursor.fetchall()

            # Query for predicted data (ensuring missing months return 0)
            predicted_sql = """
                SELECT 
                    l.year, 
                    l.month, 
                    COALESCE(AVG(p.temperature), 0) AS avg_temperature,
                    COALESCE(AVG(p.humidity), 0) AS avg_humidity,
                    COALESCE(AVG(p.lightIntensity), 0) AS avg_light,
                    COALESCE(AVG(p.co2), 0) AS avg_co2
                FROM last_12_months l
                LEFT JOIN predicted_data p 
                    ON YEAR(p.date) = l.year AND MONTH(p.date) = l.month
                    AND p.greenhouseID = %s
                GROUP BY l.year, l.month
                ORDER BY l.year DESC, l.month DESC;
            """
            cursor.execute(predicted_sql, (greenhouseID,))
            predicted_results = cursor.fetchall()

        return {
            "historical_data": historical_results,
            "predicted_data": predicted_results
        }

    except Exception as e:
        return {"error": str(e)}
    finally:
        connection.close()

@app.get("/calculate_weekly_averages/{greenhouseID}")
def calculate_weekly_averages(greenhouseID: int):
    """
    Returns exactly 7 days of:
    - Historical sensor data
    - Predicted data (missing days filled with 0)
    """

    try:
        connection = pymysql.connect(
            host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER,
            password=MYSQL_PASSWORD, database=MYSQL_DATABASE
        )

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Get the last 7 days (formatted as YYYY-MM-DD)
            days_list = []
            for i in range(7):
                day = datetime.now() - timedelta(days=i)
                days_list.append(day.strftime("%Y-%m-%d"))

            # Create a temporary table with full dates
            cursor.execute("CREATE TEMPORARY TABLE last_7_days (date_str DATE);")
            insert_values = ", ".join([f"('{d}')" for d in days_list])
            cursor.execute(f"INSERT INTO last_7_days (date_str) VALUES {insert_values};")

            # Query for historical data (ensuring all days are included)
            historical_sql = """
                SELECT 
                    DATE_FORMAT(l.date_str, '%%d/%%m') AS date, 
                    COALESCE(AVG(JSON_UNQUOTE(JSON_EXTRACT(value, '$.Tair'))), 0) AS avg_temperature,
                    COALESCE(AVG(JSON_UNQUOTE(JSON_EXTRACT(value, '$.Rhair'))), 0) AS avg_humidity,
                    COALESCE(AVG(JSON_UNQUOTE(JSON_EXTRACT(value, '$.Tot_PAR'))), 0) AS avg_light,
                    COALESCE(AVG(JSON_UNQUOTE(JSON_EXTRACT(value, '$.co2air'))), 0) AS avg_co2
                FROM last_7_days l
                LEFT JOIN sensor_data s 
                    ON s.recorded_date = l.date_str
                    AND s.device_id IN (SELECT device_id FROM device_list WHERE greenhouse_id = %s)
                GROUP BY l.date_str
                ORDER BY l.date_str DESC;
            """
            cursor.execute(historical_sql, (greenhouseID,))
            historical_results = cursor.fetchall()

            # Query for predicted data (ensuring missing days return 0)
            predicted_sql = """
                SELECT 
                    DATE_FORMAT(l.date_str, '%%d/%%m') AS date, 
                    COALESCE(AVG(p.temperature), 0) AS avg_temperature,
                    COALESCE(AVG(p.humidity), 0) AS avg_humidity,
                    COALESCE(AVG(p.lightIntensity), 0) AS avg_light,
                    COALESCE(AVG(p.co2), 0) AS avg_co2
                FROM last_7_days l
                LEFT JOIN predicted_data p 
                    ON p.date = l.date_str
                    AND p.greenhouseID = %s
                GROUP BY l.date_str
                ORDER BY l.date_str DESC;
            """
            cursor.execute(predicted_sql, (greenhouseID,))
            predicted_results = cursor.fetchall()

        return {
            "historical_data": historical_results,
            "predicted_data": predicted_results
        }

    except Exception as e:
        return {"error": str(e)}
    finally:
        connection.close()

@app.get("/get_device_status/{greenhouseID}")
def get_device_status(greenhouseID: int):
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER,
            password=MYSQL_PASSWORD, database=MYSQL_DATABASE
        )
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT dl.device_id, dl.device_name, dsl.status, dsl.log_date, dsl.log_time
                FROM device_list dl
                LEFT JOIN device_status_log dsl 
                ON dl.device_id = dsl.device_id
                WHERE dl.greenhouse_id = %s 
                AND dsl.status_log_id = (
                    SELECT MAX(status_log_id) 
                    FROM device_status_log 
                    WHERE device_status_log.device_id = dl.device_id
                )
                ORDER BY dl.device_id;
            """
            cursor.execute(sql, (greenhouseID,))
            results = cursor.fetchall()

        return results if results else {"message": "No device status found"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        connection.close()

from pydantic import BaseModel
from typing import List
import pymysql
import json
import paho.mqtt.publish as publish

# MQTT Broker Details
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))

# Define the request model
class DeviceStatusEntry(BaseModel):
    greenhouseID: int
    deviceID: int
    device_status: int  # 1 = ON, 0 = OFF

@app.post("/update_device_status")
def update_device_status(device_status_list: List[DeviceStatusEntry]):
    # Stores the device status log in the database and publishes an MQTT message.
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER,
            password=MYSQL_PASSWORD, database=MYSQL_DATABASE
        )

        with connection.cursor() as cursor:
            messages = []  

            for entry in device_status_list:
                # Convert status to a string ('1' or '0')
                device_status_str = str(entry.device_status)

                # Insert into database
                sql = """
                    INSERT INTO device_status_log (device_id, status, log_date, log_time)
                    VALUES (%s, %s, CURDATE(), CURTIME());
                """
                cursor.execute(sql, (entry.deviceID, device_status_str))

                # Prepare MQTT message
                mqtt_topic = f"greenhouse/{entry.greenhouseID}/sensor_status"
                mqtt_payload = {
                    "greenhouseID": entry.greenhouseID,
                    "deviceID": entry.deviceID,
                    "device_status": entry.device_status
                }
                messages.append((mqtt_topic, json.dumps(mqtt_payload)))

            connection.commit()

            # Publish MQTT messages
            if messages:
                publish.multiple(
                    [{"topic": topic, "payload": payload} for topic, payload in messages],
                    hostname=MQTT_BROKER,
                    port=MQTT_PORT
                )

        return {"message": "Device status logs successfully inserted and published to MQTT"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        connection.close()

# --- Login Endpoint ---
from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/login")
def login(login_data: LoginRequest):
    # Authenticates a user and returns accountID and associated greenhouseIDs.
    email = login_data.email
    password = login_data.password

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            connect_timeout=5
        )

        with connection.cursor() as cursor:
            sql = "SELECT accountID FROM account WHERE email=%s AND password=%s"
            cursor.execute(sql, (email, password))
            result = cursor.fetchone()

            if result:
                accountID = result[0]
                sql_greenhouses = "SELECT greenhouseID FROM access WHERE accountID = %s"
                cursor.execute(sql_greenhouses, (accountID,))
                greenhouse_results = cursor.fetchall()
                greenhouseIDs = [row[0] for row in greenhouse_results]

                return {
                    "message": "Login successful",
                    "accountID": accountID,
                    "greenhouseIDs": greenhouseIDs
                }
            else:
                raise HTTPException(status_code=401, detail="Invalid credentials")

    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
    finally:
        connection.close()

# --- Greenhouse Details Endpoint ---
@app.get("/greenhouse_details")
def get_greenhouse_details(accountID: int):
    #Returns details of greenhouses associated with the given accountID.
    if not accountID:
        raise HTTPException(status_code=400, detail="accountID is required")

    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            connect_timeout=5
        )

        with connection.cursor() as cursor:
            sql = """
                SELECT g.greenhouseID, g.name AS greenhouse_name, g.location, a.accessID
                FROM access a
                JOIN greenhouse g ON a.greenhouseID = g.greenhouseID
                WHERE a.accountID = %s
            """
            cursor.execute(sql, (accountID,))
            results = cursor.fetchall()

            if not results:
                raise HTTPException(status_code=404, detail="No greenhouse access found for this accountID")

            greenhouse_details = [
                {
                    "greenhouseID": row[0],
                    "name": row[1],
                    "location": row[2],
                    "accessID": row[3]
                }
                for row in results
            ]

            return greenhouse_details

    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
    finally:
        connection.close()

# --- Alert Details Endpoint ---
from decimal import Decimal

@app.get("/alert_details")
def get_alert_details(greenhouseID: int):
    # Returns alert details associated with the given greenhouseID.
    if not greenhouseID:
        raise HTTPException(status_code=400, detail="greenhouseID is required")

    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            connect_timeout=5
        )

        with connection.cursor() as cursor:
            sql = """
                SELECT a.alertID, a.date, a.time, a.changeType, a.difference, t.parameter, t.threshold
                FROM alert a
                JOIN threshold t ON a.thresholdID = t.thresholdID
                JOIN predicted_data p ON a.predictionID = p.predictionID
                WHERE p.greenhouseID = %s
                ORDER BY a.date DESC, a.time DESC
            """
            cursor.execute(sql, (greenhouseID,))
            results = cursor.fetchall()

            if not results:
                raise HTTPException(status_code=404, detail="No alert data found for this greenhouseID")

            alerts = []
            for row in results:
                date_str = row[1].strftime("%Y-%m-%d") if hasattr(row[1], 'strftime') else str(row[1])
                time_str = row[2].strftime("%H:%M:%S") if hasattr(row[2], 'strftime') else str(row[2])
                difference = float(row[4]) if isinstance(row[4], Decimal) else row[4]
                threshold = float(row[6]) if isinstance(row[6], Decimal) else row[6]

                alerts.append({
                    "alertID": row[0],
                    "date": date_str,
                    "time": time_str,
                    "changeType": row[3],
                    "difference": difference,
                    "parameter": row[5],
                    "threshold": threshold
                })

            return alerts

    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
    finally:
        connection.close()

# --- Predicted Data Endpoint ---
@app.get("/predicted_data")
def get_predicted_data(greenhouseID: int):
    # Returns the latest predicted data for the given greenhouseID.
    if not greenhouseID:
        raise HTTPException(status_code=400, detail="greenhouseID is required")

    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            connect_timeout=5
        )

        with connection.cursor() as cursor:
            sql = """
                SELECT predictionID, date, time, temperature, humidity, lightIntensity, co2
                FROM predicted_data
                WHERE greenhouseID = %s
                ORDER BY date DESC, time DESC
                LIMIT 1
            """
            cursor.execute(sql, (greenhouseID,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="No predicted data found for this greenhouseID")

            predicted_data = {
                "predictionID": result[0],
                "date": result[1].strftime("%Y-%m-%d") if hasattr(result[1], 'strftime') else str(result[1]),
                "time": result[2].strftime("%H:%M:%S") if hasattr(result[2], 'strftime') else str(result[2]),
                "temperature": float(result[3]) if isinstance(result[3], Decimal) else result[3],
                "humidity": float(result[4]) if isinstance(result[4], Decimal) else result[4],
                "lightIntensity": float(result[5]) if isinstance(result[5], Decimal) else result[5],
                "co2": float(result[6]) if isinstance(result[6], Decimal) else result[6],
                "greenhouseID": greenhouseID
            }

            return predicted_data

    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
    finally:
        connection.close()

# --- Getthreshold Endpoint ---
@app.get("/getthreshold")
def get_threshold(greenhouseID: int):
    # Returns the latest threshold values for temperature, humidity, lightIntensity, and co2 for the given greenhouseID.
    if not greenhouseID:
        raise HTTPException(status_code=400, detail="greenhouseID is required")

    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            connect_timeout=5
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT t.thresholdID, t.parameter, t.date, t.threshold, t.uncertainty
                FROM threshold t
                WHERE t.greenhouseID = %s 
                AND t.parameter IN ('temperature', 'humidity', 'lightIntensity', 'co2')
                AND (t.parameter, t.date) IN (
                    SELECT parameter, MAX(date)
                    FROM threshold
                    WHERE greenhouseID = %s
                    GROUP BY parameter
                )
                ORDER BY FIELD(t.parameter, 'temperature', 'humidity', 'lightIntensity', 'co2');
            """
            cursor.execute(sql, (greenhouseID, greenhouseID))
            results = cursor.fetchall()

            if not results or len(results) < 4:
                raise HTTPException(status_code=404, detail="Not all threshold parameters found for this greenhouseID")

            thresholds = {}
            for row in results:
                thresholds[row[1]] = {
                    "thresholdID": row[0],
                    "date": row[2].strftime("%Y-%m-%d") if hasattr(row[2], 'strftime') else str(row[2]),
                    "threshold": float(row[3]) if isinstance(row[3], Decimal) else row[3],
                    "uncertainty": float(row[4]) if isinstance(row[4], Decimal) else row[4]
                }

            return thresholds

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
    finally:
        connection.close()

# --- Post Threshold Endpoint ---
from pydantic import BaseModel
from typing import List
from datetime import datetime

class ThresholdRecord(BaseModel):
    greenhouseID: int
    parameter: str
    threshold: float
    uncertainty: float

@app.post("/POSTthresholds")
def post_threshold(new_records: List[ThresholdRecord]):
    # Inserts new threshold records into the database for the given greenhouseID.
    try:
        new_records = new_records
    except Exception as e:
        return {"statusCode": 400, "body": json.dumps({"message": f"Invalid JSON format: {str(e)}"})}

    if not isinstance(new_records, list) or len(new_records) == 0:
        return {"statusCode": 400, "body": json.dumps({"message": "Invalid data format. Expected a list of records."})}

    for record in new_records:
        if not all(k in record.dict() for k in ["greenhouseID", "parameter", "threshold", "uncertainty"]):
            return {"statusCode": 400, "body": json.dumps({"message": "Each record must include greenhouseID, parameter, threshold, and uncertainty."})}

    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            connect_timeout=5
        )
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": f"Database connection error: {str(e)}"})}

    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO threshold (greenhouseID, parameter, threshold, uncertainty, date)
                VALUES (%s, %s, %s, %s, %s)
            """

            current_date = datetime.now().date()

            for record in new_records:
                cursor.execute(sql, (
                    record.greenhouseID,
                    record.parameter,
                    record.threshold,
                    record.uncertainty,
                    current_date
                ))

            connection.commit()

        return {"statusCode": 200, "body": json.dumps({"message": "Thresholds inserted successfully"})}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": f"Error processing request: {str(e)}"})}
    finally:
        connection.close()

# --- CurrentData Endpoint ---
@app.get("/currentData")
def get_current_data(greenhouseID: int):
    # Returns the latest sensor data for various device types associated with the given greenhouseID.
    if not greenhouseID:
        raise HTTPException(status_code=400, detail="Missing greenhouseID in query parameters")

    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            connect_timeout=5
        )
    except Exception as e:
        error_message = f"Database connection error: {e}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = f"""
                SELECT 
                    (SELECT value FROM sensor_data WHERE device_id = 
                        (SELECT device_id FROM device_list WHERE greenhouse_id = {greenhouseID} AND device_type = 'vent') 
                    ORDER BY recorded_date DESC, recorded_time DESC LIMIT 1) AS vent,
                    
                    (SELECT value FROM sensor_data WHERE device_id = 
                        (SELECT device_id FROM device_list WHERE greenhouse_id = {greenhouseID} AND device_type = 'light') 
                    ORDER BY recorded_date DESC, recorded_time DESC LIMIT 1) AS light,

                    (SELECT value FROM sensor_data WHERE device_id = 
                        (SELECT device_id FROM device_list WHERE greenhouse_id = {greenhouseID} AND device_type = 'curtain') 
                    ORDER BY recorded_date DESC, recorded_time DESC LIMIT 1) AS curtain,

                    (SELECT value FROM sensor_data WHERE device_id = 
                        (SELECT device_id FROM device_list WHERE greenhouse_id = {greenhouseID} AND device_type = 'pipe') 
                    ORDER BY recorded_date DESC, recorded_time DESC LIMIT 1) AS pipe,

                    (SELECT value FROM sensor_data WHERE device_id = 
                        (SELECT device_id FROM device_list WHERE greenhouse_id = {greenhouseID} AND device_type = 'co2') 
                    ORDER BY recorded_date DESC, recorded_time DESC LIMIT 1) AS co2,

                    (SELECT value FROM sensor_data WHERE device_id = 
                        (SELECT device_id FROM device_list WHERE greenhouse_id = {greenhouseID} AND device_type = 'temperature_humidity') 
                    ORDER BY recorded_date DESC, recorded_time DESC LIMIT 1) AS temperature_humidity,

                    (SELECT value FROM sensor_data WHERE device_id = 
                        (SELECT device_id FROM device_list WHERE greenhouse_id = {greenhouseID} AND device_type = 'outside_TandH') 
                    ORDER BY recorded_date DESC, recorded_time DESC LIMIT 1) AS outside_TandH,

                    (SELECT value FROM sensor_data WHERE device_id = 
                        (SELECT device_id FROM device_list WHERE greenhouse_id = {greenhouseID} AND device_type = 'outside_wind') 
                    ORDER BY recorded_date DESC, recorded_time DESC LIMIT 1) AS outside_wind,

                    (SELECT value FROM sensor_data WHERE device_id = 
                        (SELECT device_id FROM device_list WHERE greenhouse_id = {greenhouseID} AND device_type = 'outside_radiation') 
                    ORDER BY recorded_date DESC, recorded_time DESC LIMIT 1) AS outside_radiation
            """
            
            cursor.execute(query)
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="No sensor data found for this greenhouseID")

            return result

    except Exception as e:
        error_message = f"Error querying the database: {e}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)
    finally:
        connection.close()