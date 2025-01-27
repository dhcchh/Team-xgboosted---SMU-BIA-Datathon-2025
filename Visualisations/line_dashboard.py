import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import os
import sys

# Ensure the correct path is set for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from visualization_utils.Linechart import line_builder

# Load datasets
df_news = pd.read_csv("Dataset/processed_news_2.csv")
df_news['source'] = 'news'

df_leaks = pd.read_csv("Dataset/processed_leaks_2.csv")
df_leaks['source'] = 'leaks'

# Combine datasets
combined_df = pd.concat([df_news, df_leaks], ignore_index=True)

# Convert boolean columns to integers for processing
category_columns = ['terrorism', 'security', 'espionage', 'communalism']
combined_df[category_columns] = combined_df[category_columns].astype(int)

# Ensure date columns are formatted correctly
combined_df['date'] = pd.to_datetime(combined_df[['year', 'month', 'day']], errors='coerce')

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the Dash app
app.layout = html.Div([
    html.H1("Threat Trends Over Time", style={'textAlign': 'center', 'color': 'white'}),
    
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
    
    html.Label("Select Category:", style={'color': 'white'}),
    dcc.Dropdown(
        id='category-dropdown',
        options=[{"label": cat.capitalize(), "value": cat} for cat in category_columns],
        value='terrorism',
        clearable=False,
        style={'width': '50%'}
    ),
    
    dcc.Graph(id='line-chart'),
], style={'backgroundColor': '#222222', 'padding': '20px'})

# Callback function to update line chart based on dropdown selections
@app.callback(
    Output('line-chart', 'figure'),
    [Input('source-dropdown', 'value'),
     Input('category-dropdown', 'value')]
)
def update_line_chart(selected_source, selected_category):
    # Get processed data from the line_builder function
    line_chart_data = line_builder(combined_df, selected_source, selected_category)

    # Create line chart
    fig = px.line(
        x=line_chart_data[0]['x'],
        y=line_chart_data[0]['y'],
        title=f"{selected_category.capitalize()} Trends in {selected_source.capitalize()} Data",
        labels={"x": "Time", "y": "Count"},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
