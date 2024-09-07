import os
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import requests
import pandas as pd

# Function to fetch weather data
def fetch_weather_data(city, forecast_hours):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("API key not found.  Please set OPENWEATER_API_KEY environmental variable.")
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

    # MAKE API REQUEST TO OPENWEATHERMAP
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code}")

    data = response.json()

    # EXTRACT TIME AND TEMP FROM FORECAST DATA
    forecast_list = data['list'][:forecast_hours] # get forecast for specified hours
    forecast_data = []

    for forecast in forecast_list:
        forecast_data.append({
            'time': forecast['dt_txt'], # timestand of forecast
            'temperature': forecast['main']['temp'], # temp in celsius
            'humidity': forecast['main']['humidity'], # humidity percentage
            'wind_speed': forecast['wind']['speed'], # windspeed in meters/sec
            'description': forecast['weather'][0]['description'] # weather description
        })

    # CONVERT FORECAST DATA INTO A DATAFRAME
    df = pd.DataFrame(forecast_data)
    df['time'] = pd.to_datetime(df['time']) # convert the time

    return df

   # A PREVIOUS OUTPUT
    # df = pd.DataFrame(data['list'][:forecast_hours], columns=['dt_txt', 'main'])
    # df['time'] = pd.to_datetime(df['dt_txt'])
    # df['temperature'] = df['main'].apply(lambda x: x['temp'])

def init_dashboard(server):
    dash_app = Dash(__name__, server=server, routes_pathname_prefix='/dashboard/')

    # Set up the layout
    dash_app.layout = html.Div([
        html.H1('Weather Dashboard'),
        dcc.Dropdown(
            id='city-dropdown',
            options=[
                {'label': 'New York', 'value': 'New York'},
                {'label': 'London', 'value': 'London'},
                {'label': 'Tokyo', 'value': 'Tokyo'}
            ],
            value='New York'
        ),
        dcc.Graph(id='temp-graph'),
        dcc.Slider(
            id='forecast-slider',
            min=0,
            max=48,
            value=24,
            marks={i: f'{i}h' for i in range(0, 49, 3)},
            step=3
        )
    ])


    # Define callback to update the graph
    @dash_app.callback(
        Output('temp-graph', 'figure'),
        [Input('city-dropdown', 'value'),
         Input('forecast-slider', 'value')]
    )
    def update_graph(selected_city, forecast_hours):
        df = fetch_weather_data(selected_city, forecast_hours)
        return {
            'data': [{
                'x': df['time'],
                'y': df['temperature'],
                'type': 'line',
                'name': selected_city,
            }],
            'layout': {
                'title': f'Temperature Forecast for {selected_city} (Next {forecast_hours} Hours)',
                'xaxis': {'title': 'Time'},
                'yaxis': {'title': 'Temperature (C)'},
            }
        }

    return dash_app
