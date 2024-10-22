import redis
from redis import Redis
from content_filtering_redisVL.utils.logger import get_logger
from content_filtering_redisVL.utils.config import get_config
from content_filtering_redisVL.utils.connect_redis import RedisClient
from content_filtering_redisVL.data.data_processing import MovieDataProcessor

from redisvl.schema import IndexSchema
from redisvl.index import SearchIndex


class MovieSearchIndex:
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger("")
        # self.vector_dimension = VectorEmbedding().vector_dimension()
        self.client = RedisClient().connect()
        self.df = MovieDataProcessor().get_full_text_data()


    def create_index_schema(self):
        try:
            movie_schema = IndexSchema.from_yaml("content_filtering_schema.yaml")
            index = SearchIndex(movie_schema, redis_client=self.client)
            index.create(overwrite=True, drop=True)
            data = self.df.to_dict(orient='records')
            keys = index.load(data)
            return keys
        except Exception as e:
            self.logger.info(f"Index already exists: {e}")















