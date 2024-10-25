import os
import pickle
import requests
import pandas as pd
from content_filtering_redisVL.utils.logger import get_logger
from content_filtering_redisVL.utils.config import get_config
# from content_filtering_redisVL.data.data_processing import MovieDataProcessor


class LoadEmbedding:
    def __init__(self, data):
        self.config = get_config()
        self.logger = get_logger("Using RedisVL embedding generators to generate semantic vector embeddings of the dataset descriptions")
        # self.data = MovieDataProcessor().get_full_text_data()
        self.data = data


    def load_embedding_pickle(self) -> pd.DataFrame:
        try:
            self.logger.info("Using an absolute path for safer file handling, to get the text embedded pickle file")
            embedding_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'text_embedding_file',
                                          'text_embeddings.pkl')

            self.logger.info("Get the text embedding file first from the location it was saved locally")
            with open(embedding_path, 'rb') as vector_file:
                self.data['embedding'] = pickle.load(vector_file)
                return self.data

        except FileNotFoundError:
            self.logger.info("If the file is not found, download it from the specified URL")
            embeddings_url = 'https://redis-ai-resources.s3.us-east-2.amazonaws.com/recommenders/datasets/content-filtering/text_embeddings.pkl'
            try:
                r = requests.get(embeddings_url, stream=True)
                self.logger.info("Raising an exception for HTTP errors")
                r.raise_for_status()

                self.logger.info("Create the directory to save the downloaded pickle file, if it doesn't exist in local")
                os.makedirs(os.path.dirname(embedding_path), exist_ok=True)

                self.logger.info("Saving the file in chunks to avoid stream errors")
                with open(embedding_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

                self.logger.info("Load the newly downloaded pickle file")
                with open(embedding_path, 'rb') as vector_file:
                    self.data['embedding'] = pickle.load(vector_file)
                    return self.data

            except requests.exceptions.RequestException as e:
                self.logger.info("Catch and log request-related errors")
                self.logger.error(f"Failed to download embeddings: {e}")
                return None

        except pickle.UnpicklingError as e:
            self.logger.info("Catch and log pickle file errors")
            self.logger.error(f"Failed to load embeddings from pickle file: {e}")
            return None

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            return None