import os
import requests
import pandas as pd
import numpy as np

from surprise import SVD
from surprise import Dataset, Reader
from surprise.model_selection import train_test_split

from redis.commands.json.path import Path

from collaborative_filtering_redisVL.data.movies_dataset import split_data

from src.collaborative_filtering.collaborative_filtering_redisVL.pipeline.load_data_redis import ratings_df

train_set, test_set = split_data(ratings_data)

from collaborative_filtering_redisVL.models.svd_model import user_latent_feature_matrix, movie_latent_feature_matrix
user_vectors = user_latent_feature_matrix()
movie_vectors = movie_latent_feature_matrix()

from collaborative_filtering_redisVL.data.movies_dataset import merge_movies_and_links_data
merged_movies_data = merge_movies_and_links_data()

from collaborative_filtering_redisVL.utils.connect_redis import RedisClient
client = RedisClient().connect()


# surprise casts userId and movieId to inner ids, so we have to use their mapping to know which rows to use
inner_uid = train_set.to_inner_uid(347) # userId
inner_iid = train_set.to_inner_iid(5515) # movieId

# predict one user's rating of one film
predicted_rating = np.dot(user_vectors[inner_uid], movie_vectors[inner_iid])
print(f'the predicted rating of user {347} on movie {5515} is {predicted_rating}')


def user_vector_dataset():
    # build a dataframe out of the user vectors and their userIds
    user_vectors_and_ids = {train_set.to_raw_uid(inner_id): user_vectors[inner_id].tolist() for inner_id in train_set.all_users()}
    user_vector_df = pd.Series(user_vectors_and_ids).to_frame('user_vector')
    return user_vector_df

def movie_vector_dataset():
    # now do the same for the movie vectors and their movieIds
    movie_vectors_and_ids = {train_set.to_raw_iid(inner_id): movie_vectors[inner_id].tolist() for inner_id in train_set.all_items()}
    movie_vector_df = pd.Series(movie_vectors_and_ids).to_frame('movie_vector')
    return movie_vector_df

def merged_movie_vector_series():
    # merge the movie vector series with the movies dataframe using the movieId and id fields
    movies_df = merged_movies_data.merge(movie_vector_df, left_on='movieId', right_index=True, how='inner')
    movies_df['movieId'] = movies_df['movieId'].apply(lambda x: str(x)) # need to cast to a string as this is a tag field in our search schema
    return movies_df

def store_user_vector():
    user_vectors_and_ids = {train_set.to_raw_uid(inner_id): user_vectors[inner_id].tolist() for inner_id in
                            train_set.all_users()}
    # use a Redis pipeline to store user data and verify it in a single transaction
    with client.pipeline() as pipe:
        for user_id, user_vector in user_vectors_and_ids.items():
            user_key = f"user:{user_id}"
            watched_list_ids = ratings_df[ratings_df['userId'] == user_id]['movieId'].tolist()

            user_data = {
                "user_vector": user_vector,
                "watched_list_ids": watched_list_ids
            }
            pipe.json().set(user_key, Path.root_path(), user_data)
            pipe.execute()




































