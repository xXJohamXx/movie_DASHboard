from dash import dash, html, dcc, Input, Output
import altair as alt
import pandas as pd
import numpy as np

# import dash_bootstrap_components as dbc


# load data
movies = pd.read_csv("../data/clean/tmdb_movies_clean.csv")

# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)

app.layout = html.Div(
    [
        html.Iframe(
            id="barchart",
            style={"border-width": "0", "width": "100%", "height": "400px"},
        ),
        "Select Rating Range",
        dcc.RangeSlider(
            id="vote_slider",
            min=0,
            max=10,
            step=0.001,
            value=[0, 10],
            marks={0: "0", 10: "10"},
        ),
    ]
)


@app.callback(Output("barchart", "srcDoc"), Input("vote_slider", "value"))
def plot_altair(max_vote, df=movies.copy()):
    filtered_movies = df.query("vote_average > @max_vote & revenue > 0 ").sort_values(
        ["vote_average", "vote_count"]
    )[0:10]

    tooltips = [
        alt.Tooltip("overview", title="Synopsis"),
        alt.Tooltip("runtime", title="Runtime (mins)"),
        alt.Tooltip("revenue", title="Gross Revenue (USD)"),
        alt.Tooltip("vote_count", title="Votes"),
    ]

    bar_chart = (
        alt.Chart(filtered_movies)
        .mark_bar()
        .encode(
            x=alt.X(
                "vote_count",
                title="Average Number of Votes",
                scale=alt.Scale(zero=False),
            ),
            y=alt.Y(
                "title",
                sort="-x",
                title="Movie Title",
            ),
            color=alt.Color(
                "vote_average",
                title="Average Vote Score",
            ),
            tooltip=tooltips,
        )
    )

    return bar_chart.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)
