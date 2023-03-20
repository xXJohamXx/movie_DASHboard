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

data_table_columns = [
    'title', 'tagline', 'genre_list', 'vote_average','runtime', 
    'release_date', 'budget', 'revenue','production_companies', 
    'recommendations']


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Movie Explorer Dashboard",
                        className='text-center'),
            dcc.Graph(
                id='bar-chart',
                style={"border-width": "0", "width": "100%", "height": "400px"}
            ),
        ], width={'size':11}),


    ], justify='center'),

    dbc.Row([
        dbc.Col([
            html.Label('Select a Rating Range'
            ),
            dcc.RangeSlider(
                id="rating",
                min=0,
                max=10,
                step=0.01,
                value=[5,7.5],
                marks={0: "0", 10: "10"},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            html.Label('Select Runtime Range'       
            ),
            dcc.RangeSlider(
                id="runtime",
                min=1,
                max=300,
                step=5,
                value=[60,120],
                marks={1: "0", 60: "60", 120: "120", 180: "180", 240: "240", 300: "300"},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
        ], width= 7),

        dbc.Col([
            html.Label('Select a Genre From The List'       
            ),
            dcc.Dropdown(
                id='selected_genre',
                options=genre_list,
                placeholder="Select a Genre"
            ),
            html.Br(),
            html.A(html.Button('Click To Reset All Filters'),href='/'),
    
        ], width = 3)
    
    ], justify="center"),

    dbc.Row([
        dbc.Col([
            html.H3("Explore The Movies!",
                   className='text-center'),
            dash_table.DataTable(
            id='datatable',
            columns=[{'name': col, 'id': col} for col in data_table_columns],
            data=[],
            sort_action='native',
            # style_data={
            #     'whiteSpace': 'normal',
            #     # 'height': 'auto',
            #     'lineHeight': '15px'
            # },
            page_size=10,

            style_table={'overflowX': 'auto'},

            style_cell={'textAlign': 'center'} # left align text in columns for readability

            )   
    
        ], width= 12)
    ])


], fluid=True)



@app.callback(
        # Output("barchart", "srcDoc"), 
        Output('bar-chart', 'figure'),
        Output('datatable', 'data'),
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
        
    data_table = filtered_movies[data_table_columns].to_dict('records')


    tooltips = [filtered_movies['overview'].str.wrap(50).apply(lambda x: x.replace('\n', '<br>')), 
                filtered_movies['runtime'],
                filtered_movies['revenue'], filtered_movies['genre_list'],
                filtered_movies['vote_count']
    ]

    hovertemp = ('<b>Synopsis</b>: <br>%{customdata[0]}<br><br>' +
                               '<b>Runtime (mins)</b>: %{customdata[1]}<br>' +
                               '<b>Gross Revenue (USD)</b>: $%{customdata[2]:,}<br>' +
                               '<b>Genres</b> %{customdata[3]}<br>' +
                               '<b>Votes</b>: %{customdata[4]}<extra></extra>')



    fig = px.bar(filtered_movies, x="vote_count", y='title', color='vote_average',
                 labels= {"vote_count" : "Average Number of Votes",
                          "title" : "Movie Title",
                          "vote_average" : "Average Score" },
                # hover_data=
                # barmode= "group",
                custom_data=tooltips
                          )
    fig.update_layout(
    title={
        'text': "Top 10 Movies By Rating",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    
    # fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
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



    return (fig, data_table)


if __name__ == "__main__":
    app.run_server(debug=True)
