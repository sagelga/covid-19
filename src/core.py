import pandas as pd
import numpy as np
import requests

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

try:
    # Read data to Dataframe
    df = pd.read_csv('src/owid-covid-data.csv')
except:
    # Import data from GH
    url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
    r = requests.get(url, allow_redirects=True)
    open('src/owid-covid-data.csv', 'wb').write(r.content)
    # Read data to Dataframe
    df = pd.read_csv('src/owid-covid-data.csv')

# Data selection
df = df.dropna(subset=['continent'])

# Create line chart
fig = px.line(df, x="date", y="total_cases", title='Total Cases',
              color="continent", line_group="location", hover_name="location")

# print(df)
fig.show()
