import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import time

# App Initialize
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}],
    external_stylesheets=external_stylesheets
)
server = app.server

app.title = "COVID-19 Data Explorer"
app.config["suppress_callback_exceptions"] = True

# Data Import
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
df = pd.read_csv(url)

# Data Transform
df.date = pd.to_datetime(df.date)
df = df.sort_values(by=['date', 'location'])

# Data selection
df = df.dropna(subset=['continent'])
df = df.dropna(subset=['location'])

# Calculate fields
df['people_vaccinated_per_population'] = 100 * (df['people_vaccinated'] / df['population'])
df['people_fully_vaccinated_per_population'] = 100 * (df['people_fully_vaccinated'] / df['population'])

# Calculate fields
a=int((time.time()/900-3)/2%24)
curr_time = chr(128336+a//2+a%2*12)

# Reused Components
option_case_type = [
    {'label': 'New confirmed cases', 'value': 'new_cases'},
    {'label': 'New deaths attributed', 'value': 'new_deaths'},
    {'label': 'Total confirmed cases', 'value': 'total_cases'},
    {'label': 'Total deaths attributed', 'value': 'total_deaths'},
    {'label': 'Vaccinated one dose', 'value': 'people_vaccinated'},
    {'label': 'Vaccinated all doses', 'value': 'people_fully_vaccinated'},
    {'label': 'Total confirmed cases per million people', 'value': 'total_cases_per_million'},
    {'label': 'Total deaths per million people', 'value': 'total_deaths_per_million'},
    {'label': 'Vaccinated one dose per population', 'value': 'people_vaccinated_per_population'},
    {'label': 'Vaccinated all doses per population', 'value': 'people_fully_vaccinated_per_population'},
]

# Website Builder
all_country = df.location.unique()
app.layout = html.Div([
    html.Div([], className="one columns"),
    html.Div([
        html.Div(children=[
            html.H1('COVID-19 Data Explorer'),
        ]),

        html.Div(children=[

            html.Div(children=[
                html.H5('🌎 Countries'),
                dcc.Dropdown(
                    id="dropdown-country",
                    options=[{"label": x, "value": x}
                             for x in all_country],
                    placeholder="Select a city",
                    value=['Thailand'],
                    multi=True
                ),
            ], className="three columns"),

            html.Div(children=[
                html.H5('📊 Case Type'),
                dcc.Dropdown(
                    id="dropdown-casetype",
                    options=option_case_type,
                    placeholder="Select a type",
                    value='total_cases',
                    multi=False,
                    clearable=False,
                    # disabled=True
                ),
            ], className="three columns"),

            html.Div(children=[
                html.H5(curr_time +' Time Range'),
                dcc.Dropdown(
                    id="dropdown-timerange",
                    options=[
                        {'label': 'All time', 'value': 'all'},
                        {'label': '1 Week', 'value': '7d'},
                        {'label': '2 Weeks', 'value': '14d'},
                        {'label': '30 Days', 'value': '30d'},
                        {'label': '90 Days', 'value': '90d'}
                    ],
                    placeholder="Select a range",
                    value='all',
                    multi=False,
                    clearable=False,
                    disabled=True
                ),
                # html.Button('Submit', id='submit-val', n_clicks=0),
            ], className="three columns"),

            html.Div(children=[
                html.H5('🔢 Data Source'),
                dcc.Dropdown(
                    id="dropdown-datasource",
                    options=[
                        {'label': 'Default', 'value': 'default'},
                    ],
                    placeholder="Select a data source",
                    value='default',
                    multi=False,
                    clearable=False
                ),
            ], className="three columns"),
        ], className="row"),

        # Chart
        html.Div(children=[
            dcc.Graph(id="active-case")
        ]),

        html.Div(children=[
            html.P('Datasource from https://github.com/owid/covid-19-data/'),
            html.P('Repository : https://github.com/sagelga/covid-vaccine'),
        ]),
    ], className="ten columns"),
    html.Div([], className="one columns")
], className="row")


@app.callback(
    Output("active-case", "figure"),
    [Input("dropdown-country", "value"),
     Input("dropdown-casetype", "value"),
     Input("dropdown-timerange", "value"),
     Input("dropdown-datasource", "value")]
)
def update_graph(countries, case_type, time_range, data_source):
    # Data Re-categorizing
    # - Countries -
    mask = df.location.isin(countries)
    # - Time Range -
    time_range = "date"

    if len(countries) < 3:
        title_country = ' and '.join([str(i) for i in countries])
    else:
        title_country = str(len(countries)) + " selected countries"

    # Active Case Line Chart
    figure = px.line(
        df[mask],
        x=time_range,
        y=case_type,
        color="location",
        hover_name="location",
        hover_data=['date', 'total_cases']
    )

    title = "{} in {}".format(case_type, title_country)
    figure.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=str(case_type)
    )
    figure.update_traces(connectgaps=True)

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
