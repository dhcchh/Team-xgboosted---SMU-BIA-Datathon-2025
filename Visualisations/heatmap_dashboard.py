import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import os
import sys

# Ensure the correct path for importing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from visualization_utils.WorldHeatMap import heatmap_builder

# Load datasets
LEAKS_DF = pd.read_csv("./Dataset/processed_leaks_2.csv")
NEWS_DF = pd.read_csv("./Dataset/processed_news_2.csv")

# Add source columns
LEAKS_DF['source'] = 'leaks'
NEWS_DF['source'] = 'news'

# Combine datasets
WORKING_DF = pd.concat([LEAKS_DF, NEWS_DF], ignore_index=True)

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Geospatial Threat Heatmap", style={'textAlign': 'center', 'color': 'white'}),

    html.Label("Select Data Source:", style={'color': 'white'}),
    dcc.Dropdown(
        id='source-dropdown',
        options=[
            {'label': 'News', 'value': 'news'},
            {'label': 'Leaks', 'value': 'leaks'}
        ],
        value='news',
        clearable=False,
        style={'width': '50%'}
    ),

    dcc.Graph(id='heatmap-graph'),
], style={'backgroundColor': '#222222', 'padding': '20px'})

# Callback to update heatmap based on dropdown selection
@app.callback(
    Output('heatmap-graph', 'figure'),
    [Input('source-dropdown', 'value')]
)
def update_heatmap(source):
    heatmap_fig = heatmap_builder(WORKING_DF, source)
    return heatmap_fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
