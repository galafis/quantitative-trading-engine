# 🚀 Deployment Guide

This guide covers deploying the Quantitative Trading Engine to various platforms.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Docker Deployment](#docker-deployment)
- [AWS Deployment](#aws-deployment)
- [Google Cloud Deployment](#google-cloud-deployment)
- [Azure Deployment](#azure-deployment)
- [Heroku Deployment](#heroku-deployment)
- [Production Checklist](#production-checklist)

## Prerequisites

Before deploying, ensure you have:

- ✅ All tests passing (`pytest`)
- ✅ Code properly formatted (`black`, `flake8`)
- ✅ Environment variables configured
- ✅ Database migrations ready
- ✅ SSL certificates (for production)

## Docker Deployment

### Local Docker Deployment

1. **Build and start containers:**
```bash
docker-compose up -d --build
```

2. **Check logs:**
```bash
docker-compose logs -f
```

3. **Access the API:**
```
http://localhost:8000/docs
```

### Docker Swarm Deployment

1. **Initialize swarm:**
```bash
docker swarm init
```

2. **Deploy stack:**
```bash
docker stack deploy -c docker-compose.yml trading-engine
```

3. **Check services:**
```bash
docker service ls
docker service logs trading-engine_api
```

### Docker Registry

1. **Tag image:**
```bash
docker tag quantitative-trading-engine:latest yourusername/trading-engine:latest
```

2. **Push to registry:**
```bash
docker push yourusername/trading-engine:latest
```

## AWS Deployment

### AWS ECS (Elastic Container Service)

#### 1. Setup ECR (Elastic Container Registry)

```bash
# Create ECR repository
aws ecr create-repository --repository-name trading-engine

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag and push image
docker tag trading-engine:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/trading-engine:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/trading-engine:latest
```

#### 2. Create ECS Task Definition

Create `task-definition.json`:
```json
{
  "family": "trading-engine",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/trading-engine:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://user:pass@rds-endpoint:5432/trading_db"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/trading-engine",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### 3. Create ECS Service

```bash
# Create cluster
aws ecs create-cluster --cluster-name trading-cluster

# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster trading-cluster \
  --service-name trading-service \
  --task-definition trading-engine \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

#### 4. Setup RDS for PostgreSQL

```bash
aws rds create-db-instance \
  --db-instance-identifier trading-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password <password> \
  --allocated-storage 20
```

#### 5. Setup ElastiCache for Redis

```bash
aws elasticache create-cache-cluster \
  --cache-cluster-id trading-cache \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1
```

### AWS Lambda (Serverless)

For serverless deployment with Lambda:

1. **Install Mangum:**
```bash
pip install mangum
```

2. **Update `app/main.py`:**
```python
from mangum import Mangum

# ... existing code ...

# Add Lambda handler
handler = Mangum(app)
```

3. **Deploy with AWS SAM:**
```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  TradingEngineFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.main.handler
      Runtime: python3.11
      CodeUri: .
      MemorySize: 512
      Timeout: 30
      Environment:
        Variables:
          DATABASE_URL: !Sub "postgresql://${DBUsername}:${DBPassword}@${DBEndpoint}:5432/trading_db"
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: ANY
```

```bash
sam build
sam deploy --guided
```

## Google Cloud Deployment

### Google Cloud Run

1. **Build and push to GCR:**
```bash
# Configure Docker for GCR
gcloud auth configure-docker

# Build image
docker build -t gcr.io/PROJECT-ID/trading-engine .

# Push to GCR
docker push gcr.io/PROJECT-ID/trading-engine
```

2. **Deploy to Cloud Run:**
```bash
gcloud run deploy trading-engine \
  --image gcr.io/PROJECT-ID/trading-engine \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL="postgresql://..." \
  --memory 1Gi
```

3. **Setup Cloud SQL:**
```bash
gcloud sql instances create trading-db \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=us-central1

gcloud sql databases create trading_db --instance=trading-db
```

### Google Kubernetes Engine (GKE)

1. **Create Kubernetes manifests:**

`deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: trading-engine
spec:
  replicas: 3
  selector:
    matchLabels:
      app: trading-engine
  template:
    metadata:
      labels:
        app: trading-engine
    spec:
      containers:
      - name: api
        image: gcr.io/PROJECT-ID/trading-engine:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: trading-secrets
              key: database-url
```

`service.yaml`:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: trading-engine-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: trading-engine
```

2. **Deploy to GKE:**
```bash
# Create cluster
gcloud container clusters create trading-cluster \
  --num-nodes=3 \
  --zone=us-central1-a

# Get credentials
gcloud container clusters get-credentials trading-cluster

# Deploy
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

## Azure Deployment

### Azure Container Instances

```bash
# Login to Azure
az login

# Create resource group
az group create --name trading-rg --location eastus

# Create container registry
az acr create --resource-group trading-rg --name tradingreg --sku Basic

# Build and push image
az acr build --registry tradingreg --image trading-engine:latest .

# Deploy container
az container create \
  --resource-group trading-rg \
  --name trading-engine \
  --image tradingreg.azurecr.io/trading-engine:latest \
  --dns-name-label trading-engine-app \
  --ports 8000 \
  --environment-variables DATABASE_URL="postgresql://..." \
  --cpu 1 \
  --memory 1
```

### Azure Kubernetes Service (AKS)

```bash
# Create AKS cluster
az aks create \
  --resource-group trading-rg \
  --name trading-aks \
  --node-count 3 \
  --enable-addons monitoring \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group trading-rg --name trading-aks

# Deploy (use same Kubernetes manifests as GKE)
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

## Heroku Deployment

1. **Create `Procfile`:**
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. **Create `runtime.txt`:**
```
python-3.11.0
```

3. **Deploy:**
```bash
# Login to Heroku
heroku login

# Create app
heroku create trading-engine-app

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis
heroku addons:create heroku-redis:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key"

# Deploy
git push heroku main

# Run migrations (if needed)
heroku run python -c "from app.core.database import engine, Base; Base.metadata.create_all(bind=engine)"

# Open app
heroku open
```

## Production Checklist

### Security
- [ ] Change default `SECRET_KEY` in `.env`
- [ ] Use strong database passwords
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set up firewall rules
- [ ] Use environment variables for all secrets
- [ ] Enable database encryption at rest

### Performance
- [ ] Configure database connection pooling
- [ ] Set up Redis caching
- [ ] Enable gzip compression
- [ ] Configure CDN for static files
- [ ] Set up load balancing
- [ ] Optimize database queries
- [ ] Add database indices

### Monitoring
- [ ] Set up logging (CloudWatch, Stackdriver, etc.)
- [ ] Configure alerts for errors
- [ ] Monitor API response times
- [ ] Track database performance
- [ ] Set up uptime monitoring
- [ ] Enable APM (Application Performance Monitoring)

### Backup & Recovery
- [ ] Automated database backups
- [ ] Backup retention policy
- [ ] Disaster recovery plan
- [ ] Test backup restoration
- [ ] Document recovery procedures

### CI/CD
- [ ] Automated testing pipeline
- [ ] Automated deployments
- [ ] Blue-green deployment strategy
- [ ] Rollback procedures
- [ ] Health checks configured

### Environment Variables

Essential environment variables for production:

```bash
# API
PROJECT_NAME="Quantitative Trading Engine"
VERSION="1.0.0"
API_V1_STR="/api/v1"

# Security
SECRET_KEY="<generate-secure-random-key>"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL="postgresql://user:password@host:5432/dbname"

# Redis
REDIS_URL="redis://host:6379"

# CORS
BACKEND_CORS_ORIGINS='["https://yourdomain.com"]'

# Trading
DEFAULT_INITIAL_CAPITAL=100000.0
DEFAULT_COMMISSION=0.001
DEFAULT_SLIPPAGE=0.0005
```

### SSL/HTTPS Setup

#### Using Let's Encrypt with Nginx

1. **Install Certbot:**
```bash
sudo apt-get install certbot python3-certbot-nginx
```

2. **Get certificate:**
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

3. **Nginx configuration:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Scaling Strategies

### Horizontal Scaling
- Multiple API instances behind load balancer
- Distributed database with read replicas
- Redis cluster for caching

### Vertical Scaling
- Increase CPU/memory for containers
- Upgrade database instance type
- Use faster storage (SSD/NVMe)

### Auto-scaling
```yaml
# Kubernetes HPA example
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: trading-engine-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: trading-engine
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Monitoring & Logging

### Logging Setup

```python
# app/core/logging.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler('app.log', maxBytes=10485760, backupCount=5),
            logging.StreamHandler()
        ]
    )
```

### Health Check Endpoint

Already implemented at `/health` - monitor this endpoint for service health.

## Support

For deployment assistance:
- 📧 Email: support@example.com
- 💬 GitHub Issues: [Issues](https://github.com/galafis/quantitative-trading-engine/issues)
- 📚 Documentation: [Docs](https://github.com/galafis/quantitative-trading-engine/tree/main/docs)
