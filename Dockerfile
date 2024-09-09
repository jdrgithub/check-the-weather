# Use Alpine as the base image
FROM python:3.9-slim

ARG OPENWEATHER_API_KEY
# Set the environment variable to pass the ARG value to the runtime environment
# ARG is safer for sensitive values like API keys because they’re not stored in the final image
ENV OPENWEATHER_API_KEY=$OPENWEATHER_API_KEY

# Set environment variable to avoid interactive prompts during package installs
ENV DEBIAN_FRONTEND=noninteractive

# FLASK RUNS ON LOCALHOST:5000
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

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
