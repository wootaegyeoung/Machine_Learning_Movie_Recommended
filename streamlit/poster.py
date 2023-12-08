import requests

# The Movie Database (TMDb) API key
TMDB_API_KEY = "6e68869be73ebdaf0589b5c9fa2ea77e"


# Function to retrieve movie information from TMDb API using the movie title
def get_movie_info(movie_title):
    # TMDb API base URL for searching movies
    base_url = "https://api.themoviedb.org/3/search/movie"

    # Parameters for the API request
    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_title,
    }

    # Send a GET request to TMDb API
    response = requests.get(base_url, params=params)

    # Parse the JSON response
    data = response.json()

    # Check if there are search results
    if data["results"]:
        # Return the first search result (most relevant)
        return data["results"][0]
    else:
        return None


# Function to retrieve the movie poster URL from TMDb API using the movie title
def get_movie_poster_url(movie_title):
    # Get movie information using the provided function
    movie_info = get_movie_info(movie_title)

    # Check if movie information is available
    if movie_info:
        # Extract the poster path from the movie information
        poster_path = movie_info["poster_path"]

        # Base URL for movie poster images with width set to 200 pixels
        base_url = "https://image.tmdb.org/t/p/w200"

        # Construct the complete poster URL
        poster_url = f"{base_url}{poster_path}"

        # Return the poster URL
        return poster_url
    else:
        # Return None if movie information is not available
        return None
