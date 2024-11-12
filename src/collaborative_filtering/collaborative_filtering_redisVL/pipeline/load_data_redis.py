from redis import Redis
from redisvl.schema import IndexSchema
from redisvl.index import SearchIndex


from collaborative_filtering_redisVL.utils.connect_redis import RedisClient
client = RedisClient().connect()
# client = Redis.from_url(REDIS_URL)

from collaborative_filtering_redisVL.data.datasets import vector_data
movies_df = vector_data().merged_movie_vector_series()

from collaborative_filtering_redisVL.data.datasets import movies_dataset
ratings_df = movies_dataset().ratings_columns_df()


movie_schema = IndexSchema.from_dict({
    'index': {
        'name': 'movies',
        'prefix': 'movie',
        'storage_type': 'json'
    },
    'fields': [
        {'name': 'movieId','type': 'tag'},
        {'name': 'genres', 'type': 'tag'},
        {'name': 'original_language', 'type': 'tag'},
        {'name': 'overview', 'type': 'text'},
        {'name': 'popularity', 'type': 'numeric'},
        {'name': 'release_date', 'type': 'numeric'},
        {'name': 'revenue', 'type': 'numeric'},
        {'name': 'runtime', 'type': 'numeric'},
        {'name': 'status', 'type': 'tag'},
        {'name': 'tagline', 'type': 'text'},
        {'name': 'title', 'type': 'text'},
        {'name': 'vote_average', 'type': 'numeric'},
        {'name': 'vote_count', 'type': 'numeric'},
        {
            'name': 'movie_vector',
            'type': 'vector',
            'attrs': {
                'dims': 100,
                'algorithm': 'flat',
                'datatype': 'float32',
                'distance_metric': 'ip'
            }
        }
    ]
})



movie_index = SearchIndex(movie_schema, redis_client=client)
movie_index.create(overwrite=True, drop=True)

movie_keys = movie_index.load(movies_df.to_dict(orient='records'))


def sanity_check_merged_dataframes():
    # sanity check we merged all dataframes properly and have the right sizes of movies, users, vectors, ids, etc.
    number_of_movies = len(movies_df.to_dict(orient='records'))
    size_of_movie_df = movies_df.shape[0]

    print('number of movies', number_of_movies)
    print('size of movie df', size_of_movie_df)

    unique_movie_ids = movies_df['id'].nunique()
    print('unique movie ids', unique_movie_ids)

    unique_movie_titles = movies_df['title'].nunique()
    print('unique movie titles', unique_movie_titles)

    unique_movies_rated = ratings_df['movieId'].nunique()
    print('unique movies rated', unique_movies_rated)
    movies_df.head()





from collaborative_filtering_redisVL.utils.logger import get_logger
from collaborative_filtering_redisVL.utils.config import get_config
from collaborative_filtering_redisVL.utils.connect_redis import RedisClient
import pandas as pd

class MovieSearchIndex:
    def __init__(self, data: pd.DataFrame):
        self.config = get_config()
        self.logger = get_logger("")
        self.client = RedisClient().connect()
        self.movies_df = movies_df
        self.movie_index = None

    def create_index_schema(self):
        try:
            self.logger.info("Loading the YAML index schema.")
            movie_schema = IndexSchema.from_yaml("collaborative_filtering_schema.yml")

            self.logger.info("Creating search index...")
            self.movie_index = SearchIndex(movie_schema, redis_client=self.client)
            self.movie_index.create(overwrite=True, drop=True)
            self.logger.info("Index schema created successfully")
            return self.movie_index

        except Exception as e:
            self.logger.error(f"Failed to create index schema: {e}")
            return None


    def load_data_to_redis(self):
        self.logger.info("Load the dataset records into the Redis index.")
        try:
            if not self.movie_index:
                self.logger.error("Index is not initialized. Please call `create_index_schema()` first.")
                return
            data = self.movies_df.to_dict(orient='records')
            self.logger.info(f"Loading {len(data)} records into the index in Redis.")
            keys = self.movie_index.load(data)
            self.logger.info(f"Data loaded with {len(keys)} keys.")
            return keys
        except Exception as e:
            self.logger.error(f"Error loading data into Redis: {e}")






