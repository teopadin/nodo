import streamlit as st
import requests
import xml.etree.ElementTree as ET
import random
from datetime import datetime, timedelta

# 1. Configuración de página
st.set_page_config(page_title="Nodo", layout="wide")

# 2. Estética Editorial Refinada (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Lora:ital,wght@0,700;1,700&display=swap');
    
    .stApp { background-color: #fcfcfc; color: #1a1a1a; font-family: 'Inter', sans-serif; }
    .main .block-container { max-width: 1100px; padding-top: 3rem; }
    
    /* Título Principal */
    .main-title {
        font-family: 'Lora', serif;
        font-size: 4rem;
        font-weight: 700;
        color: #000;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .title-underline {
        width: 100px;
        height: 2px;
        background-color: #000;
        margin: 0 auto 3rem auto;
    }
    
    /* Subtítulos de Sección (Sin mención de días) */
    h2 { 
        font-family: 'Inter', sans-serif; 
        font-size: 0.85rem; 
        font-weight: 600; 
        color: #555 !important; 
        text-transform: uppercase; 
        letter-spacing: 0.2em; 
        margin-top: 3rem; 
        margin-bottom: 1.5rem; 
        border-bottom: 1px solid #eee;
        padding-bottom: 0.5rem;
    }
    
    /* Tarjetas de Noticias */
    .card { 
        padding: 2rem; 
        border-radius: 0px; 
        border-left: 3px solid #000; 
        margin-bottom: 2rem; 
        background-color: #ffffff; 
        box-shadow: 0 5px 15px rgba(0,0,0,0.02);
    }
    
    h3 { font-family: 'Lora', serif; font-size: 1.5rem; font-weight: 700; color: #1a1a1a !important; margin-bottom: 1rem; line-height: 1.25; }
    
    /* Metadatos y Fechas (Formato AR) */
    .metadata { 
        font-family: 'Inter', sans-serif; 
        font-size: 0.75rem; 
        color: #888 !important; 
        margin-bottom: 1rem; 
        font-weight: 600; 
        text-transform: uppercase; 
        letter-spacing: 0.05em; 
    }
    .source-tag { color: #000; border-right: 1px solid #ddd; padding-right: 10px; margin-right: 10px; }
    
    .stMarkdown p { font-size: 1.05rem; color: #444 !important; line-height: 1.8; }
    a { color: #000 !important; text-decoration: underline; font-weight: 600; font-size: 0.8rem; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# Encabezado
st.markdown('<h1 class="main-title">Nodo</h1><div class="title-underline"></div>', unsafe_allow_html=True)

# --- FUNCIONES DE AYUDA ---

def formatear_fecha_ar(fecha_str):
    """Convierte fechas ISO a formato DD/MM/AAAA"""
    try:
        # Intenta parsear la fecha (NewsAPI suele venir como 2023-10-27T...)
        fecha_obj = datetime.fromisoformat(fecha_str.replace('Z', '+00:00'))
        return fecha_obj.strftime("%d/%m/%Y")
    except:
        return fecha_str

# --- MOTORES DE BÚSQUEDA ---

def obtener_noticias(query, dias_atras, cantidad=3, idioma='es'):
    try:
        api_key = st.secrets["NEWS_API_KEY"]
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
            fecha_raw = entry.find('{http://www.w3.org/2005/Atom}published').text
            papers.append({
                'title': entry.find('{http://www.w3.org/2005/Atom}title').text.strip(),
                'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text.strip(),
                'url': entry.find('{http://www.w3.org/2005/Atom}id').text,
                'date': formatear_fecha_ar(fecha_raw)
            })
        return papers
    except: return []

# --- RENDERIZADO ---

col_tech, col_arg = st.columns(2, gap="large")

with col_tech:
    st.header("Global Tech")
    q_tech = "('artificial intelligence' OR 'machine learning')"
    for art in obtener_noticias(q_tech, dias_atras=30, idioma='en'):
        fecha_ar = formatear_fecha_ar(art['publishedAt'])
        st.markdown(f"""<div class="card">
            <div class="metadata"><span class="source-tag">{art['source']['name']}</span>{fecha_ar}</div>
            <h3>{art['title']}</h3>
            <p>{art['description'][:150] if art['description'] else ''}...</p>
            <a href="{art['url']}" target="_blank">Full Report →</a>
        </div>""", unsafe_allow_html=True)

with col_arg:
    st.header("Actualidad Argentina")
    q_arg = "(economía OR política) AND 'Argentina'"
    for art in obtener_noticias(q_arg, dias_atras=14, idioma='es'):
        fecha_ar = formatear_fecha_ar(art['publishedAt'])
        st.markdown(f"""<div class="card">
            <div class="metadata"><span class="source-tag">{art['source']['name']}</span>{fecha_ar}</div>
            <h3>{art['title']}</h3>
            <p>{art['description'][:150] if art['description'] else ''}...</p>
            <a href="{art['url']}" target="_blank">Leer más →</a>
        </div>""", unsafe_allow_html=True)

st.header("Exploración Científica")
for p in obtener_papers("complex systems"):
    st.markdown(f"""<div class="card">
        <div class="metadata"><span class="source-tag">ArXiv Paper</span>{p['date']}</div>
        <h3>{p['title']}</h3>
        <p>{p['summary'][:200]}...</p>
        <a href="{p['url']}" target="_blank">Ver Paper →</a>
    </div>""", unsafe_allow_html=True)
        
