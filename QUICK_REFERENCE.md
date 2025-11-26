# Quick Reference Guide - Voyage Analysis Project

## 🚀 Quick Start Commands

### Start Project
```bash
cd "Flight Price Prediction"
docker-compose up -d
```

### Install Required Packages (After Each Restart)
```bash
docker-compose exec airflow-scheduler python -m pip install --no-cache-dir scikit-learn pandas numpy
docker-compose exec airflow-webserver python -m pip install --no-cache-dir scikit-learn pandas numpy
docker-compose exec airflow-worker python -m pip install --no-cache-dir scikit-learn pandas numpy
```

### Check Status
```bash
docker-compose ps
curl http://localhost:8080/health
```

### Stop Project
```bash
docker-compose down
```

---

## 🔧 Common Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f airflow-scheduler
docker-compose logs -f airflow-webserver
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart airflow-scheduler
```

### Test DAG
```bash
docker-compose exec airflow-scheduler python -c "from flight_price_prediction_dag import dag; print('OK')"
```

### Access Container Shell
```bash
docker-compose exec airflow-scheduler bash
```

---

## 🌐 Access URLs

- **Airflow UI**: http://localhost:8080 (airflow/airflow)
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

---

## ⚠️ Troubleshooting Quick Fixes

### DAG Not Showing
```bash
docker-compose restart airflow-scheduler
```

### Module Not Found
```bash
docker-compose exec airflow-scheduler python -m pip install --no-cache-dir <package>
```

### Containers Not Starting
```bash
docker-compose down
docker-compose up -d
```

### Check Container Logs
```bash
docker-compose logs airflow-scheduler | tail -50
```

---

## 📋 Service Status Check
```bash
# Check all containers
docker-compose ps

# Check specific container
docker ps | grep airflow

# Check resource usage
docker stats
```

---

## 🔄 Full Reset (If Everything Breaks)
```bash
# Stop and remove everything
docker-compose down -v

# Remove all containers
docker container prune -f

# Restart fresh
docker-compose up -d

# Reinstall packages
docker-compose exec airflow-scheduler python -m pip install --no-cache-dir scikit-learn pandas numpy
docker-compose exec airflow-webserver python -m pip install --no-cache-dir scikit-learn pandas numpy
docker-compose exec airflow-worker python -m pip install --no-cache-dir scikit-learn pandas numpy
```

