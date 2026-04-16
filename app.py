import streamlit as st
import requests
import xml.etree.ElementTree as ET
import random

# Configuración de página
st.set_page_config(page_title="Nodo", layout="wide")

# Estilo minimalista
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

# --- FUNCIONES ---

def obtener_noticias(query, cantidad=5):
    api_key = st.secrets["NEWS_API_KEY"]
    url = f"https://newsapi.org/v2/everything?q={query}&language=es&sortBy=relevancy&pageSize={cantidad}&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('articles', [])
    return []

def obtener_papers(query):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5"
    response = requests.get(url)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        papers = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            papers.append({
                'title': entry.find('{http://www.w3.org/2005/Atom}title').text,
                'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text,
                'url': entry.find('{http://www.w3.org/2005/Atom}id').text
            })
        return papers
    return []

# --- RENDERIZADO ---

# 1. Actualidad (Tus intereses)
st.header("Actualidad")
temas_interes = "sistemas complejos OR 'análisis de datos' OR economía OR 'inteligencia artificial'"
noticias = obtener_noticias(temas_interes)
for art in noticias:
    st.subheader(art['title'])
    st.write(art['description'])
    st.markdown(f"[Leer artículo]({art['url']})")
    st.write("---")

# 2. Literatura Científica (arXiv)
st.header("Literatura Científica")
papers = obtener_papers("complex systems OR data science OR economics")
for p in papers:
    st.subheader(p['title'].replace('\n', ' '))
    st.write(p['summary'][:300].replace('\n', ' ') + "...")
    st.markdown(f"[Ver paper]({p['url']})")
    st.write("---")

# 3. Fuera de la burbuja (Azar)
st.header("Fuera de la burbuja")
temas_azar = ["astronomía", "arte renacentista", "biología marina", "urbanismo", "paleontología"]
tema_elegido = random.choice(temas_azar)
st.write(f"Explorando hoy: {tema_elegido}")
noticias_azar = obtener_noticias(tema_elegido, cantidad=1)
for n in noticias_azar:
    st.subheader(n['title'])
    st.write(n['description'])
    st.markdown(f"[Explorar]({n['url']})")
