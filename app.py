import json
import pandas as pd
import dash
from dash import Dash, html, dcc, Input, Output

from visualization_utils.Piechart import piechart_builder
from visualization_utils.Linechart import line_builder
from visualization_utils.Graph import graph_builder
from visualization_utils.Barchart import barchart_builder
from visualization_utils.WorldHeatMap import heatmap_builder

# Load dataset
LEAKS_DF = pd.read_csv("./Dataset/processed_leaks_2.csv")
LEAKS_DF["source"] = "leaks"
NEWS_DF = pd.read_csv("./Dataset/processed_news_2.csv")
NEWS_DF["source"] = "news"
WORKING_DF = pd.concat([NEWS_DF, LEAKS_DF], ignore_index=True)

# Load color configuration
with open("./visualization_utils/config/colour_config.json", "r") as file:
    color_config = json.load(file)
BG = color_config["background"]
PAPER = color_config["paper"]
FONTCOLOR = color_config["font"]
EDGE = color_config["graph"]["edge"]
NODE = color_config["graph"]["node"]
TITLE = color_config["title"]

# Initialize app
app = Dash(__name__)

# Function for consistent styling
def apply_common_aesthetics(fig, title_color=TITLE):
    fig.update_layout(
        plot_bgcolor=BG,
        paper_bgcolor=PAPER,
        font=dict(size=16, color=FONTCOLOR),
        title=dict(font=dict(size=20, color=title_color))
    )
    return fig

# Layout
app.layout = html.Div(
    style={"backgroundColor": BG, "padding": "20px", "minHeight": "100vh"},
    children=[
        html.H1(
            children="ISD Monitoring Dashboard",
            style={
                "textAlign": "center",
                "color": TITLE,
                "fontFamily": "Arial",
                "fontSize": "36px"
            }
        ),

        ###############
        # World Heatmap
        ###############
        html.Div(
            style={"backgroundColor": PAPER, "padding": "20px", "borderRadius": "10px", "marginTop": "20px"},
            children=[
                html.H2(
                    "World Heatmap",
                    style={"color": TITLE, "textAlign": "center", "fontSize": "30px"}
                ),
                dcc.Checklist(
                    id="heatmap_checkbox",
                    options=[{"label": " News", "value": "news"}, {"label": " Leaks", "value": "leaks"}],
                    value=["news", "leaks"],
                    inline=True,
                    style={"textAlign": "center", "marginBottom": "15px", "color": FONTCOLOR}
                ),
                dcc.Graph(id="heatmap-graph", style={"width": "100%", "height": "600px"})
            ]
        ),

        ###################
        # Pie & Bar Charts
        ###################
        html.Div(
            style={"backgroundColor": PAPER, "padding": "20px", "borderRadius": "10px", "marginTop": "20px"},
            children=[
                html.H2(
                    "Pie & Bar Chart",
                    style={"color": TITLE, "textAlign": "center", "fontSize": "30px"}
                ),
                dcc.Checklist(
                    id="piebar_checkbox",
                    options=[{"label": " News", "value": "news"}, {"label": " Leaks", "value": "leaks"}],
                    value=["news", "leaks"],
                    inline=True,
                    style={"textAlign": "center", "marginBottom": "15px", "color": FONTCOLOR}
                ),
                html.Div([
                    dcc.Graph(id="piechart", style={"flex": "1", "height": "400px"}),
                    dcc.Graph(id="barchart", style={"flex": "1", "height": "400px"})
                ], style={"display": "flex", "gap": "20px", "justifyContent": "center"})
            ]
        ),

        ###############
        # Line Charts
        ###############
        html.Div(
            style={"backgroundColor": PAPER, "padding": "20px", "borderRadius": "10px", "marginTop": "20px"},
            children=[
                html.H2(
                    "Line Charts",
                    style={"color": TITLE, "textAlign": "center", "fontSize": "30px"}
                ),
                dcc.Checklist(
                    id="line_checkbox",
                    options=[{"label": " News", "value": "news"}, {"label": " Leaks", "value": "leaks"}],
                    value=["news", "leaks"],
                    inline=True,
                    style={"textAlign": "center", "marginBottom": "15px", "color": FONTCOLOR}
                ),
                html.Div([
                    dcc.Graph(id="linechart_t", style={"flex": "1", "height": "400px"}),
                    dcc.Graph(id="linechart_s", style={"flex": "1", "height": "400px"}),
                    dcc.Graph(id="linechart_e", style={"flex": "1", "height": "400px"}),
                    dcc.Graph(id="linechart_c", style={"flex": "1", "height": "400px"})
                ], style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"})
            ]
        )
    ]
)

###################
# CALLBACKS
###################

# World Heatmap Callback
@app.callback(
    Output("heatmap-graph", "figure"),
    [Input("heatmap_checkbox", "value")]
)
def update_heatmap(source_list):
    return apply_common_aesthetics(heatmap_builder(WORKING_DF, source_list))

# Pie & Bar Chart Callback
@app.callback(
    [Output("piechart", "figure"),
     Output("barchart", "figure")],
    [Input("piebar_checkbox", "value")]
)
def update_piebar_chart(source_list):
    piechart = apply_common_aesthetics(piechart_builder(WORKING_DF, source_list))
    barchart = apply_common_aesthetics(barchart_builder(WORKING_DF, source_list))
    return piechart, barchart

# Line Chart Callback
@app.callback(
    [Output("linechart_t", "figure"),
     Output("linechart_s", "figure"),
     Output("linechart_e", "figure"),
     Output("linechart_c", "figure")],
    [Input("line_checkbox", "value")]
)
def update_linechart(source_list):
    fig_t, fig_s, fig_e, fig_c = line_builder(WORKING_DF, source_list)
    return (
        apply_common_aesthetics(fig_t),
        apply_common_aesthetics(fig_s),
        apply_common_aesthetics(fig_e),
        apply_common_aesthetics(fig_c)
    )

# Run App
if __name__ == "__main__":
    app.run_server(debug=True)
