import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
from plotly import express as px
from plotly import graph_objects as go
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc

from app import app
from component import owid

df = owid.df

all_country = np.sort(df["location"].unique())

layout = html.Div([
    html.Div([
        html.Label('Country'),
        dcc.Dropdown(id='home-dropdown-countrySelect'
                     , options=[{"label": x, "value": x}
                                for x in all_country]
                     , value='Thailand'
                     , placeholder="Select a country"
                     , multi=False, clearable=True, searchable=True
                     , persistence=True, persistence_type='session'
                     ),
    ]),

    html.Br(),

    html.Div(id='home-container-countryData'),
])


@app.callback(
    Output('home-container-countryData', 'children'),
    Input('home-dropdown-countrySelect', 'value')
)
def get_home_countryInfo(country):
    if country is None:
        return None

    def overall_stats(df):
        fig1 = px.line(df, x="date", y='total_cases'
                       # , hover_data=[case_type]
                       )
        fig2 = px.line(df, x="date", y='total_deaths'
                       # , hover_data=[case_type]
                       )
        return html.Div([
            html.Div([
                dbc.Card(dbc.CardBody([
                    fig1
                ]))
            ], className='six columns'),
            html.Div([
                dbc.Card(dbc.CardBody([
                    fig2
                ]))
            ], className='six columns'),
        ], className='row')

    def compare_panel(df):
        return html.Div([
            dbc.Card(dbc.CardBody([
                dcc.Graph(),
            ]))
        ])

    def raw_datarank(df):
        return html.Div([
            dbc.Card(dbc.CardBody([
                dcc.Graph(),
            ]))
        ])

    ddf = df[['continent', 'location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths',
              'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated', 'new_vaccinations',
              'people_vaccinated_per_population', 'people_fully_vaccinated_per_population']]

    country_mask = ddf['location'].isin([country])

    return [html.Div([
        overall_stats(ddf[country_mask]),
        html.Br(),

        compare_panel(ddf),
        html.Br(),

        raw_datarank(ddf)
    ])]
