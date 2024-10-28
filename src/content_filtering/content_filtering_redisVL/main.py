from content_filtering_redisVL import flush_redis_database
from content_filtering_redisVL.data.data_preparation import MovieDataLoader
from content_filtering_redisVL.data.data_processing import MovieDataProcessor
from content_filtering_redisVL.models.vector_embedding import TextEmbedding
from content_filtering_redisVL.models.load_embedding import LoadEmbedding
from content_filtering_redisVL.pipeline.load_data_redisvl import MovieSearchIndex
from content_filtering_redisVL.pipeline.recommend_pipeline import MovieRecommender
from content_filtering_redisVL.utils.logger import get_logger
from redis.exceptions import RedisError


def main() -> None:
    logger = get_logger("Movie Recommender Pipeline")

    try:
        logger.info("Flushing the Redis database...")
        flush_redis_database.flush_redis_database()

        logger.info("Downloading the movies data...")
        data = MovieDataLoader().get_data()

        logger.info("Cleaning and processing the data...")
        df = MovieDataProcessor(data).get_full_text_data()

        logger.info("Generating text embeddings for the full-text column...")
        TextEmbedding(df).text_vectorizer()

        logger.info("Loading the embedding vectors and applying them to the dataset...")
        embedded_data = LoadEmbedding(df).load_embedding_pickle()

        # Initialize search index and recommender
        recommender_index = MovieSearchIndex(embedded_data)

        logger.info("Creating and initializing the search index schema...")
        index = recommender_index.create_index_schema()

        logger.info("Loading data to Redis...")
        recommender_index.load_data_to_redis()

        logger.info("Instantiating the recommender system...")
        recommend_movie = MovieRecommender(embedded_data, index)

        logger.info("Generating recommendations based on the specified filters...")
        recommend_movie.recommend_movies(
            title='The Story of the Kelly Gang',
            genres=['Crime'],
            release_year=1906,
            keywords=['exploration', 'gang', 'authorities'],
            distance=0.6
        )

        logger.info("Cleaning up resources...")
        recommend_movie.clean_up()

    except RedisError as e:
        logger.error(f"Redis error occurred: {e}")
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        logger.info("Pipeline execution completed.")


if __name__ == "__main__":
    main()