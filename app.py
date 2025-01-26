import json
import dash
import dash_cytoscape as cyto
import plotly.express as px

from dash import html, dcc

from dataloading_utils.S3Wrapper import S3Wrapper
from visualization_utils.Piechart import piechart_builder
from visualization_utils.Linechart import line_builder
from visualization_utils.Graph import graph_builder

import pandas as pd

df = pd.read_csv("leaks_processed.csv")

app = dash.Dash(__name__)

with open("./visualisation_utils/config/color_config.json", "r") as file:
    color_config = json.load(file)
BGCOLOR = color_config["background color"]
FONTCOLOR = color_config["font color"]
EDGECOLOR = color_config["graph"]["edge"]
NODECOLOR = color_config["graph"]["node"]

app.layout = html.Div([
    html.H1(
        children = "ISD Monitoring Dashboard",
        style = {
            "textAlign": "center"
        }
    ),

    dcc.Graph(
        id = "overview-piechart",
        figure = {
            "data": piechart_builder(),
            "layout": {
                "plot_bgcolor": BGCOLOR,
                "paper_bgcolor": BGCOLOR,
                "font": {
                    "color": FONTCOLOR
                },
                "title": "Overview Piechart"
            }
        }
    ),

    dcc.Graph(
        id = "overview-linechart",
        figure = {
            "data": line_builder(), 
            "layout": {
                "plot_bgcolor": BGCOLOR,
                "paper_bgcolor": BGCOLOR,
                "font": {
                    "color": FONTCOLOR
                    },
                "title": "Overview Line Chart",
                "xaxis": {
                    "title": "xaxis_label"
                    },
                "yaxis": {
                    "title": "yaxis_label"
                    }
            }
        }
    ),

    cyto.Cytoscape(
        id = "network-graph",
        elements = graph_builder(),  
        style = {
            "width": "100%",
            "height": "500px"
            },
        layout = {
            "name": "circle"
            },  # Specify graph layout (e.g., circle, grid)
        stylesheet = [
            {
                "selector": "node",
                "style": {
                    "content": "data(label)",
                    "background-color": BGCOLOR,
                    "color": NODECOLOR,
                    "text-valign": "center"
                }
            },
            {
                "selector": "edge",
                "style": {
                    "line-color": EDGECOLOR,
                    "target-arrow-color": EDGECOLOR,
                    "target-arrow-shape": "triangle",
                    "curve-style": "bezier"
                }
            }
        ]
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
