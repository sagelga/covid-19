import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output, State, ALL
import dash_core_components as dcc
import dash_html_components as html
from plotly import express as px
from plotly import graph_objects as go
from datetime import datetime, timedelta
import time

from app import app

# Data Import
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
df = pd.read_csv(url)

# Data selection
df = df[['iso_code', 'continent', 'location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths',
         'total_cases_per_million', 'new_cases_per_million', 'total_deaths_per_million', 'new_deaths_per_million',
         'icu_patients', 'icu_patients_per_million', 'hosp_patients', 'hosp_patients_per_million', 'new_tests',
         'total_tests', 'total_tests_per_thousand', 'new_tests_per_thousand', 'positive_rate', 'tests_per_case',
         'tests_units', 'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated', 'new_vaccinations',
         'stringency_index', 'population']]

# NA Data Drop
df = df.dropna(subset=[
    'date'
    , 'continent'
    , 'location'
])

# Data Transform
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by=['date', 'location'])
df['date_str'] = df['date'].apply(lambda x: str(x))

# Calculate fields
df['people_vaccinated_per_population'] = 100 * (df['people_vaccinated'] / df['population'])
df['people_fully_vaccinated_per_population'] = 100 * (df['people_fully_vaccinated'] / df['population'])

# all_country = sorted(df["location"].unique())
all_country = np.sort(df["location"].unique())

a = int((time.time() / 900 - 3) / 2 % 24)
curr_time = chr(128336 + a // 2 + a % 2 * 12)

# Reused Components
option_case_type = [
    {'label': 'New confirmed cases', 'value': 'new_cases'}
    , {'label': 'New deaths attributed', 'value': 'new_deaths'}
    , {'label': 'Total confirmed cases', 'value': 'total_cases'}
    , {'label': 'Total deaths attributed', 'value': 'total_deaths'}
    , {'label': 'Vaccinated one dose', 'value': 'people_vaccinated'}
    , {'label': 'Vaccinated all doses', 'value': 'people_fully_vaccinated'}
    , {'label': 'Patient in Hospital', 'value': 'hosp_patients'}
    , {'label': 'Patient in ICU', 'value': 'icu_patients'}
    , {'label': 'Government Response Stringency Index', 'value': 'stringency_index'}
    , {'label': 'Total confirmed cases per million people', 'value': 'total_cases_per_million'}
    , {'label': 'Total deaths per million people', 'value': 'total_deaths_per_million'}
    , {'label': 'Vaccinated one dose per population', 'value': 'people_vaccinated_per_population'}
    , {'label': 'Vaccinated all doses per population', 'value': 'people_fully_vaccinated_per_population'}
]

# Website Builder
layout = html.Div([
    html.Div(children=[
        html.H2('Data'),
        html.P('Select indicators from the dropdown menu.')
    ]),
    # Options
    html.Div(children=[
        html.Div(children=[
            html.Label('🌎 Countries'),
            dcc.Dropdown(
                id="home-dropdown-country"
                , options=[{"label": x, "value": x}
                           for x in all_country]
                , placeholder="Select a country"
                , value=['Thailand']
                , multi=True
                , clearable=True
                , searchable=True
                , persistence=True
                , persistence_type='session'
            ),
        ], className="nine columns"),

        html.Div(children=[
            html.Label('📂 Case Type'),
            dcc.Dropdown(
                id="home-dropdown-casetype"
                , options=option_case_type
                , placeholder="Select a type of case"
                , value='new_cases'
                , multi=False
                , clearable=False
                , searchable=False
                , persistence=True
                , persistence_type='session'
            ),
        ], className="three columns"),
    ], className="row"),

    # Chart
    html.Div(children=[
        dcc.Graph(id="result-chart")
    ], className="twelve columns"),

    html.Div(children=[
        html.Div(children=[
            html.Label('📊 Chart Type'),
            dcc.Dropdown(
                id="home-dropdown-charttype"
                , options=[
                    {'label': '📈 Line Chart', 'value': 'line'}
                    , {'label': '📊 Bar Chart', 'value': 'bar'}
                    , {'label': '📊 Scatter Plot', 'value': 'scatter'}
                    , {'label': '📈 Area Chart', 'value': 'area'}
                    , {'label': '🗺️ World Map', 'value': 'world'}
                ]
                , placeholder="Select a data source"
                , value='line'
                , multi=False
                , clearable=False
                , searchable=False
                , persistence=True
                , persistence_type='session'
            ),
        ], className="three columns"),

        html.Div(children=[
            html.Label(curr_time + ' Time Range'),
            dcc.Dropdown(
                id="home-dropdown-timerange",
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

        html.Div(children=[
            html.Label('📊 Chart Indicators'),
            dcc.Dropdown(
                id="home-dropdown-chartindicator"
                , options=[
                    {'label': 'Highest Threshold', 'value': 'max'}
                    , {'label': 'Average Threshold', 'value': 'avg'}
                    , {'label': 'Lowest Threshold', 'value': 'min'}
                ]
                , placeholder="Select an option (optional)"
                , multi=True
                , clearable=True
                , searchable=False
                , persistence=True
                , persistence_type='session'
                # , persistence=True
                # , persistence_type='memory'
            ),
        ], className='three columns'),
        html.Div(children=[
            html.Label('📊 Regression Line'),
            dcc.Dropdown(
                id="home-dropdown-chartregressionline"
                , options=[
                    {'label': 'Linear Regression Trend Line', 'value': 'linear'}
                    , {'label': 'Log-linear Trend Line', 'value': 'log_linear'}
                ]
                , placeholder="Select an option (optional)"
                , multi=True
                , clearable=True
                , searchable=False
                , persistence=True
                , persistence_type='session'
                # , persistence=True
                # , persistence_type='memory'
            ),
        ], className='three columns'),
    ], className='row'),

])


@app.callback(
    Output("result-chart", "figure"),
    [
        Input("home-dropdown-country", "value")
        , Input("home-dropdown-casetype", "value")
        , Input("home-dropdown-charttype", "value")
        , Input("home-dropdown-timerange", "value")
        , Input("home-dropdown-chartindicator", "value")
        , Input("home-dropdown-chartregressionline", "value")
    ]
)
def update_graph(countries, case_type, chart_type, time_range, chart_indicator, regression_line):
    # - Check a required column
    if not len(countries):
        return go.Figure(go.Indicator(
            mode="number", value=400,
            title={
                "text": "Bad Request<br><span style='font-size:0.8em;color:gray'>Please select a country to continue</span>"},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}))

    # - Time Range -
    time_list = []
    if time_range != 'all':
        for _ in range(1, int(time_range) + 1):
            time_check = (datetime.today() - timedelta(days=_)).strftime("%Y-%m-%d")
            time_list.append(time_check)
        mask = df['location'].isin(countries) & df['date'].isin(time_list)
    else:
        mask = df['location'].isin(countries)
        time_list = df['date'].unique().tolist()

    # - Chart Type -
    if chart_type == "area":  # Line Chart
        fig = px.area(df[mask], x="date", y=case_type
                      , color="location"
                      , hover_name="location"
                      )
        fig.update_traces(connectgaps=True
                          , mode="markers+lines"
                          , hovertemplate=None)
        fig.update_layout(hovermode="x unified")

    elif chart_type == "bar":  # Bar Chart
        fig = px.bar(df[mask], x="date", y=case_type
                     , color="location"
                     , hover_name="location"
                     , barmode="group"
                     )

    elif chart_type == "scatter":
        fig = px.scatter(df[mask], x="date", y=case_type
                         , color="location"
                         )

    elif chart_type == "world":
        fig = px.choropleth(df[mask], locations="iso_code", animation_frame="date_str"
                            , hover_name="location"
                            , color=case_type, color_continuous_scale=px.colors.sequential.Viridis
                            , projection='kavrayskiy7'
                            )
    else:
        fig = px.line(df[mask], x="date", y=case_type
                      , color="location"
                      , hover_name="location"
                      )
        fig.update_traces(connectgaps=True
                          , mode="markers+lines"
                          , hovertemplate=None)
        fig.update_layout(hovermode="x unified")

    # Add chart axis label
    fig.update_layout(title=generate_title(countries, case_type)
                      , xaxis_title="Date"
                      , yaxis_title=get_casetype(case_type)
                      )

    # - Chart Indicator -
    if type(chart_indicator) == list and chart_type not in ['world']:

        if 'max' in chart_indicator:  # Max Line
            y = df[mask][case_type].max()
            fig.add_shape(
                type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
                x0=0, x1=1, xref="paper", y0=y, y1=y, yref="y"
            )

        if 'avg' in chart_indicator:  # Average Line
            # y = (df[mask][case_type].sum()) / len(time_list)
            y = (df[mask][case_type]).mean()
            fig.add_shape(
                type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
                x0=0, x1=1, xref="paper", y0=y, y1=y, yref="y"
            )

        if 'min' in chart_indicator:  # Min Line
            y = df[mask][case_type].min()
            fig.add_shape(
                type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
                x0=0, x1=1, xref="paper", y0=y, y1=y, yref="y"
            )

    return fig


@app.callback(
    Output("insight-dashboard-1", "figure"),
    Output("insight-dashboard-2", "figure"),
    Output("insight-dashboard-3", "figure"),
    Output("insight-dashboard-4", "figure"),
    Output("insight-dashboard-5", "figure"),
    Output("insight-dashboard-6", "figure"),
    [
        Input("dropdown-insight-timeaverage", "value")
    ]
)
def update_insights(timeaverage):
    fig1 = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=450,
            title={
                "text": "Accounts<br><span style='font-size:0.8em;color:gray'>Subtitle</span><br><span style='font-size:0.8em;color:gray'>Subsubtitle</span>"},
            # delta={'reference': 400, 'relative': True},
            # domain={'x': [0.6, 1], 'y': [0, 1]}
        ))

    fig2 = go.Figure(go.Indicator(
        mode="number+delta",
        value=4500,
        title={
            "text": "Accounts<br><span style='font-size:0.8em;color:gray'>Subtitle</span><br><span style='font-size:0.8em;color:gray'>Subsubtitle</span>"
        },
        # delta={'reference': 400, 'relative': True},
        # domain={'x': [0.6, 1], 'y': [0, 1]}
    ))

    fig3 = go.Figure(go.Indicator(
        mode="number+delta",
        value=45000,
        title={
            "text": "Accounts<br><span style='font-size:0.8em;color:gray'>Subtitle</span><br><span style='font-size:0.8em;color:gray'>Subsubtitle</span>"
        },
        # delta={'reference': 400, 'relative': True},
        # domain={'x': [0.6, 1], 'y': [0, 1]}
    ))

    fig4 = go.Figure(go.Indicator(
        mode="number+delta",
        value=450000,
        title={
            "text": "Accounts<br><span style='font-size:0.8em;color:gray'>Subtitle</span><br><span style='font-size:0.8em;color:gray'>Subsubtitle</span>"
        },
        # delta={'reference': 400, 'relative': True},
        # domain={'x': [0.6, 1], 'y': [0, 1]}
    ))

    fig5 = go.Figure(go.Indicator(
        mode="number+delta",
        value=450000,
        title={
            "text": "Accounts<br><span style='font-size:0.8em;color:gray'>Subtitle</span><br><span style='font-size:0.8em;color:gray'>Subsubtitle</span>"
        },
        # delta={'reference': 400, 'relative': True},
        # domain={'x': [0.6, 1], 'y': [0, 1]}
    ))

    fig6 = go.Figure(go.Indicator(
        mode="number+delta",
        value=450000,
        title={
            "text": "Accounts<br><span style='font-size:0.8em;color:gray'>Subtitle</span><br><span style='font-size:0.8em;color:gray'>Subsubtitle</span>"
        },
        # delta={'reference': 400, 'relative': True},
        # domain={'x': [0.6, 1], 'y': [0, 1]}
    ))

    return fig1, fig2, fig3, fig4, fig5, fig6


def generate_title(countries, case_type):
    # Case type search
    case_type = get_casetype(case_type)

    # Country list builder
    if len(countries) < 3:
        title_country = ' and '.join([str(_) for _ in countries])
    else:
        title_country = str(len(countries)) + " selected countries"

    return "{} in {}".format(case_type, title_country)


def get_casetype(case_type):
    return next((item['label'] for item in option_case_type if item["value"] == case_type), case_type)
