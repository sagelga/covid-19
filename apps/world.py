import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output, State, ALL
import dash_core_components as dcc
import dash_html_components as html
from plotly import express as px
from datetime import datetime, timedelta

from app import app
from component import owid

df = owid.df

all_country = df["location"].unique()

# Website Builder
layout = html.Div([
    html.Div([
        html.H2('World Trends'),

        dcc.Graph(id='world-graph-choroplethview'),

        html.Div([
            html.Div(children=[
                html.Label('🕖 Time Range'),
                dcc.Dropdown(
                    id="world-dropdown-choroplethview-timerange",
                    options=[
                        {'label': 'All time', 'value': 'all'}
                        , {'label': '7 Days', 'value': '7'}
                        , {'label': '14 Days', 'value': '14'}
                        , {'label': '30 Days', 'value': '30'}
                        , {'label': '90 Days', 'value': '90'}
                        , {'label': '180 Days', 'value': '180'}
                        , {'label': '365 Days', 'value': '365'}
                    ]
                    , placeholder="Select a range"
                    , value='14'
                    , multi=False
                    , clearable=False
                    , searchable=False
                    , persistence=True
                    , persistence_type='session'
                ),
            ], className="three columns"),
        ], className='row'),
    ]),

    html.Br(),

    html.H2('Global Situation'),
    html.Div([
        html.Div([dcc.Graph()], className='six columns'),
        html.Div([dcc.Graph()], className='six columns'),
    ], className='row'),

    html.Br(),

    html.H3('Situation by Region'),
    dcc.Graph(),
    html.Div([
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
    ]),

    html.Br(),

    html.H3('Situation by Country'),
    html.Div([
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
    ]),
])


@app.callback(
    Output("world-graph-choroplethview", "figure"),
    Input("world-dropdown-choroplethview-timerange", "value")
)
def world_graph_worldmap(time_range):
    # - Time Range -
    time_max = datetime.today()
    time_list = []

    if time_range == 'all':
        time_range = time_max = timedelta(df['date'].min())

    for _ in range(1, int(time_range) + 1):
        time_check = time_max - timedelta(days=_)
        # if time_check in df['date']:
        time_check = time_check.strftime("%Y-%m-%d")
        time_list.append(time_check)

    # - Apply mask -
    mask = df['date'].isin(time_list)

    fig = px.choropleth(df[mask]
                        , locations="iso_code"
                        , color='case_per_population'
                        , hover_name="location"
                        , animation_frame="date_str"
                        , color_continuous_scale=px.colors.sequential.Viridis
                        , projection='miller'
                        )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig
