import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html

from app import app

layout = html.Div([
    html.Div([
        html.H2('Mobility Report'),
        html.P('Data from Apple. Report reflects requests for directions in Apple Maps.')
    ])
])
