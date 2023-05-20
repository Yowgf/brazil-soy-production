import dash
import plotly.express as px
from dash import Input, Output, callback, dcc, html

import lib

df = lib.process().get_table()

dash.register_page(__name__)

# TODO: add option to see all regions in a single graph -aholmquist 2023-05-20
layout = html.Div(
    [
        html.H1(children="Brazil Soy Production Area", style={"textAlign": "center"}),
        dcc.Dropdown(df.region.unique(), "Brasil", id="area-dropdown-selection"),
        dcc.Graph(id="area-graph-content"),
    ]
)


@callback(Output("area-graph-content", "figure"), Input("area-dropdown-selection", "value"))
def update_graph(value):
    dff = df[df.region == value]
    return px.line(dff, x="year", y="area")
