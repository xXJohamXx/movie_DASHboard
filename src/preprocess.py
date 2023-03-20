# Author: Jonah Hamilton
# date: 2023-03-12

import os


import pandas as pd
import numpy as np

# read in movie data retrieved from: https://www.kaggle.com/datasets/akshaypawar7/millions-of-movies?resource=download, file subsetted to save space
# movies = pd.read_csv("../data/raw/tmdb_movies.csv")
movies = pd.read_csv(os.path.join(os.pardir,"data","raw","tmdb_movies.csv"))

# pre-process csv for dashboard
movies = (
    movies.drop(columns=["popularity", "backdrop_path"])
    .dropna(subset=["genres", "runtime", "release_date", "overview"])
    .assign(
        release_date=pd.to_datetime(movies["release_date"]),
        production_companies=movies["production_companies"].str.split("-"),
        genre_list=movies["genres"].str.split("-"),
        credits=movies["credits"].str.split("-"),
        keywords=movies["keywords"].str.split("-"),
        recommendations=movies["recommendations"].str.split("-"),
        vote_average=movies['vote_average'].round(2)
    )
    .reset_index(drop=True)
)

#create dictionary of movie ids and titles
movie_id = dict(zip(list(movies["id"]), list(movies["title"])))

#repace movie reccomendation ids with movie titles
for i in range(len(movies)):
    for j in range(len(movies['recommendations'][i])):

        if int(movies['recommendations'][i][j]) in movie_id.keys():
            movies['recommendations'][i][j] = movie_id[int(movies['recommendations'][i][j])] 
        else:
            movies['recommendations'][i][j] = np.nan

#remove nan values  keep original values from df column of lists
movies['recommendations'] = movies['recommendations'].apply(lambda x: [item for item in x if item is not np.nan])

# movies.to_csv("../data/clean/tmdb_movies_clean.csv")
movies.to_csv(os.path.join(os.pardir,"data", "clean", "tmdb_movies_clean.csv"))
