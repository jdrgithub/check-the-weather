"""
A microservice that consumes data from external AP, transforms the data, and provides via new API endpoint.

THIS IS A STANDALONE FILE FOR NOW
"""
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, jsonify, render_template_string
import os
import requests
from dash_weather import init_dashboard
import logging
import plotly.graph_objs as go
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

formatted_date = datetime.now().strftime("%a, %b %d, %Y at %I:%M%p")

weekday = datetime.now().strftime("%a")

app_blueprint = Blueprint('app_blueprint', __name__)
db = SQLAlchemy()


@app_blueprint.route('/')
def index():
    return render_template('index.html')


@app_blueprint.route('/about')
def about():
    return 'This is the ABOUT page'


@app_blueprint.route('/weather', methods=['GET', 'POST'])
def get_weather():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("API key not found for /weather.  Please set OPENWEATHER_API_KEY environmental variable.")

    # DEFAULT TO NEW YORK
    if request.method == 'POST':
        city = request.form.get('city', 'New York')
    else:
        city = 'New York'  # Default when page loads first time

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

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


        # Render HTML with Flexbox and limited width for each graph
        html_template = '''
        <html>
            <head>
                <title>Weather in {{ city }}</title>
                <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script> <!-- Include Plotly JS -->
                <style>
                    body {
                        margin: 1 auto;  /* Center the content */
                        max-width: 820px;  /* Limit the overall width of the page */
                        padding: 40px;  /* Add padding for side margins */
                        font-family: 'Roboto', sans-serif;  /* Apply Montserrat font */
                    } 
                    .graph-container {
                        display: flex;
                        flex-wrap: wrap;
                        justify-content: space-between;
                        background-color: #132534;
                    }
                    .graph {
                        flex: 1 1 20%;  /* Control the flex width (30% of the container) */
                        max-width: 240px;  /* Limit the maximum width of each graph */
                        padding: 10px;
                        margin: 10px;
                        height: 450px; /* Adjust height to make the divs smaller */
                        background-color: #708090
                        border-radius: 10px;
                    }
                    h1 {
                        text-align: center;
                        font-size: 45;
                        padding: 0;
                        margin: 0;
                        font-family: 'Roboto', sans-serif;  /* Apply Montserrat font */
                    }
                    h3 {
                        text-align: center;
                        padding: 0;
                        margin: 0;
                        font-size: 25;
                        font-family: 'Roboto', sans-serif;  /* Apply Montserrat font */
                    }
                </style>
            </head>
            <body style="background-color:#132534;"> 
                <h1 style="color:white;">{{ city }} Weather</h1>
                <h3 style="color:grey;">{{current_datetime}}</h3>
                <div class="graph-container">
                    <div class="graph">
                        {{ graph_html1|safe }}
                    </div>
                    <div class="graph">
                        {{ graph_html2|safe }}
                    </div>
                    <div class="graph">
                        {{ graph_html3|safe }}
                    </div>
                </div>
            </body>
        </html>
        '''

        return render_template_string(html_template, city=city_name, current_datetime=formatted_date, graph_html1=graph_html1, graph_html2=graph_html2, graph_html3=graph_html3)

    except Exception as e:
        LOG.error(f"Error fetching weather data: {str(e)}")
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
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        LOG.error((f"Error starting application: {str(e)}"))
