FROM python:3.14-slim

# Create a non-root user for security
RUN groupadd -r soar && useradd -r -g soar soar

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Switch to non-root user
USER soar

# Set the engine to run by default when the container starts
ENTRYPOINT ["python", "soar_engine.py"]
# Default arguments (can be overridden at runtime)
CMD ["sample_alerts.json", "-p", "playbooks.yaml"]
