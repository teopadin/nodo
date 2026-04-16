import streamlit as st
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# ─── CONFIG ───────────────────────────────────────────────
st.set_page_config(page_title="Nodo", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:wght@300;400;600&display=swap');

/* Base */
.stApp { background-color: #f7f4ef; color: #1c1c1c; font-family: 'Source Sans 3', sans-serif; }
.main .block-container { max-width: 1140px; padding-top: 2rem; padding-bottom: 4rem; }

/* Cabecera tipo diario */
.masthead {
    text-align: center;
    border-top: 3px solid #1c1c1c;
    border-bottom: 3px solid #1c1c1c;
    padding: 1.2rem 0 1rem 0;
    margin-bottom: 0.4rem;
}
.masthead-title {
    font-family: 'Playfair Display', serif;
    font-size: 5rem;
    font-weight: 700;
    color: #1c1c1c;
    letter-spacing: -0.02em;
    line-height: 1;
    margin: 0;
}
.masthead-sub {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #888;
    margin-top: 0.5rem;
}
.masthead-date {
    font-size: 0.72rem;
    color: #aaa;
    margin-top: 0.2rem;
    letter-spacing: 0.05em;
}
.divider-thick { border: none; border-top: 2px solid #1c1c1c; margin: 0.5rem 0 2.5rem 0; }
.divider-thin  { border: none; border-top: 1px solid #d9d4cc; margin: 2rem 0; }

/* Etiquetas de sección */
.section-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #9c6b3c;
    margin-bottom: 1.2rem;
    display: block;
}

/* Artículo principal (hero) */
.hero-card {
    padding: 0 0 2rem 0;
    border-bottom: 1px solid #d9d4cc;
    margin-bottom: 2rem;
}
.hero-card h2 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.4rem !important;
    font-weight: 700 !important;
    color: #1c1c1c !important;
    line-height: 1.2 !important;
    margin-bottom: 0.8rem !important;
    border: none !important;
    text-transform: none !important;
    letter-spacing: normal !important;
    padding: 0 !important;
}
.hero-card p { font-size: 1.05rem; color: #444; line-height: 1.75; }
.hero-meta { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #aaa; margin-bottom: 0.6rem; }
.hero-source { color: #9c6b3c; margin-right: 10px; }

/* Artículos secundarios (lista) */
.item-card {
    padding: 1.2rem 0;
    border-bottom: 1px solid #e8e3db;
}
.item-card h4 {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #1c1c1c;
    line-height: 1.3;
    margin-bottom: 0.4rem;
}
.item-meta { font-size: 0.68rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #bbb; margin-bottom: 0.3rem; }
.item-source { color: #9c6b3c; margin-right: 8px; }
.item-card p { font-size: 0.9rem; color: #666; line-height: 1.6; margin-bottom: 0.5rem; }

/* Papers */
.paper-card {
    padding: 1.2rem 0;
    border-bottom: 1px solid #e8e3db;
    display: flex;
    gap: 1.5rem;
    align-items: flex-start;
}
.paper-index {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: #e0dbd3;
    line-height: 1;
    min-width: 2rem;
    text-align: right;
}
.paper-card h4 { font-family: 'Playfair Display', serif; font-size: 1.05rem; font-weight: 700; color: #1c1c1c; line-height: 1.3; margin-bottom: 0.3rem; }
.paper-card p { font-size: 0.85rem; color: #777; line-height: 1.55; }

/* Links */
a { color: #9c6b3c !important; text-decoration: none !important; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; }
a:hover { text-decoration: underline !important; }

/* Vacío */
.empty-state { font-size: 0.85rem; color: #bbb; font-style: italic; padding: 1.5rem 0; }

/* Ocultar elementos Streamlit */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── CABECERA ─────────────────────────────────────────────
hoy = datetime.now().strftime("%A, %d de %B de %Y").capitalize()
st.markdown(f"""
<div class="masthead">
    <div class="masthead-title">Nodo</div>
    <div class="masthead-sub">Tecnología · Economía · Ciencia</div>
    <div class="masthead-date">{hoy}</div>
</div>
<hr class="divider-thick">
""", unsafe_allow_html=True)


# ─── HELPERS ──────────────────────────────────────────────
def fmt_fecha(fecha_str):
    try:
        return datetime.fromisoformat(fecha_str.replace('Z', '+00:00')).strftime("%d/%m/%Y")
    except:
        return fecha_str

def obtener_noticias(query, dias_atras, dominios, cantidad=4, idioma='es'):
    try:
        api_key = st.secrets["NEWS_API_KEY"]
        desde = (datetime.now() - timedelta(days=dias_atras)).strftime('%Y-%m-%d')
        params = f"q={query}&from={desde}&sortBy=relevancy&pageSize={cantidad}&apiKey={api_key}&language={idioma}"
        if dominios:
            params += f"&domains={dominios}"
        r = requests.get(f"https://newsapi.org/v2/everything?{params}", timeout=8)
        return r.json().get('articles', [])
    except:
        return []

def obtener_papers(query, cantidad=4):
    try:
        url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={cantidad}&sortBy=submittedDate&sortOrder=descending"
        root = ET.fromstring(requests.get(url, timeout=8).content)
        papers = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            # Extraer solo la primera oración del abstract
            summary_full = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
            summary_short = summary_full.split('.')[0] + '.' if '.' in summary_full else summary_full[:120]
            authors = [a.find('{http://www.w3.org/2005/Atom}name').text
                       for a in entry.findall('{http://www.w3.org/2005/Atom}author')]
            papers.append({
                'title': entry.find('{http://www.w3.org/2005/Atom}title').text.strip(),
                'summary': summary_short,
                'authors': ', '.join(authors[:2]) + (' et al.' if len(authors) > 2 else ''),
                'url': entry.find('{http://www.w3.org/2005/Atom}id').text,
                'date': fmt_fecha(entry.find('{http://www.w3.org/2005/Atom}published').text)
            })
        return papers
    except:
        return []

def render_hero(art):
    fecha = fmt_fecha(art.get('publishedAt', ''))
    fuente = art['source']['name']
    desc = (art.get('description') or '')[:220]
    st.markdown(f"""
    <div class="hero-card">
        <div class="hero-meta"><span class="hero-source">{fuente}</span>{fecha}</div>
        <h2>{art['title']}</h2>
        <p>{desc}…</p>
        <a href="{art['url']}" target="_blank">Leer nota completa →</a>
    </div>""", unsafe_allow_html=True)

def render_item(art):
    fecha = fmt_fecha(art.get('publishedAt', ''))
    fuente = art['source']['name']
    desc = (art.get('description') or '')[:130]
    st.markdown(f"""
    <div class="item-card">
        <div class="item-meta"><span class="item-source">{fuente}</span>{fecha}</div>
        <h4>{art['title']}</h4>
        <p>{desc}…</p>
        <a href="{art['url']}" target="_blank">Leer →</a>
    </div>""", unsafe_allow_html=True)

def render_paper(p, idx):
    st.markdown(f"""
    <div class="paper-card">
        <div class="paper-index">{str(idx).zfill(2)}</div>
        <div>
            <div class="item-meta">{p['authors']} · {p['date']}</div>
            <h4>{p['title']}</h4>
            <p>{p['summary']}</p>
            <a href="{p['url']}" target="_blank">Ver en ArXiv →</a>
        </div>
    </div>""", unsafe_allow_html=True)

def empty_state(msg="No se encontraron resultados en este momento."):
    st.markdown(f'<div class="empty-state">{msg}</div>', unsafe_allow_html=True)


# ─── LAYOUT PRINCIPAL: 2 COLUMNAS ─────────────────────────
col_tech, col_arg = st.columns([3, 2], gap="large")

with col_tech:
    st.markdown('<span class="section-label">Tecnología Global</span>', unsafe_allow_html=True)
    fuentes_tech = "techcrunch.com,wired.com,arstechnica.com,venturebeat.com,technologyreview.com"
    arts_tech = obtener_noticias(
        "artificial intelligence OR machine learning OR startups",
        dias_atras=14, dominios=fuentes_tech, cantidad=4, idioma='en'
    )
    if arts_tech:
        render_hero(arts_tech[0])
        for a in arts_tech[1:]:
            render_item(a)
    else:
        empty_state("No hay noticias de tecnología disponibles.")

with col_arg:
    st.markdown('<span class="section-label">Economía Argentina</span>', unsafe_allow_html=True)
    fuentes_ar = "lanacion.com.ar,infobae.com,cronista.com,ambito.com"
    arts_arg = obtener_noticias(
        "economía OR inflación OR dólar OR política económica",
        dias_atras=7, dominios=fuentes_ar, cantidad=4, idioma='es'
    )
    if arts_arg:
        render_hero(arts_arg[0])
        for a in arts_arg[1:]:
            render_item(a)
    else:
        empty_state("No hay noticias argentinas disponibles.")

st.markdown('<hr class="divider-thin">', unsafe_allow_html=True)

# ─── PAPERS ───────────────────────────────────────────────
st.markdown('<span class="section-label">Ciencia Reciente</span>', unsafe_allow_html=True)

# Queries más específicas y variadas — más relevantes que el genérico anterior
queries_papers = [
    "large language models",
    "economic complexity Argentina",
    "network science social systems"
]
papers = []
for q in queries_papers:
    papers += obtener_papers(q, cantidad=2)
    if len(papers) >= 4:
        break
papers = papers[:4]

if papers:
    p_col1, p_col2 = st.columns(2, gap="large")
    for i, p in enumerate(papers):
        with (p_col1 if i % 2 == 0 else p_col2):
            render_paper(p, i + 1)
else:
    empty_state("No se pudieron cargar papers en este momento.")
