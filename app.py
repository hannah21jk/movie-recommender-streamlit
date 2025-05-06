import streamlit as st
import pickle
import pandas as pd
import requests

# --- TMDB API Setup ---
API_KEY = "a714d1b9029f92f0542af8045795ec90"  

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return ""

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]]['movie_id']  # تأكد أن عندك هذا العمود في movie_dict.pkl
        recommended_movies.append(movies.iloc[i[0]]['title'])
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# --- Load Data ---
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)  

similarity = pickle.load(open('similarity.pkl','rb'))

# --- UI ---
st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    'Choose a movie you like:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
