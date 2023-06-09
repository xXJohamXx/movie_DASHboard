
# Movie Dashboard Proposal

Author: Jonah Hamilton. Date: March 19, 2023

## Motivation & Purpose

The motivation behind creating a movie data exploration dashboard is to
provide an easy-to-use and efficient way for people to find and select
movies to watch. The purpose of the dashboard is to allow users to
explore a movie dataset quickly, filtering movies based on various
criteria, such as genre, runtime, and rating.

The target audience for this dashboard could be anyone interested in
finding a new movie to watch, whether it be for entertainment or
educational purposes.

The dashboard could solve the problem of decision fatigue, which often
occurs when people are overwhelmed with choices and have to spend a lot
of time searching for a movie to watch. By providing relevant
information and filters, the dashboard can help users quickly narrow
down their choices and find a movie that aligns with their preferences,
saving them time and effort.

## Data Description

For this version of the app (assignment for UBC DSCI 532 the dashboard
was created using the [TMDB](https://www.themoviedb.org/?language=en-CA)
data set created by [Akshay
Pawar](https://www.kaggle.com/datasets/akshaypawar7/millions-of-movies?resource=download).
The dataset contains more than 700,000 movies listed in the TMDB
Dataset. Due to storage limitations, a smaller subset is used for this
app. In the future, connecting the app directly to the TMDB api would be
a better option. The primary fields that will be presented and used for
filtering are include:

-   `title`: The Movie Title

-   `genres`: A '-' separated list of what genres the movie is tagged
    with.

-   `overview`: A short description of the movie

-   `runtime`: The length of the movie

-   `vote_average` average of votes given by tmdb users

-   `vote_count`: number of votes received

-   `revenue`: revenue generated by movie

## Research Question

The main research question is: What features and factors contribute to
the effectiveness of a movie dashboard app in helping users find a movie
to watch in the shortest amount of time?

## User Persona

**Name**: Samantha.\
**Age**: 27. Occupation: Marketing Manager.\
**Interests**:Reading,watching movies, and travelling.\
**Technology proficiency**: Comfortable with using mobile and desktop
applications

**User story**:

Samantha is a busy marketing manager who enjoys watching movies to
unwind after work. She often struggles to find movies that suit her mood
or match her preferences, and spends a lot of time scrolling through
movie lists and reading reviews. One evening, Samantha decides to use
the movie dashboard app to help her find a movie to watch. She opens the
app on her laptop and sees a homepage with various movie genres and
filters. She selects the 'Drama' genre and applies the '7-8 vote
average' rating filter. The dashboard displays a list of relevant
movies, and Samantha clicks on a movie that catches her attention. She
reads the synopsis, and sees that the movie has a high box office
revenue. Samantha decides to watch the movie and notes the other
recommended movies to check out in the future. She feels relieved to
have found a suitable movie in a matter of minutes and plans to use the
app regularly for her movie recommendations.
