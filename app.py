import streamlit as st
import requests
import xml.etree.ElementTree as ET
import random
from datetime import datetime

# 1. Configuración de página
st.set_page_config(page_title="Nodo", layout="wide")

# 2. Refuerzo de Jerarquía Visual (CSS)
st.markdown("""
    <style>
    /* Fondo gris claro para contraste de planos */
    .stApp { background-color: #f8f9fa; color: #1a1a1a; }
    
    /* Contenedor principal centrado */
    .main .block-container { max-width: 1000px; padding-top: 2rem; }

    h1 { font-size: 2.8rem; font-weight: 800; color: #000; margin-bottom: 2rem; }
    h2 { font-size: 1.1rem; font-weight: 700; color: #555 !important; text-transform: uppercase; letter-spacing: 0.12em; margin-top: 3rem; margin-bottom: 1.5rem; border-bottom: 1px solid #ddd; padding-bottom: 0.5rem; }
    
    /* Tarjetas blancas con borde definido para jerarquía clara */
    .card {
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #e1e4e8;
        margin-bottom: 1.5rem;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    h3 { font-size: 1.4rem; font-weight: 700; color: #1a1a1a !important; margin-bottom: 0.8rem; line-height: 1.25; }
    .metadata { font-size: 0.8rem; color: #666 !important; margin-bottom: 1rem; font-family: monospace; font-weight: 600; }
    .source-tag { color: #0066cc; text-transform: uppercase; margin-right: 8px; }
    
    .stMarkdown p { font-size: 1.05rem; color: #333 !important; line-height: 1.6; }
    
    a { color: #0066cc !important; text-decoration: none; font-weight: 600; }
    a:hover { text-decoration: underline; }
    
    /* Estilo del botón */
    .stButton>button { border-radius: 6px; border: 1px solid #ccc; background: white; color: #333; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

st.title("Nodo")

# --- MOTORES DE BÚSQUEDA ---
def obtener_noticias(query, cantidad=3, idioma='es'):
    try:
        api_key = st.secrets["NEWS_API_KEY"]
        url = f"https://newsapi.org/v2/everything?q={query}&language={idioma}&sortBy=relevancy&pageSize={cantidad}&apiKey={api_key}"
        return requests.get(url).json().get('articles', [])
    except: return []

def obtener_papers(query, cantidad=3):
    try:
        url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={cantidad}&sortBy=submittedDate&sortOrder=descending"
        root = ET.fromstring(requests.get(url).content)
        papers = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            fecha_str = entry.find('{http://www.w3.org/2005/Atom}published').text
            fecha = datetime.fromisoformat(fecha_str.replace('Z', '+00:00'))
            papers.append({
                'title': entry.find('{http://www.w3.org/2005/Atom}title').text.strip(),
                'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text.strip(),
                'url': entry.find('{http://www.w3.org/2005/Atom}id').text,
                'date': fecha.strftime("%d.%m.%Y")
            })
        return papers
    except: return []

# --- RENDERIZADO ---

col_tech, col_arg = st.columns(2, gap="large")

with col_tech:
    st.header("Global Tech")
    q_tech = "('artificial intelligence' OR 'machine learning' OR 'data science') -health -medicine -nigeria"
    for art in obtener_noticias(q_tech, idioma='en'):
        st.markdown(f"""<div class="card">
            <div class="metadata"><span class="source-tag">{art['source']['name']}</span> / {art['publishedAt'][:10]}</div>
            <h3>{art['title']}</h3>
            <p>{art['description'][:160] if art['description'] else ''}...</p>
            <a href="{art['url']}" target="_blank">Read Article →</a>
        </div>""", unsafe_allow_html=True)

with col_arg:
    st.header("Argentina")
    q_arg = "(economía OR política OR sociedad) AND 'Argentina' -Chile -Uruguay"
    for art in obtener_noticias(q_arg, idioma='es'):
        st.markdown(f"""<div class="card">
            <div class="metadata"><span class="source-tag">{art['source']['name']}</span> / {art['publishedAt'][:10]}</div>
            <h3>{art['title']}</h3>
            <p>{art['description'][:160] if art['description'] else ''}...</p>
            <a href="{art['url']}" target="_blank">Leer artículo →</a>
        </div>""", unsafe_allow_html=True)

st.header("Literatura Científica")
q_papers = "('complex systems' OR 'computational social science' OR 'behavioral economics')"
for p in obtener_papers(q_papers):
    st.markdown(f"""<div class="card">
        <div class="metadata"><span class="source-tag">ARXIV</span> / {p['date']}</div>
        <h3>{p['title']}</h3>
        <p>{p['summary'][:220]}...</p>
        <a href="{p['url']}" target="_blank">Consultar fuente →</a>
    </div>""", unsafe_allow_html=True)

# Sección de Azar
st.header("Exploración Aleatoria")
temas_azar = ["urbanismo", "paleontología", "teoría de juegos", "biología marina", "historia antigua"]
if 'tema_actual' not in st.session_state: st.session_state.tema_actual = random.choice(temas_azar)

c1, c2 = st.columns([5, 1])
with c1: st.write(f"Perspectiva de hoy: **{st.session_state.tema_actual.capitalize()}**")
with c2:
    if st.button("Cambiar"):
        st.session_state.tema_actual = random.choice(temas_azar)
        st.rerun()

n_azar = obtener_noticias(st.session_state.tema_actual, cantidad=1, idioma='es')
for n in n_azar:
    st.subheader(n['title'])
    st.markdown(f"[Explorar contenido]({n['url']})")
