# Author: Jonah Hamilton
# date: 2023-03-12

# read in movie data retrieved from: https://www.kaggle.com/datasets/akshaypawar7/millions-of-movies?resource=download, file subsetted to save space
import pandas as pd
import numpy as np

movies = pd.read_csv("../data/raw/tmdb_movies.csv")

# pre-process csv for dashboard
movies = (
    movies.drop(columns=["popularity", "backdrop_path"])
    .dropna(subset=["genres", "runtime", "release_date"])
    .assign(
        release_date=pd.to_datetime(movies["release_date"]),
        production_companies=movies["production_companies"].str.split("-"),
        genres=movies["genres"].str.split("-"),
        credits=movies["credits"].str.split("-"),
        keywords=movies["keywords"].str.split("-"),
        recommendations=movies["recommendations"].str.split("-"),
    )
    .reset_index(drop=True)
)

movies.to_csv("../data/clean/tmdb_movies_clean.csv")
