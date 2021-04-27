import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output, State, ALL
import dash_core_components as dcc
import dash_html_components as html
from plotly import express as px
from plotly import graph_objects as go

from app import app

url = 'https://covid19-static.cdn-apple.com/covid19-mobility-data/2106HotfixDev21/v3/en-us/applemobilitytrends-2021-04-25.csv'
df = pd.read_csv(url)
df.drop('alternative_name', inplace=True, axis=1)

layout = html.Div([
    html.Div([
        html.H2('Mobility Report'),
        html.P('Data from Apple. Report reflects requests for directions in Apple Maps.')
    ])
])
