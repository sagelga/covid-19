import pandas as pd
import numpy as np
import requests

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Importing data
from df_import import df_import

# Data selection
df = df_import()
df = df.dropna(subset=['continent'])

# Create line chart
fig = px.line(df, x="date", y="total_cases", title='Total Cases',
              color="continent", line_group="location", hover_name="location")

fig.show()
