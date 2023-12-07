import pandas as pd
import random
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split

# Extracting unique user IDs
unique_user_ids = rating['userId'].unique()

# Splitting user IDs into training and test datasets
train_userIds, test_userIds = train_test_split(unique_user_ids, test_size=0.02, random_state=42)

# Creating empty dataframes for training and testing
train_rating = pd.DataFrame(columns=rating.columns)
test_rating = pd.DataFrame(columns=rating.columns)

# Constructing the training dataset
for userId in train_userIds:
    train_rating = pd.concat([train_rating, rating[rating['userId'] == userId]], ignore_index=True)

# Constructing the test dataset
for userId in test_userIds:
    test_rating = pd.concat([test_rating, rating[rating['userId'] == userId]], ignore_index=True)

# Defining the recommendation function
def get_recommendations(input_movies):
    knncontent_output = []
    total_mae = 0
    total_num = 0

    # Predicting ratings and calculating MAE for each movie
    for movie in input_movies:
        total_mae += KNN_predict_score(movie)
        total_num = total_num + 1

    # Selecting recommended movies using KNN algorithm
    recommendations = total_neighbors
    for rec in recommendations:
        if len(knncontent_output) >= 10:
            break
        rec_movie = movies[movies['new_id'] == rec[0]]
        if not (rec_movie['original_title'].values[0] in knncontent_output):
            knncontent_output.append(rec_movie['original_title'].values[0])
    return total_mae / total_num

# Calculating average MAE for test users
total_mae = 0
for i in test_userIds:
    inputUserID = i
    inputUser = test_rating[test_rating['userId'] == inputUserID]

    # Converting user review data to datetime
    inputUser['date'] = pd.to_datetime(inputUser['timestamp'], unit='s')
    latest_date = inputUser['date'].max()
    two_years_ago = latest_date - timedelta(days=1 * 365)  # Filtering reviews from the past year

    # Filtering movies with ratings from the past year and above 3
    inputUser = inputUser[inputUser['date'] >= two_years_ago]
    inputUser = inputUser[inputUser['rating'] >= 3]

    # Merging with movie data
    inputUserData = pd.merge(inputUser, movies_movielens)
    input_movies = inputUserData['title'].unique()

    # Calling the recommendation function and updating average MAE
    total_mae += get_recommendations(input_movies)

# Outputting final average MAE
print("mae's average: ", total_mae / len(test_userIds))
