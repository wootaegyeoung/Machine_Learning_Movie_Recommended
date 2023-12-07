import pandas as pd
import numpy as np

# Loading the data
ratings_movielens = pd.read_csv('data/ratings.csv')
item_frame = pd.read_csv('data/u.item', sep='|', header=None, encoding='latin-1', ...)

# Calculating the number of users and items
n_users = ratings_movielens['userId'].unique().shape[0]
n_items = ratings_movielens['movieId'].unique().shape[0]

# Setting the user ID and item ID to their maximum values
n_users = ratings_movielens['userId'].max()
n_items = ratings_movielens['movieId'].max()

# Initializing lists for Mean Squared Error (MSE)
test_mse_lst = []
train_mse_lst = []

# Setting hyperparameters
K = 20
steps = 100
alpha = 0.001
beta = 0.02

# Initializing user and item latent feature matrices
P = np.random.normal(scale=1. / K, size=(n_users + 1, K))
Q = np.random.normal(scale=1. / K, size=(n_items + 1, K))

# Initializing biases
b_u = np.zeros(n_users + 1)
b_i = np.zeros(n_items + 1)
b = np.mean(ratings_movielens['rating'])

# Creating training data samples
samples = [
    (ratings_movielens.iloc[i, 0], ratings_movielens.iloc[i, 1], ratings_movielens.iloc[i, 2])
    for i in range(ratings_movielens.shape[0])
]

# Training using Stochastic Gradient Descent (SGD)
total_mae = 0
total_num = 0
for step in range(steps):
    np.random.shuffle(samples)
    for i, j, r in samples:
        # Calculating prediction and error
        prediction = b + b_u[i] + b_i[j] + P[i, :].dot(Q[j, :].T)
        e = (r - prediction)
        total_mae += abs(e)
        total_num += 1
        # Updating biases and feature matrices
        b_u[i] += alpha * (e - beta * b_u[i])
        b_i[j] += alpha * (e - beta * b_i[j])
        P[i, :] += alpha * (e * Q[j, :] - beta * P[i, :])
        Q[j, :] += alpha * (e * P[i, :] - beta * Q[j, :])

# Loading test data
test_data = pd.read_csv('data/ua.test', sep='\t', header=None, ...)

# Calculating MSE for the test data
mse = 0
for i, j, r in test_data.itertuples(index=False):
    try:
        prediction = b + b_u[i] + b_i[j] + P[i, :].dot(Q[j, :].T)
        mse += (r - prediction) ** 2
    except IndexError as e:
        print(f"IndexError: {e}. Skipping...")
mse /= len(test_data)

# Calculating movie recommendation scores for each user
movie_score = []
item_name = pd.read_csv('data/u.item', sep='|', header=None, encoding='latin-1', ...)
for _, j, r in test_data.itertuples(index=False):
    prediction_score = b + b_u[user_id] + b_i[j] + P[user_id, :].dot(Q[j, :].T)
    movie_name = item_name.iloc[j, 1]
    movie_score.append((movie_name, f'{prediction_score:.3f}'))

# Sorting and displaying the top 5 recommended movies
unique_samples = list(set(movie_score))
unique_samples.sort(key=lambda x: x[1], reverse=True)
print(unique_samples[:5])

# Outputting the average Mean Absolute Error (MAE)
print("mae's average: ", total_mae / total_num)
