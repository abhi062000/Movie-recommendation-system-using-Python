import pickle
import streamlit as st
import requests


def fetch_poster(movie_id):
# The `fetch_poster` function is responsible for fetching the poster image of a movie using the
# movie ID. It makes a request to the TMDB API to get the movie details, including the poster
# path. It then constructs the full URL of the poster image using the poster path and returns the
# URL.
    url = "https://api.themoviedb.org/3/movie/{}?api_key=ee1b3e8ee0aa026ff0110e0f0b679831&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
# The `recommend` function takes a movie as input and returns a list of recommended movie names
# and their corresponding poster images. It first finds the index of the input movie in the
# `movies` dataframe. Then, it calculates the similarity scores between the input movie and all
# other movies using the `similarity` matrix. The movies are sorted based on their similarity
# scores in descending order. The function then fetches the movie poster for the top 5 similar
# movies using the `fetch_poster` function and appends the movie names and poster URLs to separate
# lists. Finally, it returns the recommended movie names and poster URLs.
    with st.spinner('Fetching recommendations...'):
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            # fetch the movie poster
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)

        return recommended_movie_names, recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
