import streamlit as st
import requests
import xml.etree.ElementTree as ET

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

# --- FUNCIONES DE OBTENCIÓN DE DATOS ---

def obtener_noticias(query):
    api_key = st.secrets["NEWS_API_KEY"]
    url = f"https://newsapi.org/v2/everything?q={query}&language=es&sortBy=relevancy&pageSize=5&apiKey={api_key}"
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

# --- RENDERIZADO DE SECCIONES ---

# Sección: Noticias
st.header("Actualidad")
temas_noticias = "sistemas complejos OR 'análisis de datos' OR economía OR 'inteligencia artificial'"
noticias = obtener_noticias(temas_noticias)

if noticias:
    for art in noticias:
        st.subheader(art['title'])
        st.write(art['description'])
        st.markdown(f"[Leer artículo]({art['url']})")
        st.write("---")

# Sección: Papers Académicos
st.header("Literatura Científica")
# Buscamos en categorías generales (Broad) según lo acordado
temas_papers = "complex systems OR data science OR economics"
papers = obtener_papers(temas_papers)

if papers:
    for p in papers:
        st.subheader(p['title'].replace('\n', ' '))
        # Recortamos el resumen para mantener el minimalismo
        resumen = p['summary'][:300].replace('\n', ' ') + "..."
        st.write(resumen)
        st.markdown(f"[Ver paper]({p['url']})")
        st.write("---")
else:
    st.write("No hay publicaciones académicas recientes.")
