import streamlit as st
import pickle
import requests

# Load the data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def poster(movie_id):
    re = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f1cf0bcfa241dc5637cc06864adbcfb3&language=en-US")
    j_data = re.json()
    poster_path = j_data.get("poster_path", "")
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"  # Placeholder image if no poster available


# Define the recommendation function
def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = similarity[index]
    sorted_distances = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = [movies["id"][i[0]] for i in sorted_distances]
    return recommended_movies


# Streamlit app
st.title("MOVIE RECOMMENDER")

# Dropdown menu for movie selection
option = st.selectbox("Select a movie", movies["title"])

# Recommendation button
if st.button("Recommend"):
    recommendations = recommend(option)
    st.write("Recommended movies:")
    movie_titl = []
    poster_li = []

    for rec_movie in recommendations:
        movie_title = movies[movies["id"] == rec_movie]["title"].values[0]
        movie_titl.append(movie_title)
        poster_li.append(poster(rec_movie))

    # Display recommendations in columns
    columns = st.columns(len(recommendations))

    for idx, col in enumerate(columns):
        with col:
            st.text(movie_titl[idx])
            st.image(poster_li[idx])
