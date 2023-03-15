from dash import dash, html, dcc, Input, Output
import altair as alt
import pandas as pd
import numpy as np

# import dash_bootstrap_components as dbc


# load data
movies = pd.read_csv("../data/clean/tmdb_movies_clean.csv")

# genre list
# genre_list = list(movies.explode("genres")["genres"].unique())

genre_list = [
    "Horror",
    "Mystery",
    "Thriller",
    "Action",
    "Adventure",
    "Animation",
    "Comedy",
    "Family",
    "Science Fiction",
    "Drama",
    "War",
    "History",
    "Crime",
    "Romance",
    "Fantasy",
    "Documentary",
    "Music",
    "TV Movie",
    "Western",
]

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
            id="rating",
            min=0,
            max=10,
            step=0.001,
            value=[5,7],
            marks={0: "0", 10: "10"},
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        "Select Runtime",
        dcc.RangeSlider(
            id="runtime",
            min=1,
            max=300,
            step=10,
            value=[60,120],
            marks={1: "0", 60: "60", 120: "120", 180: "180", 240: "240", 300: "300"},
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        "Select Genres From the List",
        dcc.Dropdown(
            # options=[{"label": i, "value": i} for i in genre_list],
            options=genre_list,
            multi=True,
            placeholder="Select a Genre",
        ),
    ]
)


@app.callback(
        Output("barchart", "srcDoc"), 
        Input("rating", "value"),
        Input("runtime", "value"))
def plot_altair(rating, runtime):
    filtered_movies = (
        movies.query("vote_average <= @rating[1] & vote_average >= @rating[0]" 
                     "& runtime <= @runtime[1] & runtime >= @runtime[0] & revenue > 0")
        .sort_values(["vote_average", "vote_count"], ascending=False)
        .head(10)
    )

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
