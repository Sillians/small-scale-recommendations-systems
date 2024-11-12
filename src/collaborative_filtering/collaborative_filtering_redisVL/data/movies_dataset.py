import os
import requests
import pandas as pd
import numpy as np
from surprise import Dataset, Reader
from surprise.model_selection import train_test_split
import datetime


def fetch_dataframe(file_name):
    try:
        df = pd.read_csv('datasets/collaborative_filtering/' + file_name)
    except:
        url = 'https://redis-ai-resources.s3.us-east-2.amazonaws.com/recommenders/datasets/collaborative-filtering/'
        r = requests.get(url + file_name)
        if not os.path.exists('datasets/collaborative_filtering'):
            os.makedirs('datasets/collaborative_filtering')
        with open('datasets/collaborative_filtering/' + file_name, 'wb') as f:
            f.write(r.content)
        df = pd.read_csv('datasets/collaborative_filtering/' + file_name)
    return df


def movies_dataset():
    movies_df = fetch_dataframe('movies_metadata.csv')
    movies_df.drop(columns=['homepage', 'production_countries', 'production_companies', 'spoken_languages', 'video',
                            'original_title', 'video', 'poster_path', 'belongs_to_collection'], inplace=True)

    # drop rows that have missing values
    movies_df.dropna(subset=['imdb_id'], inplace=True)

    movies_df['original_language'] = movies_df['original_language'].fillna('unknown')
    movies_df['overview'] = movies_df['overview'].fillna('')
    movies_df['popularity'] = movies_df['popularity'].fillna(0)
    movies_df['release_date'] = movies_df['release_date'].fillna('1900-01-01').apply(
        lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").timestamp())
    movies_df['revenue'] = movies_df['revenue'].fillna(0)
    movies_df['runtime'] = movies_df['runtime'].fillna(0)
    movies_df['status'] = movies_df['status'].fillna('unknown')
    movies_df['tagline'] = movies_df['tagline'].fillna('')
    movies_df['title'] = movies_df['title'].fillna('')
    movies_df['vote_average'] = movies_df['vote_average'].fillna(0)
    movies_df['vote_count'] = movies_df['vote_count'].fillna(0)
    movies_df['genres'] = movies_df['genres'].apply(
        lambda x: [g['name'] for g in eval(x)] if x != '' else [])  # convert to a list of genre names
    movies_df['imdb_id'] = movies_df['imdb_id'].apply(lambda x: x[2:] if str(x).startswith('tt') else x).astype(
        int)  # remove leading 'tt' from imdb_id

    # make sure we've filled all missing values
    movies_df.isnull().sum()
    return movies_df

def get_links_dataset():
    links_df = fetch_dataframe('links_small.csv')  # for a larger example use 'links.csv' instead
    return links_df

def merge_movies_and_links_data():
    movies_df = movies_dataset()
    links_df = get_links_dataset()
    merged_movies_data = movies_df.merge(links_df, left_on='imdb_id', right_on='imdbId', how='inner')
    return merged_movies_data

def ratings_columns_df():
    ratings_df = fetch_dataframe('ratings_small.csv')  # for a larger example use 'ratings.csv' instead
    # only keep the columns we need: userId, movieId, rating
    ratings_df = ratings_df[['userId', 'movieId', 'rating']]
    return ratings_df


def get_ratings_data(ratings_df: pd.DataFrame) -> pd.DataFrame:
    ratings_df = ratings_columns_df()
    reader = Reader(rating_scale=(0.0, 5.0))
    ratings_data = Dataset.load_from_df(ratings_df, reader)
    return ratings_data


def split_data(ratings_data: pd.DataFrame):
    # split the data into training and testing sets (80% train, 20% test)
    train_set, test_set = train_test_split(ratings_data, test_size=0.2)
    return train_set, test_set



ratings_df = fetch_dataframe('ratings_small.csv') # for a larger example use 'ratings.csv' instead
print(ratings_df.head())


