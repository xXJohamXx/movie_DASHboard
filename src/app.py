import os 

from dash import dash, html, dcc, Input, Output
import altair as alt
import pandas as pd
import numpy as np

# import dash_bootstrap_components as dbc


# load data
# movies = pd.read_csv("../data/clean/tmdb_movies_clean.csv")
movies = pd.read_csv(os.path.join(os.pardir,"data","clean","tmdb_movies_clean.csv"))
# movies['genres'] = str(movies['genres'])

# genre_list = movies.explode('genres')["genres"].unique()
# genre_list = sorted(movies.explode('genres')['genres'].unique())

genre_list = [
 'Action',
 'Adventure',
 'Animation',
 'Comedy',
 'Crime',
 'Documentary',
 'Drama',
 'Family',
 'Fantasy',
 'History',
 'Horror',
 'Music',
 'Mystery',
 'Romance',
 'Science Fiction',
 'TV Movie',
 'Thriller',
 'War',
 'Western']


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
            id='selected_genre',
            options=genre_list,
            # multi=True,
            # value= 'Drama',
            # clearable=False,
            placeholder="Select a Genre"
        ),
    ]
)


@app.callback(
        Output("barchart", "srcDoc"), 
        [Input("selected_genre", "value"),
        Input("rating", "value"),
        Input("runtime", "value")]
        )
def plot_altair(selected_genre, rating, runtime):


    if  selected_genre == None:
        filtered_movies =  (
                    movies.
                    query(
                        "vote_average <= @rating[1] & " 
                        "vote_average >= @rating[0] & " 
                        "runtime <= @runtime[1] & "
                        "runtime >= @runtime[0] & " 
                        "revenue > 0")
                        .sort_values(["vote_average", "vote_count"], ascending=False)
                        .head(10)
                        )     

    else:
        print(selected_genre, type(selected_genre), movies.columns, type(movies["genres"][0]))
        filtered_movies = (
                    movies
                    .query(
                        "vote_average <= @rating[1] & "
                        "vote_average >= @rating[0] & " 
                        "runtime <= @runtime[1] & "
                        "runtime >= @runtime[0] & revenue > 0"
                    )
                    .loc[movies['genre_list'].str.contains(selected_genre),:]
                    .sort_values(["vote_average", "vote_count"], ascending=False)
                    .head(10)
                    )

   
    tooltips = [
        alt.Tooltip("overview", title="Synopsis"),
        alt.Tooltip("runtime", title="Runtime (mins)"),
        alt.Tooltip("revenue", title="Gross Revenue (USD)"),
        alt.Tooltip("vote_count", title="Votes"),
        alt.Tooltip("genre_list", title="Genres"),
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
