#!/bin/bash

# Voyage Analysis - Flight Price Prediction Startup Script
# This script automates the setup and startup process

set -e  # Exit on error

echo "🚀 Starting Voyage Analysis - Flight Price Prediction Project"
echo "================================================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is running
echo -e "\n${YELLOW}Checking Docker...${NC}"
if ! docker ps > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker Desktop first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker is running${NC}"

# Navigate to project directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if required directories exist
echo -e "\n${YELLOW}Checking project structure...${NC}"
mkdir -p dags/data logs plugins
if [ ! -f "dags/data/flights.csv" ]; then
    echo -e "${RED}⚠️  Warning: dags/data/flights.csv not found${NC}"
    echo "Creating sample data file..."
    # You can add logic here to create sample data if needed
fi
echo -e "${GREEN}✓ Project structure verified${NC}"

# Start Docker Compose services
echo -e "\n${YELLOW}Starting Docker Compose services...${NC}"
docker-compose down > /dev/null 2>&1  # Clean up any existing containers
docker-compose up -d

# Wait for services to be ready
echo -e "\n${YELLOW}Waiting for services to start (30 seconds)...${NC}"
sleep 30

# Check service status
echo -e "\n${YELLOW}Checking service status...${NC}"
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✓ Services are running${NC}"
else
    echo -e "${RED}❌ Some services failed to start. Check logs with: docker-compose logs${NC}"
    exit 1
fi

# Install required Python packages
echo -e "\n${YELLOW}Installing required Python packages...${NC}"
echo "This may take a few minutes..."

# Install in scheduler
echo "Installing in scheduler..."
docker-compose exec -T airflow-scheduler python -m pip install --no-cache-dir scikit-learn pandas numpy > /dev/null 2>&1 || echo "⚠️  Scheduler package installation had issues"

# Install in webserver
echo "Installing in webserver..."
docker-compose exec -T airflow-webserver python -m pip install --no-cache-dir scikit-learn pandas numpy > /dev/null 2>&1 || echo "⚠️  Webserver package installation had issues"

# Install in worker
echo "Installing in worker..."
docker-compose exec -T airflow-worker python -m pip install --no-cache-dir scikit-learn pandas numpy > /dev/null 2>&1 || echo "⚠️  Worker package installation had issues"

echo -e "${GREEN}✓ Package installation completed${NC}"

# Verify DAG can be imported
echo -e "\n${YELLOW}Verifying DAG...${NC}"
if docker-compose exec -T airflow-scheduler python -c "from flight_price_prediction_dag import dag" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ DAG is valid${NC}"
else
    echo -e "${RED}❌ DAG has errors. Check with: docker-compose exec airflow-scheduler python -c 'from flight_price_prediction_dag import dag'${NC}"
fi

# Check Airflow health
echo -e "\n${YELLOW}Checking Airflow health...${NC}"
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Airflow is healthy${NC}"
else
    echo -e "${YELLOW}⚠️  Airflow may still be starting. Wait a bit longer.${NC}"
fi

# Final status
echo -e "\n${GREEN}================================================================"
echo "✅ Setup Complete!"
echo "================================================================"
echo ""
echo "📊 Access Airflow UI at: http://localhost:8080"
echo "   Username: airflow"
echo "   Password: airflow"
echo ""
echo "📋 Useful commands:"
echo "   View logs:    docker-compose logs -f"
echo "   Stop:         docker-compose down"
echo "   Status:       docker-compose ps"
echo "   Restart:      docker-compose restart"
echo ""
echo "📚 For detailed documentation, see: SETUP_GUIDE.md"
echo -e "${NC}"

