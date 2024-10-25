import os
import requests
import pandas as pd
from content_filtering_redisVL.utils.logger import get_logger
from content_filtering_redisVL.utils.config import get_config


class MovieDataLoader:
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger("Implementation: Download the movies data and save in the current directory.")
        self.url = self.config.DATAURL


    def get_data(self) -> pd.DataFrame:
        try:
            self.logger.info("Downloading the movies dataset...")
            r = requests.get(self.url)

            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.logger.info(f"The absolute path of the current script's directory is {base_dir}")

            self.logger.info("Creating the target directory if it doesn't exist...")
            data_dir = os.path.join(base_dir, 'datasets', 'content_filtering')
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)

            self.logger.info(f"Saving the file to the data directory: {data_dir}")
            file_path = os.path.join(data_dir, '25k_imdb_movie_dataset.csv')
            with open(file_path, 'wb') as f:
                f.write(r.content)
            self.logger.info("IMDB Movie data file saved successfully in csv format")

            df = pd.read_csv(file_path)
            self.logger.info("Data read successfully.")
            return df
        except Exception as e:
            self.logger.error(f"Error loading imdb movie dataset: {e}")
            return None