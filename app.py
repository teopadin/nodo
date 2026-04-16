import streamlit as st
import requests

# Configuración de página
st.set_page_config(page_title="Nodo", layout="wide")

# Estilo minimalista mediante CSS
st.markdown("""
    <style>
    .reportview-container { background: #ffffff; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; font-weight: 400; color: #1a1a1a; }
    hr { margin-top: 1rem; margin-bottom: 1rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("Nodo")
st.write("Digest personal de noticias y artículos.")
st.write("---")

def obtener_noticias(query):
    api_key = st.secrets["NEWS_API_KEY"]
    url = f"https://newsapi.org/v2/everything?q={query}&language=es&sortBy=relevancy&pageSize=5&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('articles', [])
    return []

# Sección de Noticias
st.header("Actualidad")

temas = "sistemas complejos OR 'análisis de datos' OR economía OR 'inteligencia artificial'"
noticias = obtener_noticias(temas)

if noticias:
    for art in noticias:
        st.subheader(art['title'])
        st.write(art['description'])
        st.markdown(f"[Leer artículo]({art['url']})")
        st.write("---")
else:
    st.write("No hay noticias disponibles en este momento.")
