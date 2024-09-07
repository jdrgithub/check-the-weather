# Use Alpine as the base image
FROM python:3.9-slim

ARG OPENWEATHER_API_KEYBAS

# Set environment variable to avoid interactive prompts during package installs
ENV DEBIAN_FRONTEND=noninteractive

# Install system tools (net-tools, procps, curl, iputils)
RUN apt-get update && apt-get install -y --no-install-recommends \
    net-tools \
    procps \
    iproute2 \
    curl \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container (for Dash)
EXPOSE 5000

# Command to run the app when the container starts
CMD ["python", "flask_app.py"]
