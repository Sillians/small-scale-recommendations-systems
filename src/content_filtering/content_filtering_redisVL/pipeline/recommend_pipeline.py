import pandas as pd
from content_filtering_redisVL.utils.logger import get_logger
from content_filtering_redisVL.utils.config import get_config
from content_filtering_redisVL.utils.connect_redis import RedisClient
from redisvl.query import RangeQuery
from redisvl.query.filter import Tag, Num, Text


class MovieRecommender:
    def __init__(self, data: pd.DataFrame, index):
        self.config = get_config()
        self.logger = get_logger("Generate user recommendation")
        self.client = RedisClient().connect()
        self.df = data
        self.index = index

    def make_filter(self, genres:list=None, release_year:int=None, keywords:list=None):
        """Create a flexible filter for search queries based on genres, release year, and keywords."""
        self.logger.info(f"Creating filter with genres={genres}, release_year={release_year}, keywords={keywords}")
        filters = []

        self.logger.info("Only add filter components if their respective parameters are provided")
        if genres:
            filters.append(Tag("genres") == genres)
        if release_year:
            filters.append(Num("year") > release_year)
        if keywords:
            self.logger.info("Join keywords into a single string")
            filters.append(Text("full_text") % ' '.join(keywords))

        self.logger.info("Combine all filters with '&' if they exist; otherwise return None")
        flexible_filter = filters[0] if filters else None
        for f in filters[1:]:
            flexible_filter &= f

        return flexible_filter

    def get_recommendations(self, movie_vector, num_results:int=5, distance:float=0.6, filter=None):
        """Get movie recommendations based on the vector embedding, distance, and filter."""
        if not self.index:
            self.logger.error("Index is not initialized.")
            return None

        self.logger.info(f"Fetching {num_results} recommendations with distance threshold={distance}.")
        query = RangeQuery(
            vector=movie_vector,
            vector_field_name='embedding',
            num_results=num_results,
            distance_threshold=distance,
            return_fields=['title', 'overview', 'genres'],
            filter_expression=filter
        )

        try:
            recommendations = self.index.query(query)
            return recommendations
        except Exception as e:
            self.logger.error(f"Failed to execute query: {e}")
            return None

    def recommend_movies(self, title:str, genres:list=None,
                         release_year:int=None, keywords:list=None,
                         num_results:int=5, distance:float=0.6):
        """Recommend movies based on a given title, optional filters, and search parameters."""
        try:
            self.logger.info(f"Looking up movie vector for title: {title}")
            movie_vector = self.df[self.df['title'] == title]['embedding'].values[0]

            self.logger.info("Create the filter based on user preferences")
            filter = self.make_filter(genres=genres, release_year=release_year, keywords=keywords)

            self.logger.info("Get recommendations")
            recs = self.get_recommendations(movie_vector, num_results=num_results, distance=distance, filter=filter)

            self.logger.info("Print recommendations")
            for rec in recs:
                print(f"- {rec['title']}:\n\t{rec['overview']}\n\tGenres: {rec['genres']}")
        except IndexError:
            self.logger.error(f"Movie '{title}' not found in the dataset.")
        except Exception as e:
            self.logger.error(f"An error occurred during recommendations: {e}")


    def clean_up(self):
        self.logger.info("clean up the index")
        while remaining := self.index.clear():
            print(f"Deleted {remaining} keys")

