from dash import dash, html, dcc


app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div("I am alive!!")

app.layout = html.Div([
    'This is my slider',
    dcc.RangeSlider(min=0, max=5, value=[1, 3], marks={0: '0', 5: '5'})])

if __name__ == "__main__":
    app.run_server(debug=True)
