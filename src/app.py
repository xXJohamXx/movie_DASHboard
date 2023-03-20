import os 

from dash import dash, html, dcc, Input, Output, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


# load data
movies = pd.read_csv(os.path.join(os.pardir,"data","clean","tmdb_movies_clean.csv"))

genre_list = [ 'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary',
               'Drama', 'Family', 'Fantasy', 'History','Horror', 'Music', 'Mystery',
               'Romance','Science Fiction','TV Movie','Thriller','War','Western']

data_table_columns = [
    'title','recommendations', 'vote_average','runtime', 
    'release_date', 'budget', 'revenue', 'tagline', 'genre_list',
    'production_companies', 
    ]


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

server = app.server

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
            html.A(html.Button('Click To Refresh Page and Reset All Filters'),href='/'),
    
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
                        editable=True,
                        sort_action='native',
                        sort_mode= 'multi',
                        row_selectable='multi',
                        row_deletable=True,
                        selected_rows=[],
                        selected_columns=[],
                        page_action='native',
                        page_current= 0,
                        page_size=20,
                        style_data={'whiteSpace': 'normal','height': 'auto',},
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'center'} # left align text in columns for readability

            )   
    
        ], width= 12)
    ])


], fluid=True)



@app.callback(
        Output('bar-chart', 'figure'),
        Output('datatable', 'data'),
        [Input("selected_genre", "value"),
        Input("rating", "value"),
        Input("runtime", "value")]
        )
def plot_table(selected_genre, rating, runtime):


    if  selected_genre == None:
        filtered_movies =  (
                    movies.
                    query(
                        "vote_average <= @rating[1] & " 
                        "vote_average >= @rating[0] & " 
                        "runtime <= @runtime[1] & "
                        "runtime >= @runtime[0] & " 
                        "revenue > 0")
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
                    )
        
    data_table = filtered_movies[data_table_columns].to_dict('records')

    # get top 10 movies to plot and create tooltips
    barplot_movies = (
                filtered_movies
                .sort_values(["vote_average", "vote_count"], ascending=[False, False])
                .head(10)
    )

    tooltips = [barplot_movies['overview'].str.wrap(50).apply(lambda x: x.replace('\n', '<br>')), 
                barplot_movies['runtime'],
                barplot_movies['revenue'], 
                barplot_movies['genre_list'],
                barplot_movies['vote_count']
    ]

    hovertemp = ('<b>Synopsis</b>: <br>%{customdata[0]}<br><br>' +
                               '<b>Runtime (mins)</b>: %{customdata[1]}<br>' +
                               '<b>Gross Revenue (USD)</b>: $%{customdata[2]:,}<br>' +
                               '<b>Genres</b> %{customdata[3]}<br>' +
                               '<b>Votes</b>: %{customdata[4]}<extra></extra>')


    fig = px.bar(barplot_movies, 
                 x="vote_count", y='title', color='vote_average',
                 labels= {"vote_count" : "Average Number of Votes",
                          "title" : "Movie Title",
                          "vote_average" : "Average Score" },
                custom_data=tooltips
                          )
    fig.update_layout(
    title={
        'text': "Top 10 Movies By Rating",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
    )
    
    fig.update_traces(hovertemplate=hovertemp)

    return (fig, data_table)


if __name__ == "__main__":
    app.run_server(debug=True)
