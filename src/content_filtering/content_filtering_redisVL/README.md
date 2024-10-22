Recommendation systems are a common application of machine learning and serve many industries from e-commerce to music streaming platforms.

There are many different architechtures that can be followed to build a recommender system.

In this notebook we'll demonstrate how to build a content filtering recommender and use the movies dataset as our example data.

Content Filtering recommender systems are built on the premise that a person will want to be recommended things that are similar to things they already like.

In the case of movies, if a person watches and enjoys a nature documentary we should recommend other nature documentaries. Or if they like classic black & white horror films we should recommend more of those.

The question we need to answer is, 'what does it mean for movies to be similar?'. There are exact matching strategies, like using a movie's labelled genre like 'Horror', or 'Sci Fi', but that can lock people in to only a few genres. Or what if it's not the genre that a person likes, but certain story arcs that are common among many genres?

For our content filtering recommender we'll measure similarity between movies as semantic similarity of their descriptions and keywords.