

## 📦 Prerequisites
- Port Requirements
    - 1 for API
    - 1 for Frontend
    - 1 for Database (external DBMS tool)
    - 2 for MQTT (1 for normal, 1 for WebSocket)
- Docker
- Docker Compose
- MQTT: Ensure MQTT is installed to handle real-time messaging between the sensors and the backend. MQTT Installation Guide
- Access to the model files: `https://www.kaggle.com/models/luongchiduc/hdbtc_model`

## 🚀 Deployment Instruction

#### 0. After having having the full code go into ```docker-compose-setup/docker-compose.yml``` and change all the connected port to those on your server/machine

#### 1. Front-end 

Go into the Software folder of the git project that you pulled down earlier and do as follow:
- the web front end needs to change all its api links to the one your server/machine provided.
- Websocket listening link as well
- Rebuild the image: ```docker build -t *give it a tag* .```
- Go into docker-compose-setup/docker-compose.yml: find “projectb-container” under services and change it image from ```image: lickmya707/projectb:latest” to “image: *whatever tag you gave it*```

#### 2. Machine Learning Model Deployment

- The Model folder you downloaded from Kaggle must be placed in 
```bash 
docker-compose-setup/inference folder
```

- Build the inference image using 
```bash 
docker build --no-cache -t greenhouse-predictor:latest "your directory/docker-compose-setup/inference"
```
#### 3. Database Configuration

- Change your database login info and do the same for all other services in the ```docker-compose-setup/docker-conpose.yml```

- Do the same for all other files that get the database info in the docker-compose-setup folder and its subfolders

#### 4. Message Queue & Real-Time Data Handling
- if your server already has mqtt then you are ready and download it if your server does not have a native mqtt service running.

- When all the docker services are up and running after initializing docker compose, paste this message in your terminal outside of docker network and check the database in the sensor-data table to ensure MQTT is up and running correctly. Here is the message template:
```bash
mosquitto_pub -h localhost -p "your port that you bind it in docker-compose.yml" -t "greenhouse/1/sensor" -m '{
  "greenhouse_id": 1,
  "timestamp": "2025-03-31T09:15:00",
  "sensors": {
    "vent": { "VentLee": 6969, "VentWind": 6969 },
    "light": { "AssimLight": 6969, "Tot_PAR": 450, "Tot_PAR_Lamps": 6969 },
    "curtain": { "EnScr": 6969, "BlackScr": 6969 },
    "pipe": { "PipeLow": 6969, "PipeGrow": 6969 },
    "co2": { "co2air": 6969, "co2_dos": 6969 },
    "temperature_humidity": { "Tair": 28, "Rhair": 75 },
    "outside_TandH": { "Tout": 6969, "Rhout": 6969, "AbsHumOut": 6969 },
    "outside_wind": { "Windsp": 6969 },
    "outside_radiation": { "Iglob": 6969, "RadSum": 6969 }
  }
}'
```
### 5. Run All Services with Docker Compose

```bash
docker compose up -d --build
```

### 6. Close down all services(20 greenhouses/inference container)

```bash
docker stop greenhouse-predictor-then a number starting from 0
docker compose down --rmi all -v
```

#### 7. System Maintenance

- Logging: most logging is done by docker logs *container name* but there are 2 special one:
    - deploy-containers: ```docker exec -it deploy-containers tail -f /var/log/deploy_containers.log```
    - MQTT: it logs is saved in ```mosquitto/log/mosquitto.log```

- The AI model can be updated parallel to the running docker services, simply rebuilding the inference image after you update the model and wait till the next deployment is made automatically by deploy-containers container

- All other data, schema of the database is saved in the mysql folder inside docker-compose-setup folder

- After shutting down and running the compose a number of times, Docker can eat up a lot of memory with it image caching, shut the web down using this command :```docker-compose down --rmi all -v``` to start on a clean slate the next time you launch the web again

#### 8. Troubleshooting & Common Issues

- If you can't run ```docker compose up -d –build``` then you are most likely not in the docker-compose-setup folder where docker-compose.yml exist or you don't have docker compose installed yet

- If real time data is not working then chances are you have not configured your native MQTT for Websocket

- When using “docker compose down” command, it may run into the issue where the docker network cant be shut down, that is because you forgot to stop ```greenhouse-predictor-*a number*``` container,this is the inference container, it is built separately and brought into the project Docker network by deploy_containers container script.
