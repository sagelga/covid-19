import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app initialize
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}],
    external_stylesheets=external_stylesheets
)
server = app.server
app.title = "COVID-19 Data Visualize"
app.config["suppress_callback_exceptions"] = True

# Data Import
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
df = pd.read_csv(url)
# r = requests.get(url, allow_redirects=True)
# df = open('owid-covid-data.csv', 'wb').write(r.content)

# Data Transform
df.date = pd.to_datetime(df.date)

# Data selection
df = df.dropna(subset=['continent'])
df = df.dropna(subset=['location'])

# Calculate fields
df['ppl_vaccinated'] = 100*(df['people_vaccinated'] / df['population'])

# Selection bar
all_country = df.location.unique()
app.layout = html.Div([
    html.Div(children=[
        html.H1('covid-vaccines'),
        html.P('Datasource from https://github.com/owid/covid-19-data/'),
    ]),
    html.Div(children=[
        # dcc.Graph(id="active-case"),
        dcc.Graph(id="vaccinate-timeline"),
    ]),
    html.Div(children=[
        html.H5('Change visible countries'),

        dcc.Dropdown(
            id="dropdown",
            options=[{"label": x, "value": x}
                     for x in all_country],
            value=all_country,
            multi=True
        ),
    ]),
],)


# Create Vaccinated-Total Population Line Chart
@app.callback(
    Output("vaccinate-timeline", "figure"),
    [Input("dropdown", "value")]
)
def vaccinate_timeline(countries):
    mask = df.location.isin(countries)
    country_count = df.location.nunique()
    country_selected = df[mask].location.nunique()

    fig = px.line(df[mask], x="date", y="ppl_vaccinated", title='Total Cases',
                  color="continent", hover_name="location")
    title = "Vaccinated population in {} of {} countries".format(
        country_selected, country_count)
    fig.update_layout(title=title,
                      xaxis_title='Date', yaxis_title='Percent Vaccinated')
    fig.update_traces(connectgaps=True, selector=dict(type='scatter'))
    return fig


# Create Active Case Line Chart
# @app.callback(
#     Output("active-case", "figure"),
#     [Input("dropdown", "value")]
# )
# def active_case(countries):
#     mask = df.location.isin(countries)
#     country_count = df.location.nunique()
#     country_selected = df[mask].location.nunique()
#
#     fig = px.line(df[mask], x="date", y="total_cases",
#                   color="continent", hover_name="location")
#
#     title = "Total Case in {} of {} countries".format(
#         country_selected, country_count)
#     fig.update_layout(title=title,
#                       xaxis_title='Date', yaxis_title='Total Case')
#     fig.update_traces(connectgaps=True, selector=dict(type='scatter'))
#     return fig


if __name__ == '__main__':
    app.run_server(debug=True)
