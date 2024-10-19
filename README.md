# small-scale-recommendations-systems

A recommendation system is an artificial intelligence or AI algorithm, usually associated with machine learning, 
that uses Big Data to suggest or recommend additional products to consumers. These can be based on various criteria, 
including past purchases, search history, demographic information, and other factors. 
Recommender systems are highly useful as they help users discover products and services they might otherwise have not found on their own.

Recommender systems are trained to understand the preferences, previous decisions, and characteristics of people and products using data gathered about their interactions. 
These include impressions, clicks, likes, and purchases. Because of their capability to predict consumer
interests and desires on a highly personalized level, recommender systems are a favorite with content and product providers. 
They can drive consumers to just about any product or service that interests them, from books to videos to health classes to clothing.


<div style="text-align: center;">
    <img src="assets/Untitled-2024-09-14-1236.png" alt="recommendation system" style="height: 600px; width: 500px;"/>
</div>


### Types of Recommendation Systems
There are quite a vast number of recommender algorithms and techniques, most fall into these broad categories;
- collaborative filtering,
- content filtering, and
- context filtering

1. **Collaborative Filtering**: CF algorithms recommend items (filtering part) based on preference information from many users (collaborative part).
This approach uses similarity of user preference behaviour, given previous interactions between users and items, recommender algorithms learn to predict future 
interaction. These recommender systems build a model from a user's past behavior, such as items purchased previously or ratings given to those items and similar
decisions by other users. The idea is that if some people have made similar decisions and purchases in the past, like a movie choice, then there is a high 
probability they will agree on additional future selections. For example, if a collaborative filtering recommender knows you and another user share similar tastes in movies,
it might recommend a movie to you that it knows this other user already likes.


<div style="text-align: center;">
    <img src="assets/collaborative-filtering.png" alt="collaborative-filtering logo" style="height: 750px; width: 550px;"/>
</div>

- Advantages
  - Can work well even with sparse data
  - Doesn't require feature engineering
  - Can capture complex patterns in user behavior.

- Disadvantages
  - Cold start problem (Difficulty in making recommendations for new users or items)
  - Scalability issues with large datasets
  - Need for significant amount of historical data.


2. **Content Filtering**: This, by contrast, uses the attributes or features of an item (content part) to recommend other items similar
to the user's preferences. This approach is based on similarity of item and user features, given information about a user and items they
have interacted with (e.g. a user’s age, the category of a restaurant’s cuisine, the average review for a movie), model the likelihood of 
a new interaction. For example, if a content filtering recommender sees you liked the movies `You've Got Mail` and `Sleepless in Seatle`,
it might recommend another movie to you with the same genres and/or cast.

   
<div style="text-align: center;">
    <img src="assets/content-based-filtering.png" alt="content-based-filtering logo" style="height: 750px; width: 550px;"/>
</div>


- Advantages
  - Doesn't suffer from the cold start problem for new items
  - Can provide explanations for recommendations
  - Can recommend niche or less popular items

- Disadvantages
  - Limited by the quality of item features
  - Can result in a "filter bubble" where users are only recommended similar items,
  - Struggles with recommending items outside a user's known preferences.


3. **Context Filtering Hybrid Recommender Systems**: This combines multiple recommendation algorithms (e.g., collaborative filtering and 
content-based filtering) to leverage their strengths and mitigate weaknesses. Content filtering includes users' contextual information in the recommendation process. 
`Nexflix` makes better recommendations by framing a recommendation as a contextual sequence prediction. This approach uses a sequence of contextual user actions, plus the 
current context, to predict the probability of the next action. Given one sequence for each user, the country, device, date, and time when
they watched a movies-`Nexflix` trained a model to predict what to watch next.

- Advantages
  - Can provide more accurate and diverse recommendations by leveraging different recommendation techniques

- Disadvantages
  - Increased complexity in implementation and potential challenges in tuning and integrating multiple algorithms.

    
### Use Cases and Applications
1. E-Commerce and Retail: Personalized Merchandising
2. Media and Entertainment: Personalized Content
3. Personalized Banking


### How Recommenders Work
Recommender model makes recommendations based on the type of data you have. If you only have data about which interactions have occurred 
in the past, you'll probably be interested in collaborative filtering. If you have data describing the user and items they have interacted with
(i.e. a user's age, the category of a restaurant's cuisine, the average review for a movie), you can model the likelihood of a new
interaction given these properties at the current moment by adding content and context filtering.


## Matrix Factorization for Recommendation
Matrix factorization (MF) techniques are the core of many popular algorithms, including word embedding and topic embedding, and have become a dominant methodology
with collaborative-filtering-based recommendation. MF can be used to calculate the similarity in user's ratings or interactions to provide recommendations.
In the simple user item matrix below, `Yinka` and `Musa` like movies `B` and `C`. `Jidenna` likes movie `B`. To recommend a movie to `Jidenna`, matrix factorization
calculates that users who liked `B` also liked `C`, so `C` is a possible recommendation for `Jidenna`


<div style="text-align: center;">
    <img src="assets/matrix-factorization.png" alt="matrix-factorization image" style="height: 350px; width: 300px;"/>
</div>




































































