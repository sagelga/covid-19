import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from plotly import express as px
from plotly import graph_objects as go
from datetime import datetime, timedelta
import time

from app import app

# Website Builder
layout = html.Div([
    html.H2('Vaccine Deal'),

    html.H2('Insights'),
])
