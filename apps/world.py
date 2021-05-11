import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output, State, ALL
import dash_core_components as dcc
import dash_html_components as html
from plotly import express as px
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc

from app import app
from component import owid

df = owid.df

all_country = df["location"].unique()

# Website Builder
layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.H2('World Trends'),
            ], className='nine columns'),

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

    dcc.Graph(id='world-graph-choroplethview'),

    html.Br(),

    dbc.Card(dbc.CardBody([
        html.Div([
            html.Button(id='world-button-select-world', children='World'),
            html.Button(id='world-button-select-region', children='Region'),
            html.Button(id='world-button-select-income', children='Income Rate'),
        ]),
        html.Br(),
        html.Div(id='world-component-dataOverview'),
    ])),

    html.Br(),

    dbc.Card(dbc.CardBody([
        html.H3('Biggest Change'),
        html.Div(id='world-component-topChange'),
    ])),

    html.Br(),

    dbc.Card(dbc.CardBody([
        html.H3('Rising Outbreak'),
        html.Div(id='world-component-topHigh'),
    ])),

    html.Br(),

    dbc.Card(dbc.CardBody([
        html.H3('Top Recovery'),
        html.Div(id='world-component-topLow'),
    ])),

    html.Br(),

    html.Button(id='world-button-dataRefresh', children='🔄 Refresh')
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
                        , custom_data=['location', 'population', 'case_per_population']
                        , animation_frame="date_str"
                        , color_continuous_scale=px.colors.sequential.Viridis
                        , projection='miller'
                        )
    fig.update_traces(hovertemplate='<br>'.join([
        "%{customdata[0]}"
        , ''
        , 'Population: %{customdata[1]}'
        , 'Case per Population: %{customdata[2]}:.4f'
    ]))
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


@app.callback(
    Output('world-component-dataOverview', 'children'),
    Input('world-button-dataRefresh', 'value')
)
def world_component_global(refreshClick):
    comp = html.Div([
        html.Div([
            dbc.Card(dbc.CardBody([
                html.Label('Total Infected'),
                html.Br(),
                html.P('200', style={'fontSize': '20px'}),
            ]))
        ], className='six columns'),
        html.Div([
            dbc.Card(dbc.CardBody([
                html.Label('Total Death'),
                html.Br(),
                html.P('200', style={'fontSize': '20px'}),
            ]))
        ], className='six columns'),
    ], className='row')
    return comp


@app.callback(
    Output('world-component-topChange', 'children'),
    Input('world-button-dataRefresh', 'value')
)
def world_component_topChange(refreshClick):
    cardInfo = ['A', 'B', 'C', 'D', 'E']

    cardRow = []
    for x in cardInfo:
        cardRow.append(
            html.Div([
                dbc.Card(dbc.CardBody([
                    html.H5(x),
                    html.P('{}'.format(200))
                ]))
            ], className='two columns')
        )

    return html.Div(cardRow, className='row')


@app.callback(
    Output('world-component-topHigh', 'children'),
    Input('world-button-dataRefresh', 'value')
)
def world_component_topHigh(refreshClick):
    cardInfo = ['A', 'B', 'C', 'D', 'E']

    cardRow = []
    for x in cardInfo:
        cardRow.append(
            html.Div([
                dbc.Card(dbc.CardBody([
                    html.H5(x),
                    html.P('{}'.format(200))
                ]))
            ], className='two columns')
        )

    return html.Div(cardRow, className='row')


@app.callback(
    Output('world-component-topLow', 'children'),
    Input('world-button-dataRefresh', 'value')
)
def world_component_topLow(refreshClick):
    cardInfo = ['A', 'B', 'C', 'D', 'E']

    cardRow = []
    for x in cardInfo:
        cardRow.append(
            html.Div([
                dbc.Card(dbc.CardBody([
                    html.H5(x),
                    html.P('{}'.format(200))
                ]))
            ], className='two columns')
        )

    return html.Div(cardRow, className='row')
