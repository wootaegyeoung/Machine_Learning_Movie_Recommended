import pandas as pd
import numpy as np
from scipy import spatial
import operator
import ast
from typing import List
import pandas as pd
import boto3

# Create S3 client
s3_client = boto3.client("s3")

bucket_name = "sg01003movies"
s3_key = "movies_features.csv"

csv_file_path = "movies_features.csv"
s3_client.download_file(bucket_name, s3_key, csv_file_path)

movies = pd.read_csv(csv_file_path)

movies['genres_bin'] = movies['genres_bin'].apply(lambda x: np.array(ast.literal_eval(x)))
movies['cast_bin'] = movies['cast_bin'].apply(lambda x: np.array(ast.literal_eval(x)))
movies['director_bin'] = movies['director_bin'].apply(lambda x: np.array(ast.literal_eval(x)))



def Similarity(movieId1, movieId2):
    a = movies.iloc[movieId1]
    b = movies.iloc[movieId2]
    
    genresA = a['genres_bin']
    genresB = b['genres_bin']
    
    genreDistance = spatial.distance.cosine(genresA, genresB)
    
    scoreA = a['cast_bin']
    scoreB = b['cast_bin']
    scoreDistance = spatial.distance.cosine(scoreA, scoreB)
    
    directA = a['director_bin']
    directB = b['director_bin']
    directDistance = spatial.distance.cosine(directA, directB)
    
    wordsA = a['words_bin']
    wordsB = b['words_bin']
    wordsDistance = spatial.distance.cosine(directA, directB)
    return genreDistance + directDistance + scoreDistance + wordsDistance


# Score Predictor

total_neighbors: List = []
def KNN_predict_score(name):
    # name = input('Enter a movie title: ')
    new_movie = movies[movies['original_title'].str.contains(name)].iloc[0].to_frame().T
    def getNeighbors(baseMovie, K):
        distances = []
    
        for index, movie in movies.iterrows():
            # Skip similarity check for the same movie.
            if movie['new_id'] != baseMovie['new_id'].values[0]:
                dist = Similarity(baseMovie['new_id'].values[0], movie['new_id'])
                distances.append((movie['new_id'], dist))
    
            distances.sort(key=operator.itemgetter(1))
        neighbors = []
        # Extract top 10 data
        for x in range(K):
            neighbors.append(distances[x])
        return neighbors

    K = 10
    avgRating = 0
    neighbors = getNeighbors(new_movie, K)
    sigm = 0
    mae = 0
    print('Movies Recommended based on K-Nearest Neighbors Content-based filtering:')
    for neighbor in neighbors:
        avgRating = avgRating + movies.iloc[neighbor[0]][2]
        mae += abs(float(new_movie['vote_average']) - float(movies.iloc[neighbor[0]][2]))
        sigm += pow(float(new_movie['vote_average']) - float(movies.iloc[neighbor[0]][2]), 2)

    
    total_neighbors.extend(neighbors)
    total_neighbors.sort(key=operator.itemgetter(1))
    avgRating = avgRating / K
    sigm = (sigm / K) ** (0.5)
    mae = mae / K





def get_recommendations(input_movies):
    knncontent_output = []
    for movie in input_movies:
        KNN_predict_score(movie)
    
    recommendations = total_neighbors
    print('Movies Recommended based on K-Nearest Neighbors Content-based filtering:')
    for rec in recommendations:
        if len(knncontent_output) >= 10:
            break
        rec_movie = movies[movies['new_id'] == rec[0]]
        if not (rec_movie['original_title'].values[0] in knncontent_output):
            knncontent_output.append(rec_movie['original_title'].values[0])
    return knncontent_output