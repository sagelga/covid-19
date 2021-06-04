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
def get_home_countryinfo(country):
    if country is None:
        return None

    def overall_stats(df):
        mask = df['location'].isin([country])
        df = df[mask]

        fig1 = go.Figure(go.Indicator(
            mode="number+delta",
            value=df['total_cases'].iloc[-1],
            delta={
                'reference': df['total_cases'].iloc[-2]
                , 'relative': True
                , 'valueformat': ".2p"
                , 'increasing': {'symbol': '+'}
                , 'decreasing': {'symbol': '-'}
            },
            title={
                'text': "Total Cases<br><span style='font-size:0.8em;color:gray'>on {}</span>"
                    .format(df['date'].iloc[-1])
            },
            domain={'y': [0, 1], 'x': [0.25, 0.75]}))
        fig1.add_trace(go.Scatter(x=df['date'], y=df['total_cases']))
        fig1.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        fig2 = go.Figure(go.Indicator(
            mode="number+delta",
            value=df['total_deaths'].iloc[-1],
            delta={
                'reference': df['total_deaths'].iloc[-2]
                , 'relative': True
                , 'valueformat': ".2p"
                , 'increasing': {'symbol': '+ '}
                , 'decreasing': {'symbol': '- '}
            },
            title={'text': "Total Deaths<br><span style='font-size:0.8em;color:gray'>on {}</span>".format(
                df['date'].iloc[-1])},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}))
        fig2.add_trace(go.Scatter(x=df['date'], y=df['total_deaths']))
        fig2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        return html.Div([
            html.Div([
                dbc.Card(dbc.CardBody([
                    dcc.Graph(figure=fig1)
                ]))
            ], className='six columns'),
            html.Div([
                dbc.Card(dbc.CardBody([
                    dcc.Graph(figure=fig2)
                ]))
            ], className='six columns'),
        ], className='row')

    def compare_panel(df):
        continent = 'Asia'
        avg_continent = df[['continent', 'total_cases']].groupby(by='continent')['total_cases'].mean().values[0]
        avg_world = df['total_cases'].mean()

        mask = df['location'].isin([country])
        df = df[mask].groupby(by='location').max().reset_index()

        fig = px.bar(df, x='total_cases', y='location', text='total_cases', orientation='h')

        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

        # Add Average threshold
        draw_indicator(fig, 'salmon', avg_continent)
        draw_indicator(fig, 'salmon', avg_world)

        return html.Div([
            dbc.Card(dbc.CardBody([
                dcc.Graph(figure=fig),
            ]))
        ])

    def raw_datarank(df):
        return html.Div([
            dbc.Card(dbc.CardBody([
                dcc.Graph(),
            ]))
        ])

    def draw_indicator(fig, line_color, value):
        return fig.add_shape(type="line",
                             x0=value, x1=value, y0=-0.5, y1=0.5,
                             line={'color': line_color, 'width': 3, 'dash': 'dot'}
                             )
        # return fig.add_vline(x=value, line_width=2, line_dash="dash", line_color=line_color)

    ddf = df[['continent', 'location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths',
              'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated', 'new_vaccinations',
              'people_vaccinated_per_population', 'people_fully_vaccinated_per_population']]

    return [html.Div([
        overall_stats(ddf),
        html.Br(),

        compare_panel(ddf),
        html.Br(),

        raw_datarank(ddf)
    ])]
