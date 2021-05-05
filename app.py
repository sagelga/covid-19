import dash

# App Initialize
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css',
                        'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__
    , suppress_callback_exceptions=True
    , title="COVID-19 Data Explorer"
    , meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}]
    , external_stylesheets=external_stylesheets
)
server = app.server
