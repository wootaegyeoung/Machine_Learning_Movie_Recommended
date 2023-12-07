import boto3
import pickle
import pandas as pd
import numpy as np
# Create S3 client
s3_client = boto3.client("s3")

bucket_name = "sg01003movies"
s3_key1 = "user/samples.pkl"
s3_key2 = "user/b.pkl"
s3_key3 = "user/b_u.pkl"
s3_key4 = "user/b_i.pkl"
s3_key5 = "user/P.pkl"
s3_key6 = "user/Q.pkl"

csv_file_path1 = "user/samples.pkl"
csv_file_path2 = "user/b.pkl"
csv_file_path3 = "user/b_u.pkl"
csv_file_path4 = "user/b_i.pkl"
csv_file_path5 = "user/P.pkl"
csv_file_path6 = "user/Q.pkl"


s3_client.download_file(bucket_name, s3_key1, csv_file_path1)
s3_client.download_file(bucket_name, s3_key1, csv_file_path2)
s3_client.download_file(bucket_name, s3_key1, csv_file_path3)
s3_client.download_file(bucket_name, s3_key1, csv_file_path4)
s3_client.download_file(bucket_name, s3_key1, csv_file_path5)
s3_client.download_file(bucket_name, s3_key1, csv_file_path6)

s3_client = boto3.client("s3")
s3_client.download_file(bucket_name, 'u.item', 'user/u.item')
item_name = pd.read_csv('user/u.item', sep='|', header=None, encoding='latin-1', names=['movie_id', 'movie_title', 'release_date', 'video_release_date', 'IMDb_URL', 'unknown', 'Action', 'Adventure', 'Animation','Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy','Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'])
    

# Read samples
with open('user/samples.pkl', 'rb') as f:
    samples = pickle.load(f)

# Read b
with open('user/b.pkl', 'rb') as f:
    b = pickle.load(f)

# Read b_u
with open('user/b_u.pkl', 'rb') as f:
    b_u = pickle.load(f)

# Read b_i
with open('user/b_i.pkl', 'rb') as f:
    b_i = pickle.load(f)

# Read P
with open('user/P.pkl', 'rb') as f:
    P = pickle.load(f)

# Read Q
with open('user/Q.pkl', 'rb') as f:
    Q = pickle.load(f)
 
b = np.array(b)
b_u = np.array(b_u)
b_i = np.array(b_i)
P = np.array(P)
Q = np.array(Q)

def get_recommendations(user_id):
    movie_score = []
    for _, j, r in samples:
        prediction_score = b + b_u[user_id] + b_i[j] + P[user_id, :].dot(Q[j, :].T)
        movie_name = item_name.iloc[j, 1]
        movie_score.append((movie_name))

    unique_samples = list(set(movie_score))
    unique_samples.sort(key=lambda x: x[1], reverse=True)
    return unique_samples[:5]