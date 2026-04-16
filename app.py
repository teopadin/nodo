import streamlit as st
import requests
import xml.etree.ElementTree as ET
import random
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Nodo", layout="wide")

# Estilo de Alto Contraste y Minimalismo
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; }
    h1 { font-size: 2.2rem; font-weight: 700; color: #000000 !important; letter-spacing: -0.02em; }
    h2 { font-size: 1.1rem; font-weight: 600; color: #666666 !important; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 2rem; border-bottom: 1px solid #eeeeee; padding-bottom: 0.5rem; }
    h3 { font-size: 1.2rem; font-weight: 600; color: #1a1a1a !important; line-height: 1.3; margin-top: 1rem; }
    .stMarkdown p { font-size: 1rem; color: #222222 !important; line-height: 1.5; }
    .metadata { font-size: 0.75rem; color: #777777 !important; margin-bottom: 0.5rem; font-weight: 500; }
    a { color: #0066cc !important; text-decoration: none; }
    hr { border: 0; border-top: 1px solid #f0f0f0; margin: 1.5rem 0; }
    .stButton>button { border-radius: 4px; border: 1px solid #cccccc; background: white; color: #333333; font-size: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("Nodo")
st.markdown("<p style='color: #444;'>Digest estratégico de tecnología y actualidad nacional.</p>", unsafe_allow_html=True)

# --- MOTORES DE BÚSQUEDA ---

def obtener_noticias(query, cantidad=3, idioma='es'):
    try:
        api_key = st.secrets["NEWS_API_KEY"]
        url = f"https://newsapi.org/v2/everything?q={query}&language={idioma}&sortBy=publishedAt&pageSize={cantidad}&apiKey={api_key}"
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

# Sección 1: Actualidad Segmentada
col_tech, col_arg = st.columns(2)

with col_tech:
    st.header("Global Tech")
    q_tech = "('complex systems' OR 'data science' OR 'artificial intelligence')"
    noticias_tech = obtener_noticias(q_tech, idioma='en')
    for art in noticias_tech:
        st.subheader(art['title'])
        st.markdown(f"<div class='metadata'>{art['source']['name'].upper()} / {art['publishedAt'][:10]}</div>", unsafe_allow_html=True)
        st.write(art['description'][:200] + "...")
        st.markdown(f"[Source]({art['url']})")
        st.write("---")

with col_arg:
    st.header("Argentina")
    q_arg = "(economía OR sociedad OR política) AND Argentina"
    noticias_arg = obtener_noticias(q_arg, idioma='es')
    for art in noticias_arg:
        st.subheader(art['title'])
        st.markdown(f"<div class='metadata'>{art['source']['name'].upper()} / {art['publishedAt'][:10]}</div>", unsafe_allow_html=True)
        st.write(art['description'][:200] + "...")
        st.markdown(f"[Leer artículo]({art['url']})")
        st.write("---")

# Sección 2: Literatura Científica
st.header("Literatura Científica (arXiv)")
papers = obtener_papers("complex systems OR data science OR economics")
for p in papers:
    st.subheader(p['title'])
    st.markdown(f"<div class='metadata'>ARXIV / {p['date']}</div>", unsafe_allow_html=True)
    st.write(f"{p['summary'][:250]}...")
    st.markdown(f"[Consultar fuente]({p['url']})")
    st.write("---")

# Sección 3: Exploración Aleatoria
st.header("Exploración Aleatoria")
temas_azar = ["astronomía", "urbanismo", "paleontología", "teoría de juegos", "biología marina"]
if 'tema_actual' not in st.session_state: st.session_state.tema_actual = random.choice(temas_azar)

c1, c2 = st.columns([4, 1])
with c1: st.write(f"Hoy: **{st.session_state.tema_actual.capitalize()}**")
with c2:
    if st.button("Cambiar"):
        st.session_state.tema_actual = random.choice(temas_azar)
        st.rerun()

n_azar = obtener_noticias(st.session_state.tema_actual, cantidad=1, idioma='es')
for n in n_azar:
    st.subheader(n['title'])
    st.markdown(f"[Explorar]({n['url']})")
