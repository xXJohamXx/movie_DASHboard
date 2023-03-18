import os 

from dash import dash, html, dcc, Input, Output, dash_table
import plotly.express as px
import altair as alt
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc


# load data
movies = pd.read_csv(os.path.join(os.pardir,"data","clean","tmdb_movies_clean.csv"))


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


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
# app = dash.Dash(
#     __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
# )

app.layout = html.Div(
    [
        # html.Iframe(
        #     id="barchart",
        #     style={"border-width": "0", "width": "100%", "height": "400px"},
        # ),
        dcc.Graph(id='bar-chart',
                  style={"border-width": "0", "width": "100%", "height": "400px"}),
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
        # Output("barchart", "srcDoc"), 
        Output('bar-chart', 'figure'),
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
        filtered_movies = (
                    movies
                    .query(
                        "vote_average <= @rating[1] & "
                        "vote_average >= @rating[0] & " 
                        "runtime <= @runtime[1] & "
                        "runtime >= @runtime[0] & revenue > 0"
                    )
                    .loc[movies['genres'].str.contains(selected_genre),:]
                    .sort_values(["vote_average", "vote_count"], ascending=False)
                    .head(10)
                    )


    tooltips = [filtered_movies['overview'], filtered_movies['runtime'],
                filtered_movies['revenue'], filtered_movies['genre_list'],
                filtered_movies['vote_count']
    ]

    hovertemp = ('Synopsis: %{tooltips[0]}<br>' +
                               'Runtime (mins): %{tooltips[1]}<br>' +
                               'Gross Revenue (USD): %{tooltips[2]:.2f}<br>' +
                               'TGenres: %{tooltips[3]:.2f}<br>' +
                               'Votes: %{tooltips[4]:.2f}<br>')



    fig = px.bar(filtered_movies, x="vote_count", y='title', color='vote_average',
                 title= "Top 10 Rated Movies",
                 labels= {"vote_count" : "Average Number of Votes",
                          "title" : "Movie Title",
                          "vote_average" : "Average Vote Score" },
                # barmode= "group",
                custom_data=tooltips
                          )
    fig.update_layout(barmode='group', xaxis={'categoryorder':'total ascending'})
    # Set the custom hover text labels

    fig.update_traces(hovertemplate=hovertemp)
    # fig.update_layout(yaxis=dict(autorange="reversed"))
    

        # Set the plot layout
    # fig.update_layout(
    #     margin=dict(l=20, r=20, t=30, b=20),
    #     xaxis_title='Fruit',
    #     yaxis_title='Count',
    #     font=dict(size=12)
    # )



    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
