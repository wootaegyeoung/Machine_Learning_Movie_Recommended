import json
import pandas as pd
import requests
import streamlit as st
import poster

# Set the style for the Streamlit app
st.markdown(
    """
    <style>
    .fontsize {
        font-size: 3rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Select the page from the sidebar
page = st.sidebar.selectbox("MENU", ["info", "recommendation"])

# Check if 'input_data' exists in the session state, and initialize it if not
if 'input_data' not in st.session_state:
    st.session_state.input_data = []

# Searches the text entered by the user in the 'movies.csv' file
# returns the search results.
def search(txt):
    try:
        # Load movie data from 'movies.csv'
        df = pd.read_csv("movies.csv")
    except FileNotFoundError:
        st.error("File doesn't exist.")

    # Get the list of movie titles
    movies = df["title"].tolist()
    # Filter movies based on user input
    filtered_movies = list(filter(lambda movie: txt.lower() in movie.lower(), movies))
    return filtered_movies

# The 'info' page: A page where users enter the movies they have seen and their ratings
#
# 1. Search for movie name
# 2. Output filtered movie list using radio button
# 3. User enters rating
# 4. Save the input movie and star rating data as a tuple - input_data
if page == "info":
    st.title("🎬Moving")
    st.markdown("""
    ```
    Hi, welcome to > Moving!

    Tell me what movies you like or dislike, and I'll recommend movies to you.
    Below you can search for the movie you watched and enter a rating for it.

    Get started!
    ```

    """)

    st.write('*' * 50)

    st.header("❓Survey")
    col1, col2 = st.columns([1, 1])

    with col1:
        # User enters the movie name
        txt = st.text_input("Search for movie title", "")
        # Search for movies based on user input
        filtered_movies = search(txt)

        if txt:
            # Output search results as radio buttons
            movie_name = st.radio("Select the movie", filtered_movies)

    with col2:
        if txt:
            # Get the poster URL for the selected movie
            selected_movie = poster.get_movie_poster_url(movie_name)

            col11, col22, col33 = st.columns([1, 3, 1])   # Split screen for center alignment
            with col11:
                st.write(' ')
            with col22:
                # Display the movie poster in the center
                st.image(selected_movie, use_column_width=True)

            with col33:
                st.write(' ')

            # Save star ratings for the selected movie
            from streamlit_star_rating import st_star_rating
            user_rating = st_star_rating(f"Your Rating of {movie_name}", 5, 1, key="rating",
                                         customCSS="div {background-color: #eeeeee; color: black; font-size : xx-small; text-align: center; font-family: arial;}")
            col11, col22, col33 = st.columns(3)  # Split screen for center alignment
            with col11:
                st.write(' ')
            with col22:
                if st.button("Store"):
                    if movie_name and user_rating is not None:
                        # Save the movie name and user rating as a tuple
                        movie_rating_tuple = (movie_name, user_rating)
                        st.session_state.input_data.append(movie_rating_tuple)
            with col33:
                st.write(' ')

    # Display the list of movies and their ratings
    if st.session_state.input_data is not None:
        st.write('*' * 50)
        st.header("🎞️Your Movies")
        col1, col2 = st.columns(2)

        for i, movie_rating in enumerate(st.session_state.input_data):
            movie_poster = poster.get_movie_poster_url(movie_rating[0])

            if i % 2 == 0:
                with col1:
                    # Display the movie poster and rating in the first column
                    st.image(movie_poster)
                    st_star_rating(label=movie_rating[0], maxValue=5, defaultValue=movie_rating[1],
                                   read_only=True, customCSS="div {size : xx-small}")
            else:
                with col2:
                    # Display the movie poster and rating in the second column
                    st.image(movie_poster)
                    st_star_rating(label=movie_rating[0], maxValue=5, defaultValue=movie_rating[1],
                                   read_only=True)

# 'recommendation' page
# Print posters of recommended movies
# 1. Use content filtering techniques based on the user’s favorite movies
# 2. Use MF to recommend movies you might like
elif page == "recommendation":
    st.title("🍿How about these movies?")

    # Store movie list
    movie_list = {"data": [item[0] for item in st.session_state.input_data if item[1] >= 3]}

    # Fast API - content filtering
    url = "http://3.26.76.121:8000/content"
    response = requests.post(url, json=movie_list)
    data = response.json()
    movie_names = [movie.split('(')[0].strip() for movie in data]

    result = ','.join(movie_list['data'])
    st.header(f"🎬Movies similar to {result}")

    # Print posters of recommended movies
    col1, col2, col3 = st.columns(3)
    for i, movie in enumerate(movie_names):
        poster2 = poster.get_movie_poster_url(movie)
        if i % 3 == 0:
            col1.image(poster2, caption=movie, use_column_width=True)
        elif i % 3 == 1:
            col2.image(poster2, caption=movie, use_column_width=True)
        else:
            col3.image(poster2, caption=movie, use_column_width=True)

    st.header("🎬Movies you might like")
    col1, col2, col3 = st.columns([1, 1, 1])

    # Fast API - Matrix Factorization
    user_id = 10    # Random user ID
    url2 = f"http://3.26.76.121:8000/user/{user_id}"
    response2 = requests.get(url2)
    data2 = response2.json()
    movie_names2 = [movie.split('(')[0].strip() for movie in data2]

    # Print posters of recommended movies
    for i, movie in enumerate(movie_names2):
        poster2 = poster.get_movie_poster_url(movie)
        if i % 3 == 0:
            col1.image(poster2, caption=movie, use_column_width=True)
        elif i % 3 == 1:
            col2.image(poster2, caption=movie, use_column_width=True)
        else:
            col3.image(poster2, caption=movie, use_column_width=True)
