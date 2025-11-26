# Ports Reference Guide - Voyage Analysis Project

This document lists all ports used by the services in this project for easy reference.

---

## 🌐 Application Ports

### Flight Price Prediction (Flask App)
- **Port**: `5001`
- **URL**: http://localhost:5001
- **Service**: Flask web application
- **Status**: Changed from 5000 to 5001 (5000 is used by macOS AirPlay Receiver)
- **Command to start**: `cd "Flight Price Prediction" && python app.py`

### Gender Classification (Flask App)
- **Port**: `8000`
- **URL**: http://localhost:8000
- **Service**: Flask web application
- **Command to start**: `cd "Gender Classification Model" && python app.py`

### Travel Recommendation (Streamlit App)
- **Port**: `8501`
- **URL**: http://localhost:8501
- **Service**: Streamlit web application
- **Command to start**: `cd "Travel Recommendation Model" && streamlit run app.py`

---

## 🐳 Docker Services (Airflow)

### Airflow Web UI
- **Port**: `8080`
- **URL**: http://localhost:8080
- **Service**: Apache Airflow webserver
- **Default Credentials**:
  - Username: `airflow`
  - Password: `airflow`
- **Command to start**: `cd "Flight Price Prediction" && docker-compose up -d`

### PostgreSQL Database
- **Port**: `5432`
- **Host**: localhost
- **Service**: PostgreSQL database for Airflow
- **Connection Details**:
  - Database: `airflow`
  - Username: `airflow`
  - Password: `airflow`
- **Access**: Only accessible from Docker network (not exposed externally by default)

### Redis Broker
- **Port**: `6379`
- **Host**: localhost
- **Service**: Redis message broker for Airflow Celery
- **Access**: Only accessible from Docker network (not exposed externally by default)

---

## 📋 Quick Port Reference Table

| Service | Port | Protocol | Access | Notes |
|---------|------|----------|--------|-------|
| Flight Price Prediction | 5001 | HTTP | http://localhost:5001 | Flask app |
| Gender Classification | 8000 | HTTP | http://localhost:8000 | Flask app |
| Travel Recommendation | 8501 | HTTP | http://localhost:8501 | Streamlit app |
| Airflow Web UI | 8080 | HTTP | http://localhost:8080 | Airflow webserver |
| PostgreSQL | 5432 | TCP | localhost:5432 | Database (internal) |
| Redis | 6379 | TCP | localhost:6379 | Message broker (internal) |

---

## 🔍 Port Checking Commands

### Check if a port is in use:
```bash
# macOS/Linux
lsof -i :PORT_NUMBER

# Example: Check port 5001
lsof -i :5001

# Check multiple ports
lsof -i :5001,8000,8501,8080
```

### Check what's listening on ports:
```bash
# List all listening ports
lsof -i -P | grep LISTEN

# Check specific ports
netstat -an | grep LISTEN | grep -E "5001|8000|8501|8080"
```

### Kill process on a port:
```bash
# Find and kill process on port
lsof -ti:PORT_NUMBER | xargs kill -9

# Example: Kill process on port 5001
lsof -ti:5001 | xargs kill -9
```

---

## ⚠️ Common Port Conflicts

### Port 5000
- **Issue**: Used by macOS AirPlay Receiver by default
- **Solution**: Flight Price Prediction app uses port 5001 instead
- **To free port 5000**: System Settings → General → AirDrop & Handoff → Turn off AirPlay Receiver

### Port 8080
- **Common conflicts**: Other web servers, Jenkins, Tomcat
- **Solution**: Change Airflow port in `docker-compose.yaml` if needed

### Port 5432 (PostgreSQL)
- **Common conflicts**: Other PostgreSQL instances
- **Solution**: Change port in `docker-compose.yaml` if needed

---

## 🚀 Starting Services with Port Verification

### Before starting, check ports:
```bash
# Check all project ports
lsof -i :5001,8000,8501,8080,5432,6379
```

### Start services in order:
1. **Docker services** (Airflow):
   ```bash
   cd "Flight Price Prediction"
   docker-compose up -d
   # Wait 30-60 seconds
   ```

2. **Flask apps**:
   ```bash
   # Terminal 1 - Flight Price Prediction
   cd "Flight Price Prediction"
   python app.py
   
   # Terminal 2 - Gender Classification
   cd "Gender Classification Model"
   python app.py
   ```

3. **Streamlit app**:
   ```bash
   # Terminal 3 - Travel Recommendation
   cd "Travel Recommendation Model"
   streamlit run app.py
   ```

---

## 🛑 Stopping Services

### Stop all Flask apps:
```bash
pkill -f "app.py"
```

### Stop Streamlit:
```bash
pkill -f streamlit
```

### Stop Docker containers:
```bash
cd "Flight Price Prediction"
docker-compose down
```

### Stop everything at once:
```bash
pkill -f "app.py"
pkill -f streamlit
cd "Flight Price Prediction" && docker-compose down
```

---

## 📝 Port Change Instructions

If you need to change any port:

### Flask Apps:
Edit the `app.py` file and change:
```python
app.run(host="0.0.0.0", port=PORT_NUMBER)
```

### Streamlit:
```bash
streamlit run app.py --server.port=PORT_NUMBER
```

### Docker/Airflow:
Edit `docker-compose.yaml`:
```yaml
ports:
  - "NEW_PORT:8080"  # Change NEW_PORT to desired port
```

---

## 🔐 Security Notes

- **Ports 5432 and 6379** are only accessible from Docker network (not exposed to host by default)
- **Ports 5001, 8000, 8501, 8080** are exposed to localhost
- For production, consider:
  - Using reverse proxy (nginx)
  - Implementing authentication
  - Using HTTPS
  - Restricting access to localhost only

---

## 📚 Additional Resources

- **Docker ports**: Check `docker-compose.yaml` in Flight Price Prediction directory
- **Service status**: Use `docker-compose ps` to see running containers
- **Process status**: Use `ps aux | grep app.py` or `ps aux | grep streamlit`

---

**Last Updated**: November 2025
**Project**: Voyage Analysis - Integrating MLOps in Travel

