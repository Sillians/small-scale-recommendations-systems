## Recommendation Systems using RedisVl

Recommendation systems are a common application of machine learning and serve many industries from e-commerce to music streaming platforms.
There are many different architechtures that can be followed to build a recommender system.

This project demonstrates how to build a content filtering recommender from scratch using `redisvl` and an `IMDB` movies dataset.


### Content Filtering

Content Filtering recommender systems are built on the premise that a person will want to be recommended things that are similar to things they already like.

In the case of movies, if a person watches and enjoys a nature documentary we should recommend other nature documentaries. 
Or if they like classic black & white horror films we should recommend more of those.

The question we need to answer is, 'what does it mean for movies to be similar?'. There are exact matching strategies, 
like using a movie's labelled genre like 'Horror', or 'Sci-Fi', but that can lock people in to only a few genres. 
Or what if it's not the genre that a person likes, but certain story arcs that are common among many genres?

In this project, we'll measure similarity between movies as semantic similarity of their descriptions and keywords. 


### Environment Setup
Install Python Dependencies
- `pip install -r requirements.txt`


### Generating Vector Embeddings

To carry out the semantic similarity of movie descriptions, we need a way to generate semantic vector embeddings of these descriptions. 
RedisVL supports quite a few different embedding generators. For this example, we'll use a `HFTextVectorizer` model. 

The `HFTextVectorizer` class is designed to leverage the power of Hugging Face's Sentence Transformers for generating text embeddings. This vectorizer
is particularly useful in scenarios where advanced natural language processing and understanding are required. Utilizing this vectorizer involves specifying
a pre-trained model from Hugging Face's vast collection of Sentence Transformers. These models are trained on a variety of datasets and tasks, ensuring 
versatility and robust performance across different text embedding needs. 

`RedisVL` also supports complex query logic, beyond just vector similarity. To showcase this we'll generate an embedding from each movies' overview text
and list of plot keywords, and use the remaining fields like, genres, year, and rating as filterable fields to target our vector queries to.


### The Search Schema

To load the data into Redis, we need to define our search index schema that specifies each of our data fields and the size and type of our embedding vectors.
This was loaded from the accompanying `content_filtering_schema.yaml` file. This schema defines what each entry will look like within Redis. It specifies the 
name of each field, like title, rating, and rating-count, as well as the type of each field, like text or numeric. The vector component of each entry similarly
needs its dimension (dims), distance metric, algorithm and datatype (dtype) attributes specified.


### Loading the Data into the Redis Vector DB

We converted the cleaned and defined schema data into a format that `RedisVL` can understand, which is a list of dictionaries, and load the data into RedisVL.


### Generating user recommendations

To perform recommendation, users can specify if they want to see a romantic comedy or a horror film, or only see new releases. 
To demonstrate how to find movies similar to the  `crime` film `The Story of the Kelly Gang`. The process has 3 steps:

- Fetch the vector embedding of our film The Story of the Kelly Gang.
- Optionally define any hard filtering we want. Here, we specified we want `crime` movies on or after `1906`.
- Perform the vector range query to find similar movies that meet our filter criteria.













