#!/bin/bash
# Startup script for Aria Bot (Linux/MacOS)

echo "=================================================="
echo "            Aria Bot Launcher"
echo "=================================================="
echo ""

# Navigate to script directory
cd "$(dirname "$0")"

# Check Docker
DOCKER_AVAILABLE=0
if command -v docker &> /dev/null && docker info &> /dev/null; then
    echo "[INFO] Docker is running."
    DOCKER_AVAILABLE=1
else
    echo "[INFO] Docker is NOT running or not installed."
fi

# Check Python
PYTHON_AVAILABLE=0
if command -v python3 &> /dev/null; then
    echo "[INFO] Python 3 is available."
    PYTHON_AVAILABLE=1
else
    echo "[INFO] Python 3 is NOT available."
fi

MODE=""
if [ "$DOCKER_AVAILABLE" -eq 1 ]; then
    echo "Docker detected. Recommended way to run."
    read -p "Run via [D]ocker or [L]ocal? (Default: D): " choice
    choice=${choice:-D}
    if [[ "$choice" =~ ^[Ll]$ ]]; then
        MODE="LOCAL"
    else
        MODE="DOCKER"
    fi
elif [ "$PYTHON_AVAILABLE" -eq 1 ]; then
    echo "Docker not available. Falling back to Local run."
    MODE="LOCAL"
else
    echo "[ERROR] Neither Docker nor Python 3 were found!"
    echo "Please install Docker Desktop OR Python 3.10+."
    exit 1
fi

if [ "$MODE" == "DOCKER" ]; then
    echo ""
    echo "[MODE] Docker"
    echo "Pulling latest image..."
    docker pull agent0ai/agent-zero

    echo "Starting Aria Bot container..."
    echo "Access the UI at http://localhost:50001"

    # Open browser (cross-platform attempt)
    if command -v xdg-open &> /dev/null; then
        sleep 2 && xdg-open http://localhost:50001 &
    elif command -v open &> /dev/null; then
        sleep 2 && open http://localhost:50001 &
    fi

    docker run -it -p 50001:80 -v "$(pwd):/a0" agent0ai/agent-zero

else
    echo ""
    echo "[MODE] Local"

    # Venv setup
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
        echo "Installing dependencies..."
        ./venv/bin/pip install --upgrade pip
        ./venv/bin/pip install -r requirements.txt
    else
        echo "Virtual environment found."
    fi

    echo "Starting Aria Bot..."
    echo "Access the UI at http://localhost:5000"

    # Open browser
    if command -v xdg-open &> /dev/null; then
        sleep 5 && xdg-open http://localhost:5000 &
    elif command -v open &> /dev/null; then
        sleep 5 && open http://localhost:5000 &
    fi

    ./venv/bin/python run_ui.py
fi
