import streamlit as st
import requests
import xml.etree.ElementTree as ET
import random
from datetime import datetime, timedelta

# 1. Configuración de página
st.set_page_config(page_title="Nodo", layout="wide")

# 2. Estilo Editorial y Jerarquía Visual Reforzada (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Lora:ital,wght@0,700;1,700&display=swap');
    
    /* Fondo gris claro para resaltar tarjetas blancas */
    .stApp { background-color: #f8f9fa; color: #1a1a1a; font-family: 'Inter', sans-serif; }
    .main .block-container { max-width: 1100px; padding-top: 2rem; }
    
    /* Tipografía Editorial */
    h1 { font-family: 'Lora', serif; font-size: 3.2rem; font-weight: 700; color: #000; margin-bottom: 2rem; }
    h2 { font-family: 'Inter', sans-serif; font-size: 0.9rem; font-weight: 600; color: #777 !important; text-transform: uppercase; letter-spacing: 0.15em; margin-top: 3rem; margin-bottom: 1.5rem; border-bottom: 1px solid #ddd; padding-bottom: 0.5rem; }
    
    /* Tarjetas con jerarquía clara */
    .card { 
        padding: 2.2rem; 
        border-radius: 4px; 
        border: 1px solid #e1e4e8; 
        margin-bottom: 1.8rem; 
        background-color: #ffffff; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.03); 
    }
    
    h3 { font-family: 'Lora', serif; font-size: 1.6rem; font-weight: 700; color: #1a1a1a !important; margin-bottom: 0.8rem; line-height: 1.2; }
    .metadata { font-family: 'Inter', sans-serif; font-size: 0.75rem; color: #888 !important; margin-bottom: 1.2rem; font-weight: 500; letter-spacing: 0.05em; }
    .source-tag { color: #000; font-weight: 700; text-transform: uppercase; border-right: 1px solid #ddd; padding-right: 8px; margin-right: 8px; }
    
    .stMarkdown p { font-size: 1.05rem; color: #333 !important; line-height: 1.7; }
    a { color: #0066cc !important; text-decoration: none; font-weight: 600; font-size: 0.9rem; }
    
    /* Botón sobrio */
    .stButton>button { border-radius: 0; border: 1px solid #000; background: white; color: #000; text-transform: uppercase; font-size: 0.7rem; letter-spacing: 0.1em; }
    </style>
    """, unsafe_allow_html=True)

st.title("Nodo")

# --- MOTORES DE BÚSQUEDA ---

def obtener_noticias(query, dias_atras, cantidad=3, idioma='es'):
    try:
        api_key = st.secrets["NEWS_API_KEY"]
        # Fecha dinámica según la restricción temporal solicitada
        fecha_limite = (datetime.now() - timedelta(days=dias_atras)).strftime('%Y-%m-%d')
        url = f"https://newsapi.org/v2/everything?q={query}&from={fecha_limite}&language={idioma}&sortBy=publishedAt&pageSize={cantidad}&apiKey={api_key}"
        response = requests.get(url)
        return response.json().get('articles', [])
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
    st.header("Global Tech (30 días)")
    q_tech = "('artificial intelligence' OR 'machine learning' OR 'data science') -health -medicine -nigeria"
    for art in obtener_noticias(q_tech, dias_atras=30, idioma='en'):
        st.markdown(f"""<div class="card">
            <div class="metadata"><span class="source-tag">{art['source']['name']}</span>{art['publishedAt'][:10]}</div>
            <h3>{art['title']}</h3>
            <p>{art['description'][:160] if art['description'] else ''}...</p>
            <a href="{art['url']}" target="_blank">READ FULL STORY →</a>
        </div>""", unsafe_allow_html=True)

with col_arg:
    st.header("Argentina (14 días)")
    q_arg = "(economía OR política OR sociedad) AND 'Argentina' -Chile -Uruguay"
    for art in obtener_noticias(q_arg, dias_atras=14, idioma='es'):
        st.markdown(f"""<div class="card">
            <div class="metadata"><span class="source-tag">{art['source']['name']}</span>{art['publishedAt'][:10]}</div>
            <h3>{art['title']}</h3>
            <p>{art['description'][:160] if art['description'] else ''}...</p>
            <a href="{art['url']}" target="_blank">LEER ARTÍCULO COMPLETO →</a>
        </div>""", unsafe_allow_html=True)

st.header("Literatura Científica")
q_papers = "('complex systems' OR 'computational social science' OR 'behavioral economics')"
for p in obtener_papers(q_papers):
    st.markdown(f"""<div class="card">
        <div class="metadata"><span class="source-tag">ARXIV</span>{p['date']}</div>
        <h3>{p['title']}</h3>
        <p>{p['summary'][:220]}...</p>
        <a href="{p['url']}" target="_blank">CONSULTAR FUENTE ORIGINAL →</a>
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

n_azar = obtener_noticias(st.session_state.tema_actual, dias_atras=90, cantidad=1, idioma='es')
for n in n_azar:
    st.subheader(n['title'])
    st.markdown(f"[Explorar contenido]({n['url']})")
