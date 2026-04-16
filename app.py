import streamlit as st
import requests
import xml.etree.ElementTree as ET
import random
from datetime import datetime

# Configuración de página - Enfoque centrado para mejor lectura
st.set_page_config(page_title="Nodo", layout="centered")

# Estilo Estrictamente Minimalista
st.markdown("""
    <style>
    /* Fondo y fuente base */
    .stApp { background-color: #ffffff; font-family: 'Inter', sans-serif; }
    
    /* Títulos y secciones */
    h1 { font-size: 2.2rem; font-weight: 700; color: #1a1a1a; letter-spacing: -0.02em; }
    h2 { font-size: 1.2rem; font-weight: 600; color: #888; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 3rem; border-bottom: 1px solid #f0f0f0; padding-bottom: 0.5rem; }
    h3 { font-size: 1.4rem; font-weight: 500; color: #1a1a1a; margin-bottom: 0.2rem; line-height: 1.3; }
    
    /* Metadatos y texto */
    .metadata { font-size: 0.8rem; color: #999; margin-bottom: 1rem; }
    .stMarkdown p { font-size: 1.05rem; color: #444; line-height: 1.6; }
    
    /* Botón minimalista */
    .stButton>button { border-radius: 4px; border: 1px solid #e0e0e0; background: transparent; color: #666; padding: 0.4rem 1rem; transition: all 0.2s; }
    .stButton>button:hover { border-color: #1a1a1a; color: #1a1a1a; }
    
    /* Separadores */
    hr { border: 0; border-top: 1px solid #f8f8f8; margin: 2rem 0; }
    </style>
    """, unsafe_allow_html=True)

st.title("Nodo")
st.markdown("<p style='color: #666;'>Digest personal de información estratégica.</p>", unsafe_allow_html=True)

# --- MOTORES DE BÚSQUEDA ---

def obtener_noticias(query, cantidad=5):
    try:
        api_key = st.secrets["NEWS_API_KEY"]
        url = f"https://newsapi.org/v2/everything?q={query}&language=es&sortBy=publishedAt&pageSize={cantidad}&apiKey={api_key}"
        return requests.get(url).json().get('articles', [])
    except: return []

def obtener_papers(query):
    try:
        url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending"
        root = ET.fromstring(requests.get(url).content)
        papers = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            fecha = datetime.fromisoformat(entry.find('{http://www.w3.org/2005/Atom}published').text.replace('Z', '+00:00'))
            papers.append({
                'title': entry.find('{http://www.w3.org/2005/Atom}title').text.strip(),
                'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text.strip(),
                'url': entry.find('{http://www.w3.org/2005/Atom}id').text,
                'date': fecha.strftime("%d.%m.%Y")
            })
        return papers
    except: return []

# --- CONTENIDO ---

# 1. ACTUALIDAD
st.header("Actualidad")
noticias = obtener_noticias("sistemas complejos OR 'análisis de datos' OR economía OR 'inteligencia artificial'")
for art in noticias:
    st.subheader(art['title'])
    st.markdown(f"<div class='metadata'>{art['source']['name'].upper()} / {art['publishedAt'][:10]}</div>", unsafe_allow_html=True)
    st.write(art['description'])
    st.markdown(f"[Leer artículo]({art['url']})")
    st.write("---")

# 2. LITERATURA CIENTÍFICA
st.header("Literatura Científica")
papers = obtener_papers("complex systems OR data science OR economics")
for p in papers:
    st.subheader(p['title'])
    st.markdown(f"<div class='metadata'>ARXIV / {p['date']}</div>", unsafe_allow_html=True)
    st.write(f"{p['summary'][:250]}...")
    st.markdown(f"[Consultar fuente]({p['url']})")
    st.write("---")

# 3. FUERA DE LA BURBUJA
st.header("Exploración Aleatoria")
temas_azar = ["astronomía", "urbanismo", "paleontología", "teoría de juegos", "biología marina"]

if 'tema_actual' not in st.session_state:
    st.session_state.tema_actual = random.choice(temas_azar)

col1, col2 = st.columns([3, 1])
with col1:
    st.write(f"Perspectiva de hoy: **{st.session_state.tema_actual.capitalize()}**")
with col2:
    if st.button("Cambiar tema"):
        st.session_state.tema_actual = random.choice(temas_azar)
        st.rerun()

noticias_azar = obtener_noticias(st.session_state.tema_actual, cantidad=1)
for n in noticias_azar:
    st.subheader(n['title'])
    st.markdown(f"[Explorar contenido]({n['url']})")
