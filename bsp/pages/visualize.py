import json

import dash
import plotly.express as px
from dash import Input, Output, callback, dcc, html

import lib

with open("./database/brazil_geo.json") as f:
    br_regions_json = json.load(f)
df = lib.Preprocessor("./database", "all").get_table()
regions_replacement = {
    feature['properties']['name']: feature['id'] for feature in br_regions_json['features']
}
macroregions = {
    "Brasil": regions_replacement.values(),
    "Centro-Oeste": ["MT", "GO", "MS", "DF"],
    "Norte": ["AC", "AM", "RR", "RO", "PA" "AP", "TO"],
    "Nordeste": ["MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA"],
    "Sudeste": ["MG", "SP", "ES", "RJ"],
    "Sul": ["PR", "SC", "RS"]
}

current_end_year = 2023

dash.register_page(__name__)

def graph_figure_overrides():
    return dict(
        layout=dict(
            width=450,
        )
    )

layout = html.Div(
    [
        html.Div([
            html.Span(
                dcc.Dropdown(df.region.unique(), "Brasil", id="region-dropdown"),
                className="dropdown",
            ),
            html.Span(
                dcc.Dropdown(["area", "production"], "area", id="type-dropdown"),
                className="dropdown",
            ),
            html.Span(
                dcc.Input(id="start-year", type="number", placeholder="2006", min=1920, max=2023),
                className="dropdown",
            ),
            html.Span(
                dcc.Input(id="end-year", type="number", placeholder="2023", min=1920, max=2023),
                className="dropdown",
            ),
        ], className="dropdowns"),
        html.Div([
            html.Div(
                dcc.Graph(id="colormap-before",
                          figure=graph_figure_overrides()),
                className="graph",
            ),
            html.Div(
                dcc.Graph(id="colormap-after",
                          figure=graph_figure_overrides()),
                className="graph",
            ),
            html.Div(
                dcc.Graph(id="linechart", figure=dict(layout=dict(width=650))),
                className="graph",
            ),
            html.Div(
                html.Span(id="start-year-result"),
                className="graph graph-label"
            ),
            html.Div(
                html.Span(id="end-year-result"),
                className="graph graph-label"
            ),
            html.Div("Evolution", className="graph graph-label"),
        ], className="graphs"),
    ]
)

def colormap(region: str, typ: str, year: int):
    global current_end_year
    print(f"Generating colormap. {region=} {typ=} {year=}")
    filtered_df = df[df.year == year].copy()
    print("Filtered years: ", filtered_df.year.unique())
    filtered_df["region"] = filtered_df["region"].map(regions_replacement)
    if region in macroregions:
        filtered_df = filtered_df[filtered_df.region.isin(macroregions[region])]
    else:
        filtered_df = filtered_df[filtered_df.region == region] 
    fig = px.choropleth(filtered_df,
                        geojson=br_regions_json,
                        locations='region',
                        color=typ,
                        color_continuous_scale="Viridis",
                        range_color=(0,
                                     filtered_df[typ][filtered_df.year <= current_end_year].max() * 0.8),
                        scope="south america",
                        labels={
                            'production': 'Soy Production (Tons)',
                            'area': 'Soy Production Area (Acres)'
                        },
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

@callback(
    Output("colormap-before", "figure"),
    Input("region-dropdown", "value"),
    Input("type-dropdown", "value"),
    Input("start-year", "value"),
)
def update_colormap_before(region, typ, start_year):
    print("Updating before colormap")
    start_year = start_year or 2006
    return colormap(region, typ, start_year)

@callback(
    Output("colormap-after", "figure"),
    Input("region-dropdown", "value"),
    Input("type-dropdown", "value"),
    Input("end-year", "value"),
)
def update_colormap_after(region, typ, end_year):
    print("Updating after colormap")
    global current_end_year
    end_year = end_year or 2023
    current_end_year = end_year
    return colormap(region, typ, end_year)

@callback(
    Output("linechart", "figure"),
    Input("region-dropdown", "value"),
    Input("type-dropdown", "value"),
    Input("start-year", "value"),
    Input("end-year", "value"),
)
def update_linechart(region, typ, start_year, end_year):
    print("Updating area linechart")
    start_year = start_year or 2006
    end_year = end_year or 2023
    dff = df[(df.region == region) & (df.year.between(start_year, end_year))]
    print(f"dff: {dff=}")
    return px.line(dff, x="year", y=typ)

@callback(
    Output("start-year-result", "children"),
    Input("start-year", "value"),
)
def update_start_year(start_year):
    return start_year or 2006

@callback(
    Output("end-year-result", "children"),
    Input("end-year", "value"),
)
def update_end_year(end_year):
    return end_year or 2023
