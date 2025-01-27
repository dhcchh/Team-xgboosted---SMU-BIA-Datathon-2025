import json
import pandas as pd

from dash import Dash, html, dcc, Input, Output

from visualization_utils.Piechart import piechart_builder
from visualization_utils.Linechart import line_builder
from visualization_utils.Graph import graph_builder
from visualization_utils.Barchart import barchart_builder

LEAKS_DF = pd.read_csv("./Dataset/processed_leaks_2.csv")
LEAKS_DF["source"] = "news"
NEWS_DF = pd.read_csv("./Dataset/processed_news_2.csv")
NEWS_DF["source"] = "leaks"
WORKING_DF = pd.concat([NEWS_DF, LEAKS_DF], ignore_index=True)

app = Dash(__name__)

with open("./visualization_utils/config/color_config.json", "r") as file:
    color_config = json.load(file)
BG = color_config["background"]
PAPER = color_config["paper"]
FONTCOLOR = color_config["font"]
EDGE = color_config["graph"]["edge"]
NODE = color_config["graph"]["node"]
TITLE = color_config["title"]

def apply_common_aesthetics(fig, title_color = TITLE):
    fig.update_layout(
        plot_bgcolor = BG,
        paper_bgcolor = PAPER,
        font = dict(size = 16, color = FONTCOLOR),
        title = dict(font = dict(size = 20, color = title_color))
    )
    return fig

app.layout = html.Div(
    style = {
        "backgroundColor": BG, 
        "height": "100vh"
    },

    children = [
        html.H1(
            children = "ISD Monitoring Dashboard",
            style = {
                "textAlign": "center",
                "color": TITLE,
                "fontfamily": "Arial",
                "fontsize": "36px"
            }
        ),

        #################
        # World Heatmap #
        #################


        ###################
        # Pie & Bar chart #
        ###################
        html.H2(
            children = "Pie & Bar Chart",
            style = {
                "textAlign": "center",
                "color": TITLE,
                "fontfamily": "Arial",
                "fontsize": "36px"
            }
        ),
        dcc.Checklist(
            id = "piebar_checkbox",
            options = [
                {'label': 'News', 'value': 'news'},
                {'label': 'Leaks', 'value': 'leaks'}
            ],
            value = ["news", "leaks"],
            inline = True,
            style = {
                "marginBottom": "20px",
                "textAlign": "center",
                "backgroundColor": PAPER,
                "color": FONTCOLOR,
                "width": "50%",
                "margin": "0 auto"
                } 
        ),
        html.Div([
            dcc.Graph(id = "piechart", style = {"width": "45%", "height": "45%", "display": "inline-block"}),
            dcc.Graph(id = "barchart", style = {"width": "45%", "height": "45%", "display": "inline-block"})
        ], style = {"display": "flex", "justifyContent": "center", "gap": "20px"}),

        ###############
        # Line Charts #
        ###############
        dcc.Checklist(
            id = "line_checkbox",
            options = [
                {"label": "News", "value": "news"},
                {"label": "Leaks", "value": "leaks"}
            ],
            value = ["news", "leaks"],
            inline = True,
            style = {"textAlign": "center", "marginBottom": "20px"}
        ),

        # Graphs in 2x2 layout
        html.Div(
            children=[
                dcc.Graph(id = "linechart_t", style={"width": "100%", "height": "100%"}),
                dcc.Graph(id = "linechart_s", style={"width": "100%", "height": "100%"}),
                dcc.Graph(id = "linechart_e", style={"width": "100%", "height": "100%"}),
                dcc.Graph(id = "linechart_c", style={"width": "100%", "height": "100%"})
            ],
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",  
                "gap": "20px", 
                "justifyItems": "center",
                "alignItems": "center"
            }
        )

        #################
        # Network Graph #
        #################


    ]
)

@app.callback(
    [Output("piechart", "figure"),
     Output("barchart", "figure")],
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
    [Input("line_checkbox", "value")]

)
def update_linechart(source):
    fig_t, fig_s, fig_e, fig_c = line_builder(WORKING_DF, source)
    fig_t = apply_common_aesthetics(fig_t)
    fig_s = apply_common_aesthetics(fig_s)
    fig_e = apply_common_aesthetics(fig_e)
    fig_c = apply_common_aesthetics(fig_c)
    return fig_t, fig_s, fig_e, fig_c

if __name__ == "__main__":
    app.run_server(debug=True)
