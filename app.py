import pickle
import streamlit as st
import requests
import pandas as pd

# Definimos una función llamada 'fetch_poster' que toma un 'movie_id' como argumento.


def fetch_poster(movie_id):
    # Construimos la URL de la API utilizando el 'movie_id' y una clave API válida.
    url = f"https://api.themoviedb.org/3/movie/{
        movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    # Realizamos una solicitud GET a la URL y almacenamos la respuesta en la variable 'data'.
    data = requests.get(url)
    # Convertimos la respuesta JSON en un diccionario utilizando el método 'json()'.
    data = data.json()
    # Extraemos la ruta del poster del diccionario 'data'.
    poster_path = data['poster_path']
    # Construimos la URL completa del poster utilizando la base URL de la API y la ruta del poster.
    full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
    # Devolvemos la URL completa del poster.
    return full_path

# Definimos una función llamada 'recommend' que toma el nombre de una película como argumento.


def recommend(movie):
    # Buscamos el índice de la película en la tabla 'movies' utilizando su título.
    index = movies[movies['title'] == movie].index[0]

    # Calculamos las distancias de similitud entre la película dada y todas las demás películas.
    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    # Listas para almacenar nombres de películas recomendadas y URLs de posters.
    recommended_movie_names = []
    recommended_movie_posters = []

    # Iteramos sobre las primeras 5 películas más similares (excluyendo la película dada).
    for i in distances[1:6]:
        # Obtenemos el 'movie_id' de la película recomendada.
        movie_id = movies.iloc[i[0]].movie_id

        # Usamos la función 'fetch_poster' para obtener la URL del poster de la película.
        recommended_movie_posters.append(fetch_poster(movie_id))

        # Agregamos el título de la película recomendada a la lista.
        recommended_movie_names.append(movies.iloc[i[0]].title)

    # Devolvemos las listas de nombres y URLs de posters de películas recomendadas.
    return recommended_movie_names, recommended_movie_posters

st.set_page_config(page_title="Sistema de recomendaciones de Películas", layout="wide")
with st.sidebar:
    # Agregar un título principal
    st.title("Sistema de recomendaciones de Películas")

    # Agregar una imagen
    st.image('https://img.blogs.es/iahuawei/wp-content/uploads/2018/12/mitos-1080x675.jpg', use_column_width=True)

    # Agregar una descripción
    st.write("Este sistema te permite seleccionar una película y obtendrás recomendaciones de películas similares.")



st.header('Sistema de Recomendación')

# Se cargan los datos necesarios para el sistema de recomendación
movies = pd.read_pickle('model/movie_list.pkl')
similarity = pd.read_pickle('model/similarity.pkl')


movie_list = movies['title'].values
selected_movie = st.selectbox("Selecciona una película de la lista", movie_list)


import streamlit as st

if st.button('Mostrar Recomendaciones'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)  # Cambia a 'st.columns' si no tienes acceso a 'st.beta_columns'.
    for i, col in enumerate(cols):
        col.text(recommended_movie_names[i])
        col.image(recommended_movie_posters[i])


