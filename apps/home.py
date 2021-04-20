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


def generate_insight_cards(id, title, p):
    return html.Div(children=[
        html.Div(children=[
            dcc.Graph(id="insight-dashboard{}".format(id))
        ], className="four columns"),
        html.Div(children=[
            html.H5(title),
            html.P(p,
                   style={'align': 'justify'}
                   ),
        ], className="eight columns"),
    ], className="six columns")


# Website Builder
layout = html.Div([
    html.Div(children=[
        html.H2('Data'),
        html.P('Select indicators from the dropdown menu.')
    ]),
    # Options
    html.Div(children=[
        html.Div(children=[
            html.Label('📂 Case Type'),
            dcc.Dropdown(
                id="dropdown-casetype"
                , options=option_case_type
                , placeholder="Select a type"
                , value='new_cases'
                , multi=False
                , clearable=False
                , searchable=False
                , persistence=True
                , persistence_type='session'
            ),
        ], className="three columns"),

        html.Div(children=[
            html.Label('🌎 Countries'),
            dcc.Dropdown(
                id="dropdown-country"
                , options=[{"label": x, "value": x}
                           for x in all_country]
                , placeholder="Select a city"
                , value=['Thailand']
                , multi=True
                , clearable=True
                , searchable=True
                , persistence=True
                , persistence_type='session'
            ),
        ], className="three columns"),

        html.Div(children=[
            html.Label('📊 Chart Type'),
            dcc.Dropdown(
                id="dropdown-typechart"
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
                id="dropdown-timerange",
                options=[
                    {'label': 'All time', 'value': 'all'}
                    , {'label': '1 Week', 'value': '7d'}
                    , {'label': '2 Weeks', 'value': '14d'}
                    , {'label': '30 Days', 'value': '30d'}
                    , {'label': '90 Days', 'value': '90d'}
                    , {'label': '365 Days', 'value': '365d'}
                ]
                , placeholder="Select a range"
                , value='14d'
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
            html.Label('📊 Chart Indicators'),
            dcc.Dropdown(
                id="dropdown-chartoption"
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
                id="dropdown-regressionoption"
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

    html.Br(),

    html.Div(children=[
        html.H2('Insights'),
        html.P(
            'These are insights from your data selection. If you like to change the insight section, try adding/removing a country from the dropdown above.')
    ]),

    generate_insight_cards(1, 'Title', 'Subtitle'),
    generate_insight_cards(2, 'Title', 'Subtitle'),
    generate_insight_cards(3, 'Title', 'Subtitle'),
    generate_insight_cards(4, 'Title', 'Subtitle'),
])


@app.callback(
    Output("result-chart", "figure"),
    [
        Input("dropdown-casetype", "value")
        , Input("dropdown-country", "value")
        , Input("dropdown-typechart", "value")
        , Input("dropdown-chartoption", "value")
        , Input("dropdown-timerange", "value")
    ]
)
def update_graph(case_type, countries, type_chart, chart_indicator, time_range):
    # - Time Range -
    time_max = datetime.today()
    time_list = []
    for _ in range(1, int(time_range.replace('d', '')) + 1):
        time_check = time_max - timedelta(days=_)
        # if time_check in df['date']:
        time_check = time_check.strftime("%Y-%m-%d")
        time_list.append(time_check)

    # - Apply mask -
    mask = df['location'].isin(countries) & df['date'].isin(time_list)

    if type_chart == "area":  # Line Chart
        fig = px.area(df[mask]
                      , x="date"
                      , y=case_type
                      , color="location"
                      , hover_name="location"
                      )
        fig.update_traces(connectgaps=True
                          , mode="markers+lines"
                          , hovertemplate=None)
        fig.update_layout(hovermode="x unified")

    elif type_chart == "bar":  # Bar Chart
        fig = px.bar(df[mask]
                     , x="date"
                     , y=case_type
                     , color="location"
                     , hover_name="location"
                     , barmode="group"
                     )

    elif type_chart == "scatter":
        fig = px.scatter(df[mask]
                         , x="date"
                         , y=case_type
                         , color="location"
                         # , trendline="lowess"
                         )

    elif type_chart == "world":
        fig = px.choropleth(df[mask]
                            , locations="iso_code"
                            , color=case_type
                            , hover_name="location"
                            , animation_frame="date_str"
                            , color_continuous_scale=px.colors.sequential.Viridis
                            , projection='kavrayskiy7'
                            )
    else:
        fig = px.line(df[mask]
                      , x="date"
                      , y=case_type
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

    if type(chart_indicator) == list and type_chart not in ['world']:
        # Retrieve data
        # df[mask]

        # Max Line
        if 'max' in chart_indicator:
            y = 1200
            fig.add_shape(
                type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
                x0=0, x1=1, xref="paper", y0=y, y1=y, yref="y"
            )

        # Average Line
        if 'avg' in chart_indicator:
            y = 900
            fig.add_shape(
                type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
                x0=0, x1=1, xref="paper", y0=y, y1=y, yref="y"
            )

        # Min Line
        if 'min' in chart_indicator:
            y = 500
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
