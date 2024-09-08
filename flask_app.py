"""
A microservice that consumes data from external AP, transforms the data, and provides via new API endpoint.

THIS IS A STANDALONE FILE FOR NOW
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, jsonify
import os
import requests
from dash_weather import init_dashboard
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


app_blueprint = Blueprint('app_blueprint', __name__)
db = SQLAlchemy()



@app_blueprint.route('/')
def home():
    return 'Welcome to the Home Page!'


@app_blueprint.route('/about')
def about():
    return 'This is the ABOUT page.'


@app_blueprint.route('/weather/<city>')
def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("API key not found.  Please set OPENWEATER_API_KEY environmental variable.")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        print(response)
        if response.status_code == 200:
            data = response.json()
            return jsonify(data), 200
        else:
            print(f"Failed to retrieve data: {response.status_code}")
    except requests.RequestException as e:
        LOG.error(f"Request failed: {str(e)}")
        return jsonify({"error": "Request to weather API failed"}), 500

    data = response.json()
    return jsonify(data), 200

@app_blueprint.route('/weather-transformed/<city>')
def get_weather_transformed(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("API key not found.  Please set OPENWEATER_API_KEY environmental variable.")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({"error": "Unable to fetch weather data"}), 500

        data = response.json()

        # Transform the data
        transformed_data = {
            "city": data["name"],
            "temperature_celsius": data["main"]["temp"],
            "temperature_fahrenheit": data["main"]["temp"] * 9/5 + 32,  # Convert to Fahrenheit
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"]
        }

        # return jsonify(transformed_data), 200
        return jsonify(transformed_data), 200
    except Exception as e:
        LOG.error(f"Error with weather data transformation: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500



def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()

    # Import blueprints or routes
    flask_app.register_blueprint(app_blueprint)

    # Initialize the Dash app and pass flask app's server
    init_dashboard(flask_app)

    return flask_app


# Create/name the blueprint/Create blueprint object
# Server starts only if script is executed directly, not as module.
if __name__ == '__main__':
    try:
        app = create_app()
        # STARTS FLASK AND ENABLES DEBUG MODE
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        LOG.error((f"Error starting application: {str(e)}"))
