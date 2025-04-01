import paho.mqtt.client as mqtt
import mysql.connector
import json
import datetime
import os

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt-broker")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "greenhouse/+/sensor")

# MySQL Configuration
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql-container")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER", "admin")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "Binhlol707")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "Greenhouse")

LOG_FILE = "error_log.txt"

# Expected JSON structure
EXPECTED_STRUCTURE = {
    "greenhouse_id": int,
    "timestamp": str,
    "sensors": {
        "vent": dict,
        "light": dict,
        "curtain": dict,
        "pipe": dict,
        "co2": dict,
        "temperature_humidity": dict,
        "outside_TandH": dict,
        "outside_wind": dict,
        "outside_radiation": dict
    }
}

# Validate JSON structure
def validate_json(message):
    try:
        data = json.loads(message)
        if not all(key in data for key in EXPECTED_STRUCTURE):
            return False
        if not isinstance(data["greenhouse_id"], int):
            return False
        if not isinstance(data["timestamp"], str):
            return False
        if not isinstance(data["sensors"], dict):
            return False
        for sensor_type in EXPECTED_STRUCTURE["sensors"]:
            if sensor_type not in data["sensors"] or not isinstance(data["sensors"][sensor_type], dict):
                return False
        return True
    except json.JSONDecodeError:
        return False

# Log invalid messages
def log_invalid_message(topic, message):
    with open(LOG_FILE, "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] Invalid message from topic {topic}: {message}\n")

# Insert data into MySQL
def insert_sensor_data(data):
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        cursor = connection.cursor()
        greenhouse_id = data["greenhouse_id"]
        timestamp = datetime.datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%S")
        recorded_date = timestamp.date()
        recorded_time = timestamp.time()

        for device_type, sensor_values in data["sensors"].items():
            cursor.execute(
                "SELECT device_id FROM device_list WHERE device_type = %s AND greenhouse_id = %s",
                (device_type, greenhouse_id)
            )
            result = cursor.fetchone()
            if result:
                device_id = result[0]
                cursor.execute("""
                    INSERT INTO sensor_data (device_id, value, recorded_date, recorded_time)
                    VALUES (%s, %s, %s, %s)
                """, (device_id, json.dumps(sensor_values), recorded_date, recorded_time))

        connection.commit()
        cursor.close()
        connection.close()
        print(f"[?] Data inserted for greenhouse_id {greenhouse_id}")
    except Exception as e:
        print(f"[?] DB error: {e}")

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)
    print(f"[MQTT] Subscribed to topic: {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        print(f"[MQTT] Received message on {msg.topic}: {payload}")
        if validate_json(payload):
            print("[?] JSON is valid.")
            insert_sensor_data(json.loads(payload))
        else:
            print("[??] Invalid JSON. Logging...")
            log_invalid_message(msg.topic, payload)
    except Exception as e:
        print(f"[?] Error in on_message: {e}")

# MQTT Client Setup
client = mqtt.Client()  # Use default API version 1 for now
client.on_connect = on_connect
client.on_message = on_message

print(f"[INFO] Connecting to broker at {MQTT_BROKER}:{MQTT_PORT}...")
client.connect(MQTT_BROKER, MQTT_PORT)
print("[INFO] Starting loop_forever()")
client.loop_forever()

