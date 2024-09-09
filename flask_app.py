"""
A microservice that consumes data from external AP, transforms the data, and provides via new API endpoint.

THIS IS A STANDALONE FILE FOR NOW
"""
from flask import Flask, request, render_template, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import requests
from dash_weather import init_dashboard
import logging
import plotly.graph_objs as go
from datetime import datetime

# GET KEY FROM ENV VAR
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast'

# SETUP LOGGING
LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Datetime
formatted_date = datetime.now().strftime("%a, %b %d, %Y at %I:%M%p")
weekday = datetime.now().strftime("%a")

# REGISTER BLUEPRINT
app = Blueprint('app', __name__)
# INSTANTIATE SQLALCHEMY
db = SQLAlchemy()


# JUMP PAGE
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return 'This is the ABOUT page'


# GET WEATHER -> GETS CURRENT WEATHER
@app.route('/weather', methods=['GET', 'POST'])
def get_weather():
    if not API_KEY:
        raise ValueError("API key not found for /weather.  Please set OPENWEATHER_API_KEY environmental variable.")

    # DEFAULT TO NEW YORK
    if request.method == 'POST':
        city = request.form.get('city', 'New York')
    else:
        city = 'New York'  # Default when page loads first time

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to retrieve weather data"}), response.status_code
        data = response.json()

        # Extract data for the graph
        city_name = data["name"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        # 1. HUMIDITY GRAPH
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=["Humidity"],
            y=[humidity],
            name="Humidity",
            marker=dict(color=['#7393B3']),   # Custom color for cloud level
            width=0.5
        ))
        fig1.update_layout(
            title="HUMIDITY",
            title_x=0.5,
            yaxis_title="PERCENTAGE (%)",
            xaxis_title="Humidity",
            xaxis_title_standoff=20,
            xaxis=dict(
                showticklabels=False,
                title_font=dict(size=12)
            )
        )
        graph_html1 = fig1.to_html(full_html=False, include_plotlyjs=False)

        # 2. TEMPERATURE GRAPH
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=["Temperature (°C)"],
            y=[temperature],
            name="Temperature",
            marker=dict(color='#7293cb'),
            width=0.5
        ))
        fig2.update_layout(
            title="TEMPERATURE",
            title_x=0.5,
            yaxis_title="Degrees Celsius (°C)",
            xaxis_title="Temperature",
            xaxis_title_standoff=20,
            xaxis=dict(
                showticklabels=False,
                title_font=dict(size=12)
            )
        )
        graph_html2 = fig2.to_html(full_html=False, include_plotlyjs=False)

        # 3. WIND SPEED GRAPH
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=["Wind Speed (m/s)"],
            y=[wind_speed],
            name="Wind Speed",
            marker=dict(color='#6082B6'),
            width=0.6
        ))
        fig3.update_layout(
            title='WIND SPEED',
            title_x=0.5,
            yaxis_title="Meters per second (m/s)",
            xaxis_title="Wind Speed",
            xaxis_title_standoff=20,
            xaxis=dict(
                showticklabels=False,
                title_font=dict(size=12)
            )
        )
        graph_html3 = fig3.to_html(full_html=False, include_plotlyjs=False)

        return render_template(
            'weather_today.html',
            city=city_name,
            current_datetime=formatted_date,
            graph_html1=graph_html1,
            graph_html2=graph_html2,
            graph_html3=graph_html3
        )

    except Exception as e:
        LOG.error(f"Error fetching weather data: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/hourly_forecast', methods=['POST'])
def hourly_forecast():
    city = request.form.get('city', 'New York')
    print(city)


# Get forecast data from OpenWeather API
def get_openweather_forecast(timeframe, city='New York'):
    # Request the weather data for the city
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'fahrenheit',  # Use 'imperial' for Fahrenheit
    }
    response = requests.get(BASE_URL, params=params)

    # Parse the JSON data from OpenWeather
    if response.status_code == 200:
        weather_data = response.json()

        if timeframe == 'next_hour':
            # Get the forecast for the next hour
            return weather_data['list'][0]['weather'][0]['description'], weather_data['list'][0]['main']['temp']

        elif timeframe == 'next_4_hours':
            # Get the forecast for the next 4 hours (OpenWeather provides 3-hour intervals)
            return weather_data['list'][1]['weather'][0]['description'], weather_data['list'][1]['main']['temp']

        elif timeframe == 'next_day':
            # Get the forecast for the next 24 hours (approximately 8 intervals of 3 hours)
            return weather_data['list'][8]['weather'][0]['description'], weather_data['list'][8]['main']['temp']

        elif timeframe == 'next_3_days':
            # Get the forecast for the next 3 days (approximately 24 intervals of 3 hours)
            return weather_data['list'][24]['weather'][0]['description'], weather_data['list'][24]['main']['temp']
    else:
        return "Error fetching data from OpenWeather", None


# Route to handle forecast requests
@app.route('/forecast', methods=['POST'])
def display_forecast():
    selected_timeframe = request.form['timeframe']

    # Fetch forecast from OpenWeather API based on the selected timeframe
    forecast_description, forecast_temp = get_openweather_forecast(selected_timeframe)

    if forecast_temp is not None:
        forecast = f"{forecast_description.capitalize()} with a temperature of {forecast_temp}°C."
    else:
        forecast = forecast_description  # Error message in case of API failure

    # Render the forecast page with the selected forecast
    return render_template('forecast.html', forecast=forecast)


def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()

    # Import blueprints or routes
    flask_app.register_blueprint(app)

    # Initialize the Dash app and pass flask app's server
    init_dashboard(flask_app)

    return flask_app


# Create/name the blueprint/Create blueprint object
# Server starts only if script is executed directly, not as module.
if __name__ == '__main__':
    try:
        app = create_app()
        # STARTS FLASK AND ENABLES DEBUG MODE
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        LOG.error(f"Error starting application: {str(e)}")
