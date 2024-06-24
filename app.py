import streamlit as st
import pickle
import pandas as pd
import requests

# Define function to fetch movie poster
def fetch_poster(movie_id):
    response = requests.get(
        'api-key'.format(
            movie_id))
    data = response.json()

    poster_path = data.get('poster_path')  # Get poster path from API response
    if poster_path:
        poster_url = "https://image.tmdb.org/t/p/w500" + poster_path
        return poster_url
    else:
        st.text("No poster available for movie ID: " + str(movie_id))
        return None

# Define function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch poster from API
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movies_posters.append(poster_url)
        else:
            recommended_movies_posters.append("No poster available")
    return list(zip(recommended_movies, recommended_movies_posters))

# Load movie data and similarity matrix
movies = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Set page title and background color
st.set_page_config(page_title='Movie Recommender', page_icon=':movie_camera:', layout='wide', initial_sidebar_state='collapsed')
st.markdown(
    """
    <style>
    .reportview-container {
        background: #f5f5f5;
    }
    .movie-title {
        font-size: 24px;
        font-weight: bold;
        color: grey; /* Change color to green */
        margin-bottom: 10px;
        white-space: nowrap; /* Prevent title from wrapping */
        overflow-x: auto; /* Add horizontal scrollbar */
        text-align: center; /* Center align the title */
    }
    .poster-image {
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .recommendation-column {
        padding: 0 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display title and selectbox for movie selection
st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title']
)

# Display recommendations when button is clicked
if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    # Display recommendations with styling
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]
    for i, (name, poster) in enumerate(recommendations):
        with cols[i]:
            st.markdown(f'<p class="movie-title">{name}</p>', unsafe_allow_html=True)
            st.image(poster, width=200, caption='', use_column_width='auto', output_format='JPEG', channels='RGB', clamp=False)
