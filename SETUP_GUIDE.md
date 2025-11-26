# Voyage Analysis - MLOps in Travel - Complete Setup Guide

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [Initial Setup](#initial-setup)
5. [Running the Flight Price Prediction Component](#running-the-flight-price-prediction-component)
6. [Running Other Components](#running-other-components)
7. [Useful Commands](#useful-commands)
8. [Troubleshooting](#troubleshooting)
9. [Accessing Services](#accessing-services)

---

## 🎯 Project Overview

This project is an MLOps implementation for travel analytics with three main components:

1. **Flight Price Prediction** - Apache Airflow-based ML pipeline with automated data processing and model training
2. **Gender Classification Model** - Flask web application for gender classification
3. **Travel Recommendation Model** - Streamlit application for hotel recommendations

---

## 📦 Prerequisites

### Required Software
- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 1.29 or higher)
- **Python 3.8+** (for running Flask/Streamlit apps locally, optional)

### Verify Installation
```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker-compose --version

# Verify Docker is running
docker ps
```

### System Requirements
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: At least 5GB free
- **OS**: macOS, Linux, or Windows with WSL2

---

## 📁 Project Structure

```
voyage_analysis-Integrating-MLOps-in-Travel-main/
│
├── Flight Price Prediction/          # Main Airflow component
│   ├── dags/
│   │   ├── flight_price_prediction_dag.py
│   │   ├── data/
│   │   │   └── flights.csv
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── data_ingestion.py
│   │       ├── data_transformation.py
│   │       └── model_training.py
│   ├── docker-compose.yaml
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py                        # Flask web app (optional)
│
├── Gender Classification Model/
│   ├── app.py
│   └── (requires model files: scaler.pkl, pca.pkl, tuned_logistic_regression_model.pkl)
│
├── Travel Recommendation Model/
│   ├── app.py
│   └── (requires model file: cf_recommender.pkl)
│
└── SETUP_GUIDE.md                    # This file
```

---

## 🚀 Initial Setup

### Step 1: Navigate to Project Directory
```bash
cd "/Users/pankajkumaryadav/Desktop/Projects/voyage_analysis-Integrating-MLOps-in-Travel-main/Flight Price Prediction"
```

### Step 2: Verify Required Directories Exist
```bash
# Create directories if they don't exist
mkdir -p dags/data logs plugins

# Verify structure
ls -la dags/
ls -la dags/data/
```

### Step 3: Verify Data File Exists
```bash
# Check if flights.csv exists
ls -lh dags/data/flights.csv

# If missing, the file should contain flight data with columns:
# from, to, date, flightType, agency, distance, time, price
```

### Step 4: Start Docker Desktop
```bash
# On macOS
open -a Docker

# Wait for Docker to start (check with: docker ps)
```

---

## 🎯 Running the Flight Price Prediction Component

### Step 1: Start All Services
```bash
cd "Flight Price Prediction"
docker-compose up -d
```

This command will:
- Start PostgreSQL database
- Start Redis broker
- Initialize Airflow database
- Start Airflow webserver (port 8080)
- Start Airflow scheduler
- Start Airflow worker

### Step 2: Install Required Python Packages

The Airflow containers need scikit-learn, pandas, and numpy. Install them in all containers:

```bash
# Install in scheduler
docker-compose exec airflow-scheduler python -m pip install --no-cache-dir scikit-learn pandas numpy

# Install in webserver
docker-compose exec airflow-webserver python -m pip install --no-cache-dir scikit-learn pandas numpy

# Install in worker
docker-compose exec airflow-worker python -m pip install --no-cache-dir scikit-learn pandas numpy
```

**Note**: These packages need to be installed after each container restart. Consider creating a custom Docker image for persistence.

### Step 3: Verify Services Are Running
```bash
# Check container status
docker-compose ps

# Expected output should show all containers as "Up" or "Up (healthy)"
```

### Step 4: Check Airflow Health
```bash
# Check Airflow health endpoint
curl http://localhost:8080/health

# Or open in browser: http://localhost:8080
```

### Step 5: Access Airflow Web UI
1. Open browser: **http://localhost:8080**
2. Login credentials:
   - **Username**: `airflow`
   - **Password**: `airflow`

### Step 6: Enable and Trigger the DAG
1. In Airflow UI, find `flight_price_prediction_dag`
2. Toggle the switch on the left to **enable** the DAG
3. Click the **play button** (▶) to trigger manually
4. Or wait for scheduled run (daily at midnight)

---

## 🔧 Running Other Components

### Gender Classification Model (Flask App)

**Prerequisites**: Model files required (scaler.pkl, pca.pkl, tuned_logistic_regression_model.pkl)

```bash
cd "../Gender Classification Model"

# Install dependencies
pip install flask sentence-transformers scikit-learn pandas numpy joblib

# Run the app
python app.py

# Access at: http://localhost:8000
```

### Travel Recommendation Model (Streamlit App)

**Prerequisites**: Model file required (cf_recommender.pkl)

```bash
cd "../Travel Recommendation Model"

# Install dependencies
pip install streamlit pandas pickle5

# Run the app
streamlit run app.py

# Access at: http://localhost:8501
```

---

## 💻 Useful Commands

### Docker Compose Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart all services
docker-compose restart

# View logs
docker-compose logs -f airflow-webserver
docker-compose logs -f airflow-scheduler
docker-compose logs -f airflow-worker

# View logs for specific service (last 50 lines)
docker-compose logs --tail=50 airflow-scheduler

# Check service status
docker-compose ps

# Recreate containers (useful after config changes)
docker-compose up -d --force-recreate

# Stop and remove all containers, networks, and volumes
docker-compose down -v
```

### Docker Commands

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# View container logs
docker logs airflow_webserver
docker logs airflow_scheduler

# Execute command in container
docker-compose exec airflow-scheduler bash

# Check container resource usage
docker stats

# Remove all stopped containers
docker container prune
```

### Airflow-Specific Commands

```bash
# Test DAG import
docker-compose exec airflow-scheduler python -c "from flight_price_prediction_dag import dag; print('DAG OK')"

# List DAGs
docker-compose exec airflow-webserver airflow dags list

# Trigger DAG from command line
docker-compose exec airflow-webserver airflow dags trigger flight_price_prediction_dag

# Check DAG tasks
docker-compose exec airflow-webserver airflow tasks list flight_price_prediction_dag

# View task logs
docker-compose exec airflow-webserver airflow tasks logs flight_price_prediction_dag load_data_task 2024-01-01
```

### Python Package Management

```bash
# Install packages in scheduler
docker-compose exec airflow-scheduler python -m pip install --no-cache-dir <package-name>

# Install packages in webserver
docker-compose exec airflow-webserver python -m pip install --no-cache-dir <package-name>

# Install packages in worker
docker-compose exec airflow-worker python -m pip install --no-cache-dir <package-name>

# Install multiple packages at once
docker-compose exec airflow-scheduler python -m pip install --no-cache-dir scikit-learn pandas numpy
```

### File Operations

```bash
# Copy file to container
docker cp local_file.txt airflow-scheduler:/opt/airflow/dags/

# Copy file from container
docker cp airflow-scheduler:/opt/airflow/dags/file.txt ./

# View file in container
docker-compose exec airflow-scheduler cat /opt/airflow/dags/flight_price_prediction_dag.py
```

---

## 🔍 Troubleshooting

### Issue 1: Docker Daemon Not Running

**Symptoms**: `Cannot connect to the Docker daemon`

**Solution**:
```bash
# Start Docker Desktop
open -a Docker  # macOS
# or start Docker Desktop application manually

# Wait and verify
docker ps
```

### Issue 2: Port Already in Use

**Symptoms**: `Bind for 0.0.0.0:8080 failed: port is already allocated`

**Solution**:
```bash
# Find process using port 8080
lsof -i :8080  # macOS/Linux
netstat -ano | findstr :8080  # Windows

# Kill the process or change port in docker-compose.yaml
```

### Issue 3: DAG Not Appearing in UI

**Symptoms**: DAG doesn't show up in Airflow UI

**Solutions**:
```bash
# Check DAG file syntax
docker-compose exec airflow-scheduler python -c "from flight_price_prediction_dag import dag"

# Check scheduler logs
docker-compose logs airflow-scheduler | grep -i error

# Verify file exists
docker-compose exec airflow-scheduler ls -la /opt/airflow/dags/

# Restart scheduler
docker-compose restart airflow-scheduler
```

### Issue 4: ModuleNotFoundError

**Symptoms**: `ModuleNotFoundError: No module named 'sklearn'`

**Solution**:
```bash
# Install missing packages in all containers
docker-compose exec airflow-scheduler python -m pip install --no-cache-dir scikit-learn pandas numpy
docker-compose exec airflow-webserver python -m pip install --no-cache-dir scikit-learn pandas numpy
docker-compose exec airflow-worker python -m pip install --no-cache-dir scikit-learn pandas numpy
```

### Issue 5: Database Connection Error

**Symptoms**: `Can't connect to database`

**Solution**:
```bash
# Check PostgreSQL container
docker-compose ps postgres

# Check PostgreSQL logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres

# Wait for health check
docker-compose ps
```

### Issue 6: Import Errors in DAG

**Symptoms**: `ModuleNotFoundError: No module named 'dags'` or `No module named 'utils'`

**Solution**:
- Use relative imports: `from utils.data_ingestion import DataLoader`
- NOT: `from dags.utils.data_ingestion import DataLoader`
- The `/opt/airflow/dags/` directory is already in Python path

### Issue 7: Containers Keep Restarting

**Symptoms**: Containers show "Restarting" status

**Solution**:
```bash
# Check logs for errors
docker-compose logs airflow-scheduler
docker-compose logs airflow-webserver

# Stop and restart
docker-compose down
docker-compose up -d

# Check resource usage
docker stats
```

### Issue 8: Data File Not Found

**Symptoms**: `FileNotFoundError: flights.csv`

**Solution**:
```bash
# Verify file exists
ls -la dags/data/flights.csv

# Check file permissions
chmod 644 dags/data/flights.csv

# Verify mount in docker-compose.yaml
# Should have: - ./dags/data:/opt/airflow/dags/data
```

---

## 🌐 Accessing Services

### Airflow Web UI
- **URL**: http://localhost:8080
- **Username**: `airflow`
- **Password**: `airflow`

### PostgreSQL Database
- **Host**: localhost
- **Port**: 5432
- **Database**: airflow
- **Username**: airflow
- **Password**: airflow

### Redis
- **Host**: localhost
- **Port**: 6379

### Flask App (Gender Classification)
- **URL**: http://localhost:8000
- **Run**: `python app.py` in Gender Classification Model directory

### Streamlit App (Travel Recommendation)
- **URL**: http://localhost:8501
- **Run**: `streamlit run app.py` in Travel Recommendation Model directory

---

## 📝 Important Notes

### Package Installation Persistence
⚠️ **Important**: Python packages installed via `pip install` in containers are **NOT persistent**. They will be lost when containers are recreated. 

**Solutions**:
1. Reinstall packages after each `docker-compose down` and `docker-compose up`
2. Create a custom Dockerfile to build a custom Airflow image with packages pre-installed
3. Use `_PIP_ADDITIONAL_REQUIREMENTS` environment variable (may have compatibility issues)

### Data Persistence
- PostgreSQL data persists in Docker volumes
- Airflow logs are stored in `./logs/` directory
- DAG files are mounted from `./dags/` directory

### Performance Tips
- Allocate at least 4GB RAM to Docker
- Use SSD for better I/O performance
- Monitor container resource usage: `docker stats`

---

## 🔄 Quick Start Checklist

Use this checklist for quick setup:

- [ ] Docker Desktop is running
- [ ] Navigate to `Flight Price Prediction` directory
- [ ] Verify `dags/data/flights.csv` exists
- [ ] Run `docker-compose up -d`
- [ ] Wait 30-60 seconds for services to start
- [ ] Install packages: `docker-compose exec airflow-scheduler python -m pip install --no-cache-dir scikit-learn pandas numpy`
- [ ] Install packages in webserver and worker
- [ ] Verify services: `docker-compose ps`
- [ ] Open http://localhost:8080
- [ ] Login with airflow/airflow
- [ ] Enable `flight_price_prediction_dag`
- [ ] Trigger the DAG

---

## 📚 Additional Resources

### Airflow Documentation
- Official Docs: https://airflow.apache.org/docs/
- Docker Image: https://hub.docker.com/r/apache/airflow

### Project Files
- DAG File: `dags/flight_price_prediction_dag.py`
- Data File: `dags/data/flights.csv`
- Docker Compose: `docker-compose.yaml`

### Support
- Check logs: `docker-compose logs -f`
- Verify DAG: `docker-compose exec airflow-scheduler python -c "from flight_price_prediction_dag import dag"`
- Check health: `curl http://localhost:8080/health`

---

## 🎉 Success Indicators

You'll know everything is working when:
- ✅ All containers show "Up" status
- ✅ Airflow UI loads at http://localhost:8080
- ✅ `flight_price_prediction_dag` appears in DAG list (no "Broken DAG" error)
- ✅ DAG can be enabled and triggered
- ✅ Tasks complete successfully (green status)

---

**Last Updated**: November 2025
**Project**: Voyage Analysis - Integrating MLOps in Travel

