import os
import requests
import pandas as pd
import numpy as np

from surprise import SVD
from surprise import Dataset, Reader
from surprise.model_selection import train_test_split

from collaborative_filtering_redisVL.data.movies_dataset import split_data
train_set, test_set = split_data(ratings_data)

def svd_model(n_factors:int = 100, biased:bool = False):
    # use SVD (Singular Value Decomposition) for collaborative filtering
    svd = SVD(n_factors, biased)  # we'll set biased to False so that predictions are of the form "rating_prediction = user_vector dot item_vector"
    return svd


def svd_trainingset(model_svd: SVD, training_set: pd.DataFrame):
    # train the algorithm on the train set
    model_svd.fit(training_set)


def user_latent_feature_matrix(model_svd:SVD):
    user_vectors = model_svd.pu  # user latent features (matrix)
    return user_vectors


def movie_latent_feature_matrix(model_svd:SVD):
    movie_vectors = model_svd.qi  # movie latent features (matrix)
    return movie_vectors


svd = svd_model()
svd_trainingset(model_svd=svd, training_set=train_set)