import os
import time
import paho.mqtt.client as mqtt
import mysql.connector

DB_HOST = os.getenv("DB_HOST", "mysql-container")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Binhlol707")
DB_NAME = os.getenv("DB_NAME", "Greenhouse")

MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt-broker")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))

# Keep track of how many topics were already created
created_topic_ids = set()

def get_greenhouse_ids():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute("SELECT greenhouseID FROM greenhouse")
        result = cursor.fetchall()
        connection.close()
        return [row[0] for row in result]
    except Exception as e:
        print(f"[ERROR] DB connection or query failed: {e}")
        return []

def publish_mqtt_topics(greenhouse_id):
    try:
        client = mqtt.Client()
        print(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
        client.connect(MQTT_BROKER, MQTT_PORT)
        print("Connected to MQTT broker successfully")
        sensor_topic = f"greenhouse/{greenhouse_id}/sensor"
        status_topic = f"greenhouse/{greenhouse_id}/sensor_status"

        client.publish(sensor_topic, "Initializing sensor data...")
        client.publish(status_topic, "Initializing sensor status...")

        print(f"[INFO] MQTT topics published for greenhouse {greenhouse_id}")
        client.disconnect()
    except Exception as e:
        print(f"[ERROR] Failed to publish MQTT topics for greenhouse {greenhouse_id}: {e}")

def main():
    print("[INFO] Auto MQTT topic creator started.")
    while True:
        greenhouse_ids = get_greenhouse_ids()
        print(f"[DEBUG] Found greenhouse IDs in DB: {greenhouse_ids}")

        for gid in greenhouse_ids:
            if gid not in created_topic_ids:
                publish_mqtt_topics(gid)
                created_topic_ids.add(gid)
            else:
                print(f"[DEBUG] Topics already created for greenhouse {gid}")

        time.sleep(60)

if __name__ == "__main__":
    main()
