import os
import pickle
from content_filtering_redisVL.utils.logger import get_logger
from content_filtering_redisVL.utils.config import get_config
# from content_filtering_redisVL.data.data_processing import MovieDataProcessor
from redisvl.utils.vectorize import HFTextVectorizer


class TextEmbedding:
    def __init__(self, data):
        self.config = get_config()
        self.logger = get_logger("Using RedisVL embedding generators to generate semantic vector embeddings of the dataset descriptions")
        # self.data = MovieDataProcessor().get_full_text_data()
        self.data = data

    def text_vectorizer(self) -> pickle:
        try:
            self.logger.info("Initialize the RedisVL vectorizer")
            vectorizer = HFTextVectorizer(model=self.config.PRETRAINED_REDISVL_MODEL)

            self.logger.info("Apply embedding to the 'full_text' column")
            self.data['embedding'] = self.data['full_text'].apply(lambda x: vectorizer.embed(x, as_buffer=False))

            self.logger.info("Create 'text_embedding_file' folder if it doesn't exist")
            os.makedirs('text_embedding_file', exist_ok=True)

            self.logger.info("Save the applied embeddings file as a pickle file")
            with open(os.path.join('text_embedding_file', 'text_embeddings.pkl'), 'wb') as f:
                pickle.dump(self.data['embedding'], f)

        except ValueError as e:
            self.logger.info(f"There was an error setting the embedding model dimensions: {e}")

