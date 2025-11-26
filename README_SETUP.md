# 🚀 Quick Start - Voyage Analysis Project

## Fastest Way to Start

### Option 1: Using the Startup Script (Recommended)
```bash
cd "Flight Price Prediction"
./start_project.sh
```

### Option 2: Manual Setup
```bash
# 1. Navigate to project
cd "Flight Price Prediction"

# 2. Start services
docker-compose up -d

# 3. Wait 30 seconds, then install packages
docker-compose exec airflow-scheduler python -m pip install --no-cache-dir scikit-learn pandas numpy
docker-compose exec airflow-webserver python -m pip install --no-cache-dir scikit-learn pandas numpy
docker-compose exec airflow-worker python -m pip install --no-cache-dir scikit-learn pandas numpy

# 4. Access Airflow UI
open http://localhost:8080
# Login: airflow / airflow
```

---

## 📚 Documentation Files

1. **SETUP_GUIDE.md** - Complete detailed setup guide with all steps
2. **QUICK_REFERENCE.md** - Quick command reference
3. **start_project.sh** - Automated startup script

---

## ⚡ Essential Commands

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Restart
docker-compose restart
```

---

## 🌐 Access Points

- **Airflow UI**: http://localhost:8080 (airflow/airflow)
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

---

## ⚠️ Important Notes

1. **Docker must be running** before starting
2. **Packages need to be reinstalled** after container restarts
3. **Wait 30-60 seconds** after `docker-compose up -d` for services to initialize
4. **Check logs** if something doesn't work: `docker-compose logs -f`

---

## 🆘 Quick Troubleshooting

**DAG not showing?**
```bash
docker-compose restart airflow-scheduler
```

**Module not found?**
```bash
docker-compose exec airflow-scheduler python -m pip install --no-cache-dir scikit-learn pandas numpy
```

**Containers not starting?**
```bash
docker-compose down
docker-compose up -d
```

---

For complete documentation, see **SETUP_GUIDE.md**

