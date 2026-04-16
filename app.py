import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# ─── CONFIG ───────────────────────────────────────────────
st.set_page_config(page_title="Nodo", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:wght@300;400;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

/* Base */
.stApp { background-color: #f7f4ef; color: #1c1c1c; font-family: 'Source Sans 3', sans-serif; }
.main .block-container { max-width: 1140px; padding-top: 2rem; padding-bottom: 4rem; }
* { box-sizing: border-box; }

/* Cabecera tipo diario */
.masthead {
    text-align: center;
    border-top: 3px solid #1c1c1c;
    border-bottom: 3px solid #1c1c1c;
    padding: 1.2rem 0 1rem 0;
    margin-bottom: 0.4rem;
.stApp {
    background-color: #ffffff;
    color: #111;
    font-family: 'Inter', sans-serif;
}
.masthead-title {
    font-family: 'Playfair Display', serif;
    font-size: 5rem;
    font-weight: 700;
    color: #1c1c1c;
    letter-spacing: -0.02em;
    line-height: 1;
    margin: 0;
.main .block-container {
    max-width: 1080px;
    padding-top: 4rem;
    padding-bottom: 6rem;
}
.masthead-sub {
    font-size: 0.72rem;

/* Ocultar chrome de Streamlit */
#MainMenu, footer, header { visibility: hidden; }
.stMarkdown { margin: 0; }

/* ── Cabecera ── */
.nodo-header {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #f0f0f0;
    margin-bottom: 3rem;
}
.nodo-wordmark {
    font-size: 1rem;
   font-weight: 600;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #888;
    margin-top: 0.5rem;
    letter-spacing: -0.01em;
    color: #111;
}
.masthead-date {
.nodo-date {
   font-size: 0.72rem;
   color: #aaa;
    margin-top: 0.2rem;
    letter-spacing: 0.05em;
    font-weight: 400;
}
.divider-thick { border: none; border-top: 2px solid #1c1c1c; margin: 0.5rem 0 2.5rem 0; }
.divider-thin  { border: none; border-top: 1px solid #d9d4cc; margin: 2rem 0; }

/* Etiquetas de sección */
.section-label {
/* ── Etiqueta de sección ── */
.sect-label {
   font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.3em;
    font-weight: 600;
    letter-spacing: 0.18em;
   text-transform: uppercase;
    color: #9c6b3c;
    margin-bottom: 1.2rem;
    color: #bbb;
    margin-bottom: 1.5rem;
   display: block;
}

/* Artículo principal (hero) */
.hero-card {
    padding: 0 0 2rem 0;
    border-bottom: 1px solid #d9d4cc;
/* ── Hero ── */
.hero {
    padding-bottom: 2rem;
   margin-bottom: 2rem;
    border-bottom: 1px solid #f0f0f0;
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
.hero-source {
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #bbb;
    margin-bottom: 0.75rem;
}
.hero-card p { font-size: 1.05rem; color: #444; line-height: 1.75; }
.hero-meta { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #aaa; margin-bottom: 0.6rem; }
.hero-source { color: #9c6b3c; margin-right: 10px; }

/* Artículos secundarios (lista) */
.item-card {
    padding: 1.2rem 0;
    border-bottom: 1px solid #e8e3db;
.hero-title {
    font-size: 1.45rem;
    font-weight: 600;
    color: #111;
    line-height: 1.35;
    letter-spacing: -0.02em;
    margin-bottom: 0.75rem;
}
.item-card h4 {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #1c1c1c;
    line-height: 1.3;
    margin-bottom: 0.4rem;
.hero-desc {
    font-size: 0.875rem;
    color: #666;
    line-height: 1.7;
    font-weight: 400;
    margin-bottom: 1rem;
}
.hero-link {
    font-size: 0.68rem;
    font-weight: 500;
    color: #111 !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    text-decoration: none !important;
    border-bottom: 1px solid #111;
    padding-bottom: 1px;
}
.item-meta { font-size: 0.68rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #bbb; margin-bottom: 0.3rem; }
.item-source { color: #9c6b3c; margin-right: 8px; }
.item-card p { font-size: 0.9rem; color: #666; line-height: 1.6; margin-bottom: 0.5rem; }

/* Papers */
.paper-card {
    padding: 1.2rem 0;
    border-bottom: 1px solid #e8e3db;
/* ── Items secundarios ── */
.item {
   display: flex;
    gap: 1.5rem;
    justify-content: space-between;
   align-items: flex-start;
    gap: 1rem;
    padding: 1rem 0;
    border-bottom: 1px solid #f5f5f5;
}
.paper-index {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: #e0dbd3;
    line-height: 1;
    min-width: 2rem;
    text-align: right;
.item-body { flex: 1; }
.item-source {
    font-size: 0.62rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #ccc;
    margin-bottom: 0.35rem;
}
.item-title {
    font-size: 0.875rem;
    font-weight: 500;
    color: #111;
    line-height: 1.4;
    letter-spacing: -0.01em;
    margin-bottom: 0.4rem;
}
.item-link {
    font-size: 0.62rem;
    font-weight: 500;
    color: #aaa !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    text-decoration: none !important;
}
.item-date {
    font-size: 0.62rem;
    color: #ddd;
    white-space: nowrap;
    margin-top: 0.2rem;
}
.paper-card h4 { font-family: 'Playfair Display', serif; font-size: 1.05rem; font-weight: 700; color: #1c1c1c; line-height: 1.3; margin-bottom: 0.3rem; }
.paper-card p { font-size: 0.85rem; color: #777; line-height: 1.55; }

/* Links */
a { color: #9c6b3c !important; text-decoration: none !important; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; }
a:hover { text-decoration: underline !important; }
/* ── Papers ── */
.paper {
    padding: 1.2rem 0;
    border-bottom: 1px solid #f5f5f5;
    display: grid;
    grid-template-columns: 2rem 1fr;
    gap: 0 1.25rem;
    align-items: start;
}
.paper-num {
    font-size: 0.65rem;
    font-weight: 600;
    color: #ddd;
    padding-top: 0.15rem;
}
.paper-title {
    font-size: 0.875rem;
    font-weight: 500;
    color: #111;
    line-height: 1.4;
    letter-spacing: -0.01em;
    margin-bottom: 0.35rem;
}
.paper-meta {
    font-size: 0.65rem;
    color: #bbb;
    margin-bottom: 0.35rem;
}
.paper-summary {
    font-size: 0.8rem;
    color: #888;
    line-height: 1.6;
    margin-bottom: 0.4rem;
}

/* Vacío */
.empty-state { font-size: 0.85rem; color: #bbb; font-style: italic; padding: 1.5rem 0; }
/* ── Divisor ── */
.rule { border: none; border-top: 1px solid #f0f0f0; margin: 3rem 0; }

/* Ocultar elementos Streamlit */
#MainMenu, footer, header { visibility: hidden; }
/* ── Empty state ── */
.empty { font-size: 0.8rem; color: #ccc; padding: 2rem 0; }
</style>
""", unsafe_allow_html=True)


# ─── CABECERA ─────────────────────────────────────────────
hoy = datetime.now().strftime("%A, %d de %B de %Y").capitalize()
hoy = datetime.now().strftime("%d de %B de %Y")
st.markdown(f"""
<div class="masthead">
    <div class="masthead-title">Nodo</div>
    <div class="masthead-sub">Tecnología · Economía · Ciencia</div>
    <div class="masthead-date">{hoy}</div>
<div class="nodo-header">
    <span class="nodo-wordmark">Nodo</span>
    <span class="nodo-date">{hoy}</span>
</div>
<hr class="divider-thick">
""", unsafe_allow_html=True)


# ─── HELPERS ──────────────────────────────────────────────
def fmt_fecha(fecha_str):
def fmt_fecha(s):
try:
        return datetime.fromisoformat(fecha_str.replace('Z', '+00:00')).strftime("%d/%m/%Y")
        return datetime.fromisoformat(s.replace('Z', '+00:00')).strftime("%d/%m/%Y")
except:
        return fecha_str
        return s

def obtener_noticias(query, dias_atras, dominios, cantidad=4, idioma='es'):
try:
@@ -161,20 +212,19 @@ def obtener_noticias(query, dias_atras, dominios, cantidad=4, idioma='es'):
except:
return []

def obtener_papers(query, cantidad=4):
def obtener_papers(query, cantidad=3):
try:
url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={cantidad}&sortBy=submittedDate&sortOrder=descending"
root = ET.fromstring(requests.get(url, timeout=8).content)
papers = []
for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            # Extraer solo la primera oración del abstract
            summary_full = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
            summary_short = summary_full.split('.')[0] + '.' if '.' in summary_full else summary_full[:120]
            summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
            summary = summary.split('.')[0] + '.' if '.' in summary else summary[:120]
authors = [a.find('{http://www.w3.org/2005/Atom}name').text
for a in entry.findall('{http://www.w3.org/2005/Atom}author')]
papers.append({
'title': entry.find('{http://www.w3.org/2005/Atom}title').text.strip(),
                'summary': summary_short,
                'summary': summary,
'authors': ', '.join(authors[:2]) + (' et al.' if len(authors) > 2 else ''),
'url': entry.find('{http://www.w3.org/2005/Atom}id').text,
'date': fmt_fecha(entry.find('{http://www.w3.org/2005/Atom}published').text)
@@ -183,99 +233,91 @@ def obtener_papers(query, cantidad=4):
except:
return []

def render_hero(art):
def hero(art):
fecha = fmt_fecha(art.get('publishedAt', ''))
    fuente = art['source']['name']
    desc = (art.get('description') or '')[:220]
    desc = (art.get('description') or '')[:200]
st.markdown(f"""
    <div class="hero-card">
        <div class="hero-meta"><span class="hero-source">{fuente}</span>{fecha}</div>
        <h2>{art['title']}</h2>
        <p>{desc}…</p>
        <a href="{art['url']}" target="_blank">Leer nota completa →</a>
    <div class="hero">
        <div class="hero-source">{art['source']['name']} &nbsp;·&nbsp; {fecha}</div>
        <div class="hero-title">{art['title']}</div>
        <div class="hero-desc">{desc}…</div>
        <a class="hero-link" href="{art['url']}" target="_blank">Leer →</a>
   </div>""", unsafe_allow_html=True)

def render_item(art):
def item(art):
fecha = fmt_fecha(art.get('publishedAt', ''))
    fuente = art['source']['name']
    desc = (art.get('description') or '')[:130]
st.markdown(f"""
    <div class="item-card">
        <div class="item-meta"><span class="item-source">{fuente}</span>{fecha}</div>
        <h4>{art['title']}</h4>
        <p>{desc}…</p>
        <a href="{art['url']}" target="_blank">Leer →</a>
    <div class="item">
        <div class="item-body">
            <div class="item-source">{art['source']['name']}</div>
            <div class="item-title">{art['title']}</div>
            <a class="item-link" href="{art['url']}" target="_blank">Leer →</a>
        </div>
        <div class="item-date">{fecha}</div>
   </div>""", unsafe_allow_html=True)

def render_paper(p, idx):
def paper(p, idx):
st.markdown(f"""
    <div class="paper-card">
        <div class="paper-index">{str(idx).zfill(2)}</div>
    <div class="paper">
        <div class="paper-num">{str(idx).zfill(2)}</div>
       <div>
            <div class="item-meta">{p['authors']} · {p['date']}</div>
            <h4>{p['title']}</h4>
            <p>{p['summary']}</p>
            <a href="{p['url']}" target="_blank">Ver en ArXiv →</a>
            <div class="paper-meta">{p['authors']} · {p['date']}</div>
            <div class="paper-title">{p['title']}</div>
            <div class="paper-summary">{p['summary']}</div>
            <a class="item-link" href="{p['url']}" target="_blank">Ver en ArXiv →</a>
       </div>
   </div>""", unsafe_allow_html=True)

def empty_state(msg="No se encontraron resultados en este momento."):
    st.markdown(f'<div class="empty-state">{msg}</div>', unsafe_allow_html=True)
def empty(msg="Sin resultados por el momento."):
    st.markdown(f'<div class="empty">{msg}</div>', unsafe_allow_html=True)


# ─── LAYOUT PRINCIPAL: 2 COLUMNAS ─────────────────────────
# ─── CONTENIDO ────────────────────────────────────────────
col_tech, col_arg = st.columns([3, 2], gap="large")

with col_tech:
    st.markdown('<span class="section-label">Tecnología Global</span>', unsafe_allow_html=True)
    fuentes_tech = "techcrunch.com,wired.com,arstechnica.com,venturebeat.com,technologyreview.com"
    arts_tech = obtener_noticias(
    st.markdown('<span class="sect-label">Tecnología</span>', unsafe_allow_html=True)
    arts = obtener_noticias(
"artificial intelligence OR machine learning OR startups",
        dias_atras=14, dominios=fuentes_tech, cantidad=4, idioma='en'
        dias_atras=14,
        dominios="techcrunch.com,wired.com,arstechnica.com,venturebeat.com,technologyreview.com",
        cantidad=4, idioma='en'
)
    if arts_tech:
        render_hero(arts_tech[0])
        for a in arts_tech[1:]:
            render_item(a)
    if arts:
        hero(arts[0])
        for a in arts[1:]: item(a)
else:
        empty_state("No hay noticias de tecnología disponibles.")
        empty()

with col_arg:
    st.markdown('<span class="section-label">Economía Argentina</span>', unsafe_allow_html=True)
    fuentes_ar = "lanacion.com.ar,infobae.com,cronista.com,ambito.com"
    arts_arg = obtener_noticias(
    st.markdown('<span class="sect-label">Argentina</span>', unsafe_allow_html=True)
    arts = obtener_noticias(
"economía OR inflación OR dólar OR política económica",
        dias_atras=7, dominios=fuentes_ar, cantidad=4, idioma='es'
        dias_atras=7,
        dominios="lanacion.com.ar,infobae.com,cronista.com,ambito.com",
        cantidad=4, idioma='es'
)
    if arts_arg:
        render_hero(arts_arg[0])
        for a in arts_arg[1:]:
            render_item(a)
    if arts:
        hero(arts[0])
        for a in arts[1:]: item(a)
else:
        empty_state("No hay noticias argentinas disponibles.")
        empty()

st.markdown('<hr class="divider-thin">', unsafe_allow_html=True)
st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ─── PAPERS ───────────────────────────────────────────────
st.markdown('<span class="section-label">Ciencia Reciente</span>', unsafe_allow_html=True)
st.markdown('<span class="sect-label">Ciencia</span>', unsafe_allow_html=True)

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
papers_data = []
for q in ["large language models", "economic complexity", "network science social systems"]:
    papers_data += obtener_papers(q, cantidad=2)
    if len(papers_data) >= 6: break
papers_data = papers_data[:6]

if papers:
    p_col1, p_col2 = st.columns(2, gap="large")
    for i, p in enumerate(papers):
        with (p_col1 if i % 2 == 0 else p_col2):
            render_paper(p, i + 1)
if papers_data:
    pc1, pc2 = st.columns(2, gap="large")
    for i, p in enumerate(papers_data):
        with (pc1 if i % 2 == 0 else pc2):
            paper(p, i + 1)
else:
    empty_state("No se pudieron cargar papers en este momento.")
    empty()
