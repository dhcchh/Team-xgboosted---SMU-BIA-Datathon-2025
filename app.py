import json
import dash_cytoscape as cyto
import plotly.express as px

from dash import Dash, html, dcc, Input, Output

from S3Wrapper import S3Wrapper
from visualization_utils.Piechart import piechart_builder
from visualization_utils.Linechart import line_builder
from visualization_utils.Graph import graph_builder
from visualization_utils.Barchart import barchart_builder

import pandas as pd

LEAKS_DF = pd.read_csv("./Dataset/processed_leaks_2.csv")
NEWS_DF = pd.read_csv("./Dataset/processed_news_2.csv")
WORKING_DF = "placeholder"

app = Dash(__name__)

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
        id = "piechart",
        figure = {
            "data": piechart_builder(),
            "layout": {
                "plot_bgcolor": BGCOLOR,
                "paper_bgcolor": BGCOLOR,
                "font": {
                    "color": FONTCOLOR
                },
                "title": "Piechart"
            }
        }
    ),

    dcc.Checklist(
        id = "barchart_slicer",
        options = [
            {"label": "Leaks", "value": "leaks"},
            {"label": "News", "value": "news"}
        ],
        value = ["Leaks", "News"],
        inline = True
    ),

    dcc.Graph(id = "barchart"),

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

@app.callback(
    Output("barchart", "figure"),  
    Input("barchart_slicer", "value") 
)
def update_barchart(source):
    processed_df = barchart_builder(WORKING_DF, source)
    fig = px.bar(processed_df, x="Category", y="Count", title="")

    fig.update_layout(
        plot_bgcolor = BGCOLOR,
        paper_bgcolor = BGCOLOR,
        font = dict(color = FONTCOLOR, size = 14),
        title = dict(font = dict(size = 20)),
        xaxis = dict(title = "", tickangle = 0),
        yaxis = dict(title = "")
    )
    return fig

@app.callback(
    Output("")
)

@app.callback

if __name__ == "__main__":
    app.run_server(debug=True)
