FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set the engine to run by default when the container starts
ENTRYPOINT ["python", "soar_engine.py"]
# Default arguments (can be overridden at runtime)
CMD ["sample_alerts.json", "-p", "playbooks.yaml"]
