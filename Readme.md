## 📦 Prerequisites

- Docker
- Docker Compose
- Access to the model files: `https://www.kaggle.com/models/luongchiduc/hdbtc_model`

## 🚀 Quickstart

### 1. Build the Inference Docker Image
Download all the .pkl files in the Kaggle link then put it in /docker-compose-setup/inference/ directory
```bash
docker build --no-cache -t greenhouse-predictor:latest "your directory/docker-compose-setup/inference"
```

### 2. Pull the Web Frontend Image

```bash
docker pull lickmya707/projectb:latest
```

### 3. Run All Services with Docker Compose

```bash
docker compose up -d --build
```

### 4. Close down all services(20 greenhouses/inference container)

```bash
docker stop greenhouse-predictor-then a number starting from 0
docker compose down --rmi all -v
```

### Bonus Setup: Build and Push Web Frontend so i can get yours hehe
```bash
docker build -t lickmya707/projectb:latest .
docker push lickmya707/projectb:latest 
docker pull lickmya707/projectb:latest
```

### Bonus command: for checking deploy containers logs
```bash
docker exec -it deploy-containers tail -f /var/log/deploy_containers.log
```
the log for mosquitto is simply in /docker-compose-setup/mosquitto/log/mosquitto.log
the config for mosquitto is in /docker-compose-setup/mosquitto/config/mosquitto.conf