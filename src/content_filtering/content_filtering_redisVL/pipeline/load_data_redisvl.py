from redisvl.schema import IndexSchema
from redisvl.index import SearchIndex
from content_filtering_redisVL.utils.logger import get_logger
from content_filtering_redisVL.utils.config import get_config
from content_filtering_redisVL.utils.connect_redis import RedisClient
import pandas as pd


class MovieSearchIndex:
    def __init__(self, data: pd.DataFrame):
        self.config = get_config()
        self.logger = get_logger("Define the search index schema that specifies each of our data fields and the size and type of the embedding vectors")
        self.client = RedisClient().connect()
        self.data = data
        self.index = None

    def create_index_schema(self):
        try:
            self.logger.info("Loading the YAML index schema.")
            movie_schema = IndexSchema.from_yaml("content_filtering_schema.yaml")

            self.logger.info("Creating search index...")
            self.index = SearchIndex(movie_schema, redis_client=self.client)
            self.index.create(overwrite=True, drop=True)
            self.logger.info("Index schema created successfully")
            return self.index

        except Exception as e:
            self.logger.error(f"Failed to create index schema: {e}")
            return None

    def load_data_to_redis(self):
        self.logger.info("Load the dataset records into the Redis index.")
        try:
            if not self.index:
                self.logger.error("Index is not initialized. Please call `create_index_schema()` first.")
                return
            data = self.data.to_dict(orient='records')
            self.logger.info(f"Loading {len(data)} records into the index in Redis.")
            keys = self.index.load(data)
            self.logger.info(f"Data loaded with {len(keys)} keys.")
            return keys
        except Exception as e:
            self.logger.error(f"Error loading data into Redis: {e}")


    # def get_sample_recommendation(self):
    #     from redisvl.query import RangeQuery
    #     if not self.index:
    #         self.logger.error("Index is not initialized. Please call `create_index_schema()` first.")
    #         return None
    #     self.logger.info("Fetching recommendation results")
    #     query_vector = self.data[self.data['title'] == 'The Story of the Kelly Gang']['embedding'].values[
    #         0]  # one good match
    #
    #     query = RangeQuery(vector=query_vector,
    #                        vector_field_name='embedding',
    #                        num_results=5,
    #                        distance_threshold=0.7,
    #                        return_fields=['title', 'overview', 'vector_distance'])
    #
    #     results = self.index.query(query)
    #     for r in results:
    #         print(r)















