# Weather Dashboard Microservice

## Overview
This project is a Flask-based microservice that consumes weather data from the OpenWeather API, processes the data, and provides it via new API endpoints. It also includes a dashboard built with Plotly and Dash to visualize the weather data, offering graphs for temperature, humidity, and wind speed.

# Substack
I'm writing blog posts about this API and data visualization test bed project.  

- The Dashing Weather Dashboard - https://substack.com/@jonathanrooke/p-149481181
- Digging Dash - https://substack.com/@jonathanrooke/p-149465357

### Features:
- Real-time weather data for selected cities
- Dynamic city selection via a dropdown menu
- Plotly-based graphs for temperature, humidity, and wind speed
- Dockerized application for easy deployment and portability

## Table of Contents
1. [Setup](#setup)
2. [Configuration](#configuration)
3. [Running the Application](#running-the-application)
4. [Docker Build and Run](#docker-build-and-run)
5. [Creating a Wheel File](#creating-a-wheel-file)
6. [Endpoints](#endpoints)
7. [License](#license)

## Setup

### Prerequisites:
- Python 3.6+
- OpenWeather API Key (You'll need to sign up for an API key at https://openweathermap.org/api)
- Optional: Docker installed on your machine

### Install Dependencies
1. Clone the repository:
    ```bash
    git clone https://github.com/jdrgithub/check_the_weather.git
    cd check_the_weather
    ```
2. Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Set the `OPENWEATHER_API_KEY` environment variable:
    ```bash
    export OPENWEATHER_API_KEY=your_api_key
    ```
4. Run the Flask application:
    ```bash
    python flask_app.py
    ```

### Environment Variables:
- **OPENWEATHER_API_KEY**: Your OpenWeather API key is required to fetch weather data. Set it in your terminal or use a `.env` file with a tool like `python-dotenv` to manage it.

## Running the Application

Once the app is running, it can be accessed at `http://localhost:5000`.

### Endpoints:
1. **Landing Page (`/`)**:
   - Main page with a dropdown to select a city and view its weather data.

2. **Current Weather (`/weather`)**:
   - Fetches and displays the current weather data for the selected city.

3. **Interactive Dashboard (`/dashboard`)**:
   - A dynamic Dash-based dashboard that provides interactive graphs for weather forecasts, including temperature, humidity, and wind speed.

## Docker Build and Run

To run the application in a Docker container, follow these steps:

1. Build the Docker image:
    ```bash
    docker build --build-arg OPENWEATHER_API_KEY=your_api_key -t weather_dashboard .
    ```
2. Run the Docker container:
    ```bash
    docker run -p 5000:5000 weather_dashboard
    ```
   The app will be accessible at `http://localhost:5000`.

## Creating a Wheel File

To build a Python wheel file for this project, follow these steps:

1. **Clone the repository** (if not already cloned):
    ```bash
    git clone https://github.com/jdrgithub/check_the_weather.git
    cd check_the_weather
    ```

2. **Install necessary build tools**:
    ```bash
    pip install setuptools wheel
    ```

3. **Build the wheel**:
    ```bash
    python setup.py bdist_wheel
    ```

4. **Find the wheel file** in the `dist/` directory:
    ```bash
    dist/your_project-0.1.0-py3-none-any.whl
    ```

5. **Optional - Install the wheel file locally** to test it:
    ```bash
    pip install dist/your_project-0.1.0-py3-none-any.whl
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
tall -r requirements.txt
3. Set the `OPENWEATHER_API_KEY` environment variable:
    export OPENWEATHER_API_KEY=your_api_key
4. Run the Flask application:
    python flask_app.py

### Environment Variables:
- **OPENWEATHER_API_KEY**: Your OpenWeather API key is required to fetch weather data.
You can set the environment variable in your terminal, or use a `.env` file and a tool like [python-dotenv](https://github.com/theskumar/python-dotenv) to manage it.

### Running the Application
Once the app is up and running, you can access it at `http://localhost:5000`.

### Endpoints:
- `/`: Landing page with, at the moment, has one dropdown to select a city.
- `/weather`: Fetches the weather data for the selected city.
- `/dashboard`: A dashboard built with Dash that provides interactive weather visualizations.

## Docker Build and Run
To run the application in a Docker container, follow these steps:

### Build the Docker Image:
1. Make sure your `Dockerfile` is correctly configured with the `OPENWEATHER_API_KEY` argument:
- docker build --build-arg OPENWEATHER_API_KEY=your_api_key -t weather_dashboard .
2. Expose port 5000 and run the container:
- docker run -p 5000:5000 weather_dashboard
The application will now be accessible at http://localhost:5000.

## Building a Wheel File:
To create a wheel file for this project, follow these steps:

### Clone the repository:
git clone https://github.com/jdrgithub/check_the_weather.git
cd check_the_weather

### Install the required tools: You need setuptools and wheel to build the wheel file. You can install them using pip:
- pip install setuptools wheel

### Build the wheel: 
Run the following command in the root directory of the project (where setup.py is located) to build the wheel file:
- python setup.py bdist_wheel

### Find the wheel file: 
After running the build command, the .whl file will be generated in the dist/ directory:
- dist/your_project-0.1.0-py3-none-any.whl

### Install the wheel file locally (optional): 
You can install the wheel file locally to test it using pip:
- pip install dist/your_project-0.1.0-py3-none-any.whl









