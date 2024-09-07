import os
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
import pandas as pd

# Function to fetch weather data
def fetch_weather_data(city, forecast_hours):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    response = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric")
    data = response.json()
    df = pd.DataFrame(data['list'][:forecast_hours], columns=['dt_txt', 'main'])
    df['time'] = pd.to_datetime(df['dt_txt'])
    df['temperature'] = df['main'].apply(lambda x: x['temp'])
    return df
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
                'title': 'Temperature Forecast'
            }
        }

    return dash_app
