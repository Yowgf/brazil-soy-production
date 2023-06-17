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

dash.register_page(__name__)

layout = html.Div(
    [
        html.H1(children="Brazil Soy Production", style={"textAlign": "center"}),
        html.Div([
            dcc.Dropdown(df.region.unique(), "Brasil", id="region-dropdown",
                         className="dropdown"),
            dcc.Dropdown(["area", "production"], "area", id="type-dropdown",
                         className="dropdown"),
        ], className="dropdowns"),
        dcc.Graph(id="colormap-before"),
        dcc.Graph(id="colormap-after"),
        dcc.Graph(id="linechart"),
    ]
)

def colormap(region: str, typ: str, year: int):
    filtered_df = df[df.year == year]
    filtered_df["region"] = df["region"].map(regions_replacement)
    if region in macroregions:
        filtered_df = df[df.region.isin(macroregions[region])]
    else:
        filtered_df = df[df.region == region]
    fig = px.choropleth(filtered_df,
                        geojson=br_regions_json,
                        locations='region',
                        color=typ,
                        color_continuous_scale="Viridis",
                        range_color=(0, 1.5e7),
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
    Input("type-dropdown", "value")
)
def update_colormap_before(region, typ):
    print("Updating before colormap")
    return colormap(region, typ, 2006)

@callback(
    Output("colormap-after", "figure"),
    Input("region-dropdown", "value"),
    Input("type-dropdown", "value")
)
def update_colormap_after(region, typ):
    print("Updating after colormap")
    return colormap(region, typ, 2023)

@callback(
    Output("linechart", "figure"),
    Input("region-dropdown", "value"),
    Input("type-dropdown", "value")
)
def update_linechart(region, typ):
    print("Updating area linechart")
    dff = df[df.region == region]
    return px.line(dff, x="year", y=typ)
