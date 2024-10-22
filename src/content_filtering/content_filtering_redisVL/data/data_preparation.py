import pandas as pd
import os
import requests
from content_filtering_redisVL.utils.logger import get_logger
from content_filtering_redisVL.utils.config import get_config


class MovieDataLoader:
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger("load-data-and-change-data-to-DataFrame")
        self.url = self.config.DATAURL

    def get_data(self) -> pd.DataFrame:
        try:
            self.logger.info("download the movies data")
            r = requests.get(self.url)

            self.logger.info("Save the file as a csv")
            if not os.path.exists('./datasets/content_filtering'):
                os.makedirs('./datasets/content_filtering')
            with open('./datasets/content_filtering/25k_imdb_movie_dataset.csv', 'wb') as f:
                f.write(r.content)
            df = pd.read_csv("datasets/content_filtering/25k_imdb_movie_dataset.csv")
            self.logger.info("Data read successfully.")
            return df
        except Exception as e:
            self.logger.error(f"Error loading imdb movie dataset: {e}")



# df = MovieDataLoader().get_data()
# print(df.describe())