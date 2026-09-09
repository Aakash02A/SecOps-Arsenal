# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# - nmap: required for basic-recon
# - tshark/libpcap: required for packet-sniffer
# - build-essential: required for compiling some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    nmap \
    tshark \
    libpcap-dev \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# By default, open a bash shell so users can run the CLI tools interactively
CMD ["/bin/bash"]
