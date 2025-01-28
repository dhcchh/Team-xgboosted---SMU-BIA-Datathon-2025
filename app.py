import json
import pandas as pd
import dash_cytoscape as cyto
import plotly.express as px

from dash import Dash, html, dcc, Input, Output
from visualization_utils.Piechart import piechart_builder
from visualization_utils.Linechart import line_builder
from visualization_utils.Graph import graph_builder
from visualization_utils.Barchart import barchart_builder
from visualization_utils.WorldHeatMap import heatmap_builder

# Load datasets
LEAKS_DF = pd.read_csv("./Dataset/processed_leaks_2.csv")
LEAKS_DF["source"] = "leaks"

NEWS_DF = pd.read_csv("./Dataset/processed_news_2.csv")
NEWS_DF["source"] = "news"

WORKING_DF = pd.concat([NEWS_DF, LEAKS_DF], ignore_index=True)

# Initialize Dash App
app = Dash(__name__)

# Load color config
with open("./visualization_utils/config/colour_config.json", "r") as file:
    color_config = json.load(file)

BG = color_config["background"]
PAPER = color_config["paper"]
FONTCOLOR = color_config["font"]
EDGE = color_config["graph"]["edge"]
NODE = color_config["graph"]["node"]
TITLE = color_config["title"]

# Function to apply consistent aesthetics to figures
def apply_common_aesthetics(fig, title_color=TITLE):
    fig.update_layout(
        plot_bgcolor=BG,
        paper_bgcolor=PAPER,
        font=dict(size=16, color=FONTCOLOR),
        title=dict(font=dict(size=22, color=title_color)),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# App Layout
app.layout = html.Div(
    style={
        "backgroundColor": BG,
        "minHeight": "100vh",
        "padding": "20px",
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "justifyContent": "flex-start",
        "width": "100%",
        "margin": "0"
    },
    children=[
        #################
        # Main Container#
        #################
        html.Div(
            style={
                "width": "90%",
                "backgroundColor": BG,
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.3)"
            },
            children=[
                html.H1(
                    children="ISD Monitoring Dashboard",
                    style={
                        "textAlign": "center",
                        "color": TITLE,
                        "fontFamily": "Arial",
                        "fontSize": "36px",
                        "marginBottom": "20px"
                    }
                ),

                #################
                # World Heatmap #
                #################
                html.Div([
                    html.H2(
                        children="World Heatmap",
                        style={
                            "textAlign": "center",
                            "color": TITLE,
                            "fontFamily": "Arial",
                            "fontSize": "30px",
                            "marginBottom": "10px"
                        }
                    ),
                    dcc.Checklist(
                        id="heatmap_checkbox",
                        options=[{'label': ' News', 'value': 'news'}, {'label': ' Leaks', 'value': 'leaks'}],
                        value=["news", "leaks"],
                        inline=True,
                        style={
                            "marginBottom": "20px",
                            "textAlign": "center",
                            "backgroundColor": PAPER,
                            "color": FONTCOLOR,
                            "fontSize": "16px",
                            "padding": "10px",
                            "borderRadius": "5px"
                        }
                    ),
                    dcc.Graph(id="heatmap-graph", style={"width": "100%", "height": "500px"})
                ], style={"backgroundColor": PAPER, "padding": "20px", "borderRadius": "10px", "marginTop": "20px", "width": "100%"}),

                ###################
                # Pie & Bar Chart #
                ###################
                html.Div(
                    style={
                        "backgroundColor": PAPER,
                        "padding": "30px",
                        "borderRadius": "10px",
                        "marginTop": "20px",
                        "width": "100%"
                    },
                    children=[
                        html.H2(
                            children="Pie & Bar Chart",
                            style={
                                "color": TITLE,
                                "fontFamily": "Arial",
                                "fontSize": "30px",
                                "marginBottom": "15px",
                                "textAlign": "center"
                            }
                        ),
                        dcc.Checklist(
                            id="piebar_checkbox",
                            options=[{'label': ' News', 'value': 'news'}, {'label': ' Leaks', 'value': 'leaks'}],
                            value=["news", "leaks"],
                            inline=True,
                            style={
                                "marginBottom": "20px",
                                "textAlign": "center",
                                "backgroundColor": PAPER,
                                "color": FONTCOLOR,
                                "fontSize": "16px",
                                "padding": "10px",
                                "borderRadius": "5px"
                            }
                        ),
                        html.Div([
                            dcc.Graph(id="piechart", style={"width": "48%", "height": "400px", "display": "inline-block"}),
                            dcc.Graph(id="barchart", style={"width": "48%", "height": "400px", "display": "inline-block"})
                        ], style={"display": "flex", "justifyContent": "center", "gap": "20px"})
                    ]
                ),

                ###############
                # Line Charts #
                ###############
                html.Div([
                    html.H2(
                        children="Trend Analysis",
                        style={
                            "textAlign": "center",
                            "color": TITLE,
                            "fontFamily": "Arial",
                            "fontSize": "30px",
                            "marginBottom": "10px"
                        }
                    ),
                    dcc.Checklist(
                        id="linechart_checkbox",
                        options=[
                            {"label": " News", "value": "news"},
                            {"label": " Leaks", "value": "leaks"}
                        ],
                        value=["news", "leaks"],
                        inline=True,
                        style={
                            "textAlign": "center",
                            "marginBottom": "20px"
                        }
                    ),
                    html.Div(
                        children=[
                            dcc.Graph(id="linechart_t", style={"width": "48%", "height": "400px", "display": "inline-block"}),
                            dcc.Graph(id="linechart_s", style={"width": "48%", "height": "400px", "display": "inline-block"}),
                            dcc.Graph(id="linechart_e", style={"width": "48%", "height": "400px", "display": "inline-block"}),
                            dcc.Graph(id="linechart_c", style={"width": "48%", "height": "400px", "display": "inline-block"})
                        ],
                        style={"display": "flex", "flexWrap": "wrap", "justifyContent": "center", "gap": "20px"}
                    )
                ], style={"backgroundColor": PAPER, "padding": "20px", "borderRadius": "10px", "marginTop": "20px", "width": "100%"})
            ]
        )
    ]
)

# Callbacks

@app.callback(
    Output("heatmap-graph", "figure"),
    Input("heatmap_checkbox", "value")
)
def update_heatmap(source_list):
    return heatmap_builder(WORKING_DF, source_list)

@app.callback(
    [Output("piechart", "figure"), Output("barchart", "figure")],
    [Input("piebar_checkbox", "value")]
)
def update_piebar_chart(source):
    piechart = apply_common_aesthetics(piechart_builder(WORKING_DF, source))
    barchart = apply_common_aesthetics(barchart_builder(WORKING_DF, source))
    return piechart, barchart

@app.callback(
    [Output("linechart_t", "figure"),
     Output("linechart_s", "figure"),
     Output("linechart_e", "figure"),
     Output("linechart_c", "figure")],
    [Input("linechart_checkbox", "value")]
)
def update_linecharts(source_list):
    return line_builder(WORKING_DF, source_list)

# Run the App
if __name__ == "__main__":
    app.run_server(debug=True)