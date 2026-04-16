import streamlit as st
import requests
import xml.etree.ElementTree as ET
import random
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Nodo", layout="centered")

# Estilo de Alto Contraste para legibilidad
st.markdown("""
    <style>
    /* Forzar fondo blanco y texto oscuro */
    .stApp { background-color: #ffffff; color: #1a1a1a; }
    
    /* Títulos nítidos */
    h1 { font-size: 2.2rem; font-weight: 700; color: #000000 !important; letter-spacing: -0.02em; }
    h2 { font-size: 1.1rem; font-weight: 600; color: #666666 !important; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 3rem; border-bottom: 1px solid #eeeeee; padding-bottom: 0.5rem; }
    h3 { font-size: 1.4rem; font-weight: 600; color: #1a1a1a !important; margin-bottom: 0.2rem; line-height: 1.3; }
    
    /* Cuerpo de texto legible */
    .stMarkdown p { font-size: 1.05rem; color: #222222 !important; line-height: 1.6; }
    .metadata { font-size: 0.8rem; color: #777777 !important; margin-bottom: 1rem; font-weight: 500; }
    
    /* Enlaces sobrios */
    a { color: #0066cc !important; text-decoration: none; font-weight: 500; }
    a:hover { text-decoration: underline; }
    
    /* Botón */
    .stButton>button { border-radius: 4px; border: 1px solid #cccccc; background: white; color: #333333; }
    </style>
    """, unsafe_allow_html=True)

st.title("Nodo")
st.markdown("<p style='color: #444;'>Digest personal de información estratégica.</p>", unsafe_allow_html=True)

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

# --- RENDERIZADO ---
st.header("Actualidad")
noticias = obtener_noticias("sistemas complejos OR 'análisis de datos' OR economía OR 'inteligencia artificial'")
for art in noticias:
    st.subheader(art['title'])
    st.markdown(f"<div class='metadata'>{art['source']['name'].upper()} / {art['publishedAt'][:10]}</div>", unsafe_allow_html=True)
    st.write(art['description'])
    st.markdown(f"[Leer artículo]({art['url']})")
    st.write("---")

st.header("Literatura Científica")
papers = obtener_papers("complex systems OR data science OR economics")
for p in papers:
    st.subheader(p['title'])
    st.markdown(f"<div class='metadata'>ARXIV / {p['date']}</div>", unsafe_allow_html=True)
    st.write(f"{p['summary'][:250]}...")
    st.markdown(f"[Consultar fuente]({p['url']})")
    st.write("---")

st.header("Exploración Aleatoria")
temas_azar = ["astronomía", "urbanismo", "paleontología", "teoría de juegos", "biología marina"]
if 'tema_actual' not in st.session_state: st.session_state.tema_actual = random.choice(temas_azar)

col1, col2 = st.columns([3, 1])
with col1: st.write(f"Perspectiva de hoy: **{st.session_state.tema_actual.capitalize()}**")
with col2:
    if st.button("Cambiar"):
        st.session_state.tema_actual = random.choice(temas_azar)
        st.rerun()

noticias_azar = obtener_noticias(st.session_state.tema_actual, cantidad=1)
for n in noticias_azar:
    st.subheader(n['title'])
    st.markdown(f"[Explorar contenido]({n['url']})")
