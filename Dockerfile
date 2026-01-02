FROM python:3.11-slim

RUN apt-get update && apt-get install -y git ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the image
COPY . .

# Launch the web UI
CMD ["python", "run_ui.py"]
