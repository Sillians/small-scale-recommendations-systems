import ast
import pandas as pd
from content_filtering_redisVL.utils.logger import get_logger
from content_filtering_redisVL.utils.config import get_config
# from content_filtering_redisVL.data.data_preparation import MovieDataLoader


ROMAN_NUMERALS = ['(I)', '(II)', '(III)', '(IV)', '(V)',
                  '(VI)', '(VII)', '(VIII)', '(IX)',
                  '(XI)', '(XII)', '(XVI)', '(XIV)',
                  '(XXXIII)', '(XVIII)', '(XIX)', '(XXVII)']

class MovieDataProcessor:
    def __init__(self, data):
        self.config = get_config()
        self.logger = get_logger("Clean and Process the Downloaded Movie data")
        # self.df = MovieDataLoader().get_data()
        self.df = data

    def replace_year(self, x: int) -> int:
        if x in ROMAN_NUMERALS:
            self.logger.info("Replace with the average year of the dataset")
            return 1998
        else:
            return x

    def clean_dataset(self) -> pd.DataFrame:
        self.logger.info("Drop all unnecessary columns...")
        self.df.drop(columns=['runtime', 'writer', 'path'], inplace=True)
        self.logger.info("replace roman numerals with average year")
        self.df['year'] = self.df['year'].apply(self.replace_year)
        self.logger.info("convert string representation of list to list")
        self.df['genres'] = self.df['genres'].apply(ast.literal_eval)
        self.logger.info("convert string representation of list to list")
        self.df['keywords'] = self.df['keywords'].apply(ast.literal_eval)
        self.logger.info("convert string representation of list to list")
        self.df['cast'] = self.df['cast'].apply(ast.literal_eval)
        self.logger.info("drop rows with missing overviews")
        self.df = self.df[~self.df['overview'].isnull()]
        self.logger.info("drop rows with 'none' as the overview")
        self.df = self.df[~self.df['overview'].isin(['none'])]

        self.logger.info("making sure we've filled all missing values")
        self.logger.info(self.df.isnull().sum())
        return self.df

    def get_full_text_data(self) -> pd.DataFrame:
        new_df = self.clean_dataset()
        self.logger.info("Add a column to the dataframe with all the text we want to embed")
        new_df['full_text'] = new_df["title"] + ". " + new_df["overview"] + " " + new_df['keywords'].apply(lambda x: ', '.join(x))
        self.logger.info("The dataset is too large, select the first 1000 rows from the dataset")
        first_200_df = new_df.head(1000)
        return first_200_df
