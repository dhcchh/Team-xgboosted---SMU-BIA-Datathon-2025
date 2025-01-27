import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import os
import sys

# Ensure the correct path is set for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from visualization_utils.Piechart import piechart_builder

# Load datasets
df_news = pd.read_csv("Dataset/processed_news_2.csv")
df_news['source'] = 'news'

df_leaks = pd.read_csv("Dataset/processed_leaks_2.csv")
df_leaks['source'] = 'leaks'

# Combine datasets
combined_df = pd.concat([df_news, df_leaks], ignore_index=True)

# Convert boolean columns to integers to ensure correct aggregation
category_columns = ['terrorism', 'security', 'espionage', 'communalism']
combined_df[category_columns] = combined_df[category_columns].astype(int)

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the Dash app
app.layout = html.Div([
    html.H1("Threat Category Distribution", style={'textAlign': 'center', 'color': 'white'}),
    
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
    
    dcc.Graph(id='pie-chart'),
], style={'backgroundColor': '#222222', 'padding': '20px'})

# Callback function to update pie chart based on dropdown selection
@app.callback(
    Output('pie-chart', 'figure'),
    Input('source-dropdown', 'value')
)
def update_pie_chart(selected_source):
    pie_chart_data = piechart_builder(combined_df, selected_source)
    labels = pie_chart_data[0]["labels"]
    values = pie_chart_data[0]["values"]

    # Create pie chart
    fig = px.pie(
        names=labels,
        values=values,
        title=f"Category Distribution for {selected_source.capitalize()} Data",
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
