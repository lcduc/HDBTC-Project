import pymysql
import math
import subprocess
import time
import os
import logging
from datetime import datetime

logging.basicConfig(
    filename="/var/log/deploy_containers.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

GREENHOUSES_PER_CONTAINER = 20
CONTAINER_NAME_PREFIX = "greenhouse-predictor-"

def get_env_config():
    config = {
        "DB_HOST": os.getenv("DB_HOST", "mysql-container"),
        "DB_PORT": int(os.getenv("DB_PORT", 3306)),
        "DB_USER": os.getenv("DB_USER", "admin"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD", "Binhlol707"),
        "DB_NAME": os.getenv("DB_NAME", "Greenhouse"),
        "DOCKER_IMAGE": os.getenv("DOCKER_IMAGE", "greenhouse-predictor:latest")
    }
    logging.info(f"[CONFIG] Loaded config: {config}")
    return config

def get_greenhouse_count(config):
    max_retries = 5
    retry_delay = 5
    for attempt in range(max_retries):
        try:
            logging.info(f"[DB CONNECT] Attempt {attempt + 1}/{max_retries} to {config['DB_HOST']}:{config['DB_PORT']}")
            connection = pymysql.connect(
                host=config["DB_HOST"],
                port=config["DB_PORT"],
                user=config["DB_USER"],
                password=config["DB_PASSWORD"],
                database=config["DB_NAME"],
                connect_timeout=5
            )
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM greenhouse")
                total_greenhouses = cursor.fetchone()[0]
                cursor.execute("SELECT greenhouseID FROM greenhouse ORDER BY greenhouseID")
                greenhouse_ids = [row[0] for row in cursor.fetchall()]
            connection.close()
            logging.info(f"[DB RESULT] Found {total_greenhouses} greenhouses")
            return total_greenhouses, greenhouse_ids
        except Exception as e:
            logging.error(f"[DB ERROR] Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                logging.error("[DB ERROR] All retries failed.")
                return 0, []

def stop_existing_containers():
    try:
        result = subprocess.run(
            ["docker", "ps", "-a", "-q", "--filter", f"name={CONTAINER_NAME_PREFIX}"],
            capture_output=True, text=True, check=True
        )
        container_ids = result.stdout.strip().split()
        if container_ids:
            logging.info(f"[CLEANUP] Removing containers: {container_ids}")
            subprocess.run(["docker", "stop"] + container_ids, capture_output=True, check=True)
            subprocess.run(["docker", "rm"] + container_ids, capture_output=True, check=True)
        else:
            logging.info("[CLEANUP] No containers to stop.")
    except subprocess.CalledProcessError as e:
        logging.error(f"[CLEANUP ERROR] Command failed: {e.stderr}")
    except Exception as e:
        logging.error(f"[CLEANUP ERROR] {str(e)}")

def deploy_containers(total_greenhouses, greenhouse_ids, config):
    try:
        num_containers = math.ceil(total_greenhouses / GREENHOUSES_PER_CONTAINER)
        logging.info(f"[DEPLOY] Deploying {num_containers} container(s) for {total_greenhouses} greenhouses")
        stop_existing_containers()
        for i in range(num_containers):
            start_idx = i * GREENHOUSES_PER_CONTAINER
            end_idx = min(start_idx + GREENHOUSES_PER_CONTAINER, total_greenhouses)
            subset_ids = greenhouse_ids[start_idx:end_idx]
            greenhouse_ids_str = ",".join(map(str, subset_ids))
            container_name = f"{CONTAINER_NAME_PREFIX}{i}"
            logging.info(f"[DEPLOY] Launching {container_name} for greenhouse IDs: {greenhouse_ids_str}")
            cmd = [
                "docker", "run", "-d",
                "--name", container_name,
                "--network", "docker-compose-setup_greenhouse-net",  
                "-e", f"GREENHOUSE_IDS={greenhouse_ids_str}",
                "-e", f"DB_HOST={config['DB_HOST']}",
                "-e", f"DB_PORT={config['DB_PORT']}",
                "-e", f"DB_USER={config['DB_USER']}",
                "-e", f"DB_PASSWORD={config['DB_PASSWORD']}",
                "-e", f"DB_NAME={config['DB_NAME']}",
                config["DOCKER_IMAGE"]
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logging.info(f"[SUCCESS] Container {container_name} started with ID: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        logging.error(f"[DEPLOY ERROR] Command failed: {e.stderr}")
    except Exception as e:
        logging.error(f"[DEPLOY ERROR] {str(e)}")

def get_next_run_time():
    now = datetime.now()
    if now.minute < 20:
        next_minute = 20
    elif now.minute < 50:
        next_minute = 50
    else:
        next_minute = 20
        now = now.replace(hour=(now.hour + 1) % 24)
    return now.replace(minute=next_minute, second=0, microsecond=0)

def main():
    logging.info("[STARTUP] Deploy script started.")
    config = get_env_config()
    logging.info(f"Connecting to DB: host={config['DB_HOST']}, port={config['DB_PORT']}, user={config['DB_USER']}, db={config['DB_NAME']}")
    while True:
        total_greenhouses, greenhouse_ids = get_greenhouse_count(config)
        if total_greenhouses > 0:
            deploy_containers(total_greenhouses, greenhouse_ids, config)
        else:
            logging.warning("[SKIP] No greenhouses found. Skipping deployment.")
        next_run = get_next_run_time()
        sleep_seconds = (next_run - datetime.now()).total_seconds()
        logging.info(f"Next deployment at {next_run.strftime('%H:%M')}. Sleeping {sleep_seconds:.2f} seconds.")
        time.sleep(sleep_seconds)

if __name__ == "__main__":
    main()