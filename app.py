import json
import pandas as pd
import dash
from dash import html, dcc, Input, Output
import dash_cytoscape as cyto
import plotly.graph_objects as go

# Import visualization functions
from visualization_utils.Piechart import piechart_builder
from visualization_utils.Linechart import line_builder
from visualization_utils.Graph import graph_builder
from visualization_utils.Barchart import barchart_builder
from visualization_utils.WorldHeatMap import heatmap_builder

# Load datasets
LEAKS_DF = pd.read_csv("./Dataset/processed_leaks_2.csv")
NEWS_DF = pd.read_csv("./Dataset/processed_news_2.csv")

# Add source columns
LEAKS_DF["source"] = "leaks"
NEWS_DF["source"] = "news"

# Combine datasets
WORKING_DF = pd.concat([LEAKS_DF, NEWS_DF], ignore_index=True)

# Load color configuratiore
with open("./visualization_utils/config/colour_config.json", "r") as file:
    color_config = json.load(file)
BG = color_config["background"]
PAPER = color_config["paper"]
FONTCOLOR = color_config["font"]
EDGE = color_config["graph"]["edge"]
NODE = color_config["graph"]["node"]
TITLE = color_config["title"]

# Initialize Dash app
app = dash.Dash(__name__)


def apply_common_aesthetics(fig, title_color=TITLE):
    """Apply consistent styling across all figures."""
    fig.update_layout(
        plot_bgcolor=BG,
        paper_bgcolor=PAPER,
        font=dict(size=16, color=FONTCOLOR),
        title=dict(font=dict(size=20, color=title_color))
    )
    return fig


# Define layout
app.layout = html.Div(
    style={"backgroundColor": BG, "padding": "20px"},

    children=[
        html.H1(
            "ISD Monitoring Dashboard",
            style={"textAlign": "center", "color": TITLE, "fontfamily": "Arial", "fontsize": "36px"}
        ),

        ##############
        # Heatmap #
        ##############
        html.H2("Geospatial Threat Heatmap", style={"textAlign": "center", "color": TITLE}),
        dcc.Checklist(
            id="heatmap-checkbox",
            options=[{"label": "News", "value": "news"}, {"label": "Leaks", "value": "leaks"}],
            value=["news", "leaks"],
            inline=True,
            style={"textAlign": "center", "marginBottom": "10px", "color": FONTCOLOR}
        ),
        html.Div(
            style={"display": "flex", "justifyContent": "center", "gap": "20px"},
            children = [
                dcc.Graph(
                    id="heatmap-graph",
                    config={"displayModeBar": True},
                    style={
                        "display": "flex",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "width": "80%",
                        "height": "80vh"
                    }
                ),
                dcc.Slider(
                    id="heatmap-slider",
                    min=0,
                    max=50,
                    step=1,
                    value=20,
                    marks={i: str(i) for i in range(0, 51, 10)},
                    vertical=True,
                    tooltip={"always_visible": True, "placement": "right"}
                )
            ]
        ),
        html.P(
            "This map shows where all TCCE cases in the data provided have happened for each country. "
            "The legend 'No. of Incidents' corresponds to the number of incidents for each country. "
            "The slider allows you to filter the map by the number of TCCE incidents for each country.",
            style={"textAlign": "center", "color": FONTCOLOR, "padding": "10px"}
        ),

        ###################
        # Pie & Bar Chart #
        ###################
        html.H2("Pie & Bar Chart", style={"textAlign": "center", "color": TITLE}),
        dcc.Checklist(
            id="piebar-checkbox",
            options=[{"label": "News", "value": "news"}, {"label": "Leaks", "value": "leaks"}],
            value=["news", "leaks"],
            inline=True,
            style={"textAlign": "center", "marginBottom": "10px", "color": FONTCOLOR}
        ),
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "center",
                "width": "80%"
            },
            children = [
                html.Div(
                    style={
                        "display": "flex",
                        "justifyContent": "center",
                        "width": "80%"
                    },
                    children = [
                        dcc.Graph(id="piechart", style={"width": "50%", "height": "450px", "alignItems": "center"}),
                        dcc.Graph(id="barchart", style={"width": "50%", "height": "450px", "alignItems": "center"})
                    ]
                )
            ]
        ),
        html.P(
            "The pie chart displays the proportion (%) of different threat categories. The bar"
            "chart provides the exact count for each category, making it easier to compare specific values."
            "You can see the exact count by hovering over the bar chart.",
            style={"textAlign": "center", "color": FONTCOLOR, "padding": "10px"}
        ),

        ###############
        # Line Charts #
        ###############
        html.H2("Trend Analysis Over Time", style={"textAlign": "center", "color": TITLE}),
        dcc.Checklist(
            id="line-checkbox",
            options=[{"label": "News", "value": "news"}, {"label": "Leaks", "value": "leaks"}],
            value=["news", "leaks"],
            inline=True,
            style={"textAlign": "center", "marginBottom": "10px", "color": FONTCOLOR}
        ),
        html.Div(
            children=[
                dcc.Graph(id="linechart_t", style={"width": "100%"}),
                dcc.Graph(id="linechart_s", style={"width": "100%"}),
                dcc.Graph(id="linechart_e", style={"width": "100%"}),
                dcc.Graph(id="linechart_c", style={"width": "100%"})
            ],
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"}
        ),
        html.P(
            "These line charts depict trends in the occurrence of different threats over time."
            "If a count is zero on the line chart, it means the incident is not classified under that specific category but falls into one of the other three." 
            " For example, an incident with a count of zero under Espionage may be classified as Terrorism, Communalism, or Cybersecurity.",
            style={"textAlign": "center", "color": FONTCOLOR, "padding": "10px"}
        ),

        #################
        # Network Graph #
        #################
        html.H2("Network Graph of Threat Incidents", style={"textAlign": "center", "color": TITLE}),
        dcc.Checklist(
            id="graph-checkbox",
            options=[
                {"label": "Terrorism", "value": "terrorism"},
                {"label": "Cybersecurity", "value": "cyber_security"},
                {"label": "Espionage", "value": "espionage"},
                {"label": "Communalism", "value": "communalism"}
            ],
            value=["cyber_security"],  # Default selection
            inline=True,
            style={"textAlign": "center", "marginBottom": "10px", "color": FONTCOLOR}
        ),
        cyto.Cytoscape(
            id="network-graph",
            elements=[],
            style={"width": "100%", "height": "700px"},
            layout={"name": "breadthfirst", "roots": ["Singapore"]},
            stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "content": "data(label)",
                        "background-color": "#666666",  # Dark gray nodes
                        "color": "#FFFF00",  # Bright yellow text for contrast
                        "font-size": "18px",  # Larger text
                        "text-valign": "top",  # Move text above node
                        "text-halign": "center",
                        "text-rotation": "45deg",
                        "text-margin-y": "-12px",  # Offset text upwards
                        "width": "20px",  # Bigger nodes
                        "height": "20px",
                    }
                },
                {
                    "selector": "edge",
                    "style": {
                        "line-color": "#BBBBBB",  # Light gray edges
                        "target-arrow-color": "#BBBBBB",
                        "target-arrow-shape": "none",
                        "curve-style": "bezier",
                        "label": "data(rows)",
                        "color": "#FFFF00"
                    }
                }
            ]
        ),
        html.P(
            "This network graph shows the connections between countries based on shared threat incidents. Clusters "
            "indicate regional connections or geopolitical ties."
            "The nodes (points) on the Network can be dragged by clicking and holding on it."
            "To find out the exact incidents involved, you can click on the node to find the incident ID by index on the combined table",
            style={"textAlign": "center", "color": FONTCOLOR, "padding": "10px"}
        )
    ]
)



###########################
# CALLBACKS FOR UPDATING #
###########################

# Heatmap Callback
@app.callback(
    Output("heatmap-graph", "figure"),
    [Input("heatmap-checkbox", "value"),
     Input("heatmap-slider", "value")]
)
def update_heatmap(source_list, cutoff):
    return apply_common_aesthetics(heatmap_builder(WORKING_DF, source_list, cutoff))


# Pie & Bar Chart Callback
@app.callback(
    [Output("piechart", "figure"), Output("barchart", "figure")],
    Input("piebar-checkbox", "value")
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
    Input("line-checkbox", "value")
)
def update_linechart(source_list):
    fig_t, fig_s, fig_e, fig_c = line_builder(WORKING_DF, source_list)
    return (apply_common_aesthetics(fig_t),
            apply_common_aesthetics(fig_s),
            apply_common_aesthetics(fig_e),
            apply_common_aesthetics(fig_c))


# Network Graph Callback
@app.callback(
    Output("network-graph", "elements"),
    Input("graph-checkbox", "value"),
    Input("network-graph", "tapNode")
)
def update_network_graph(selected_categories, tapped_node):
    return graph_builder(WORKING_DF, selected_categories, tapped_node)


# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
