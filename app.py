import streamlit as st
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

st.set_page_config(page_title="Nodo", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

* { box-sizing: border-box; }

.stApp {
    background-color: #ffffff;
    color: #111;
    font-family: 'Inter', sans-serif;
}
.main .block-container {
    max-width: 1080px;
    padding-top: 4rem;
    padding-bottom: 6rem;
}

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
    letter-spacing: -0.01em;
    color: #111;
}
.nodo-date {
    font-size: 0.72rem;
    color: #aaa;
    font-weight: 400;
}

/* ── Etiqueta de sección ── */
.sect-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #bbb;
    margin-bottom: 1.5rem;
    display: block;
}

/* ── Hero ── */
.hero {
    padding-bottom: 2rem;
    margin-bottom: 2rem;
    border-bottom: 1px solid #f0f0f0;
}
.hero-source {
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #bbb;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-size: 1.45rem;
    font-weight: 600;
    color: #111;
    line-height: 1.35;
    letter-spacing: -0.02em;
    margin-bottom: 0.75rem;
}
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

/* ── Items secundarios ── */
.item {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem 0;
    border-bottom: 1px solid #f5f5f5;
}
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

/* ── Divisor ── */
.rule { border: none; border-top: 1px solid #f0f0f0; margin: 3rem 0; }

/* ── Empty state ── */
.empty { font-size: 0.8rem; color: #ccc; padding: 2rem 0; }
</style>
""", unsafe_allow_html=True)


# ─── CABECERA ─────────────────────────────────────────────
hoy = datetime.now().strftime("%d de %B de %Y")
st.markdown(f"""
<div class="nodo-header">
    <span class="nodo-wordmark">Nodo</span>
    <span class="nodo-date">{hoy}</span>
</div>
""", unsafe_allow_html=True)


# ─── HELPERS ──────────────────────────────────────────────
def fmt_fecha(s):
    try:
        return datetime.fromisoformat(s.replace('Z', '+00:00')).strftime("%d/%m/%Y")
    except:
        return s

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

def obtener_papers(query, cantidad=3):
    try:
        url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={cantidad}&sortBy=submittedDate&sortOrder=descending"
        root = ET.fromstring(requests.get(url, timeout=8).content)
        papers = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
            summary = summary.split('.')[0] + '.' if '.' in summary else summary[:120]
            authors = [a.find('{http://www.w3.org/2005/Atom}name').text
                       for a in entry.findall('{http://www.w3.org/2005/Atom}author')]
            papers.append({
                'title': entry.find('{http://www.w3.org/2005/Atom}title').text.strip(),
                'summary': summary,
                'authors': ', '.join(authors[:2]) + (' et al.' if len(authors) > 2 else ''),
                'url': entry.find('{http://www.w3.org/2005/Atom}id').text,
                'date': fmt_fecha(entry.find('{http://www.w3.org/2005/Atom}published').text)
            })
        return papers
    except:
        return []

def hero(art):
    fecha = fmt_fecha(art.get('publishedAt', ''))
    desc = (art.get('description') or '')[:200]
    st.markdown(f"""
    <div class="hero">
        <div class="hero-source">{art['source']['name']} &nbsp;·&nbsp; {fecha}</div>
        <div class="hero-title">{art['title']}</div>
        <div class="hero-desc">{desc}…</div>
        <a class="hero-link" href="{art['url']}" target="_blank">Leer →</a>
    </div>""", unsafe_allow_html=True)

def item(art):
    fecha = fmt_fecha(art.get('publishedAt', ''))
    st.markdown(f"""
    <div class="item">
        <div class="item-body">
            <div class="item-source">{art['source']['name']}</div>
            <div class="item-title">{art['title']}</div>
            <a class="item-link" href="{art['url']}" target="_blank">Leer →</a>
        </div>
        <div class="item-date">{fecha}</div>
    </div>""", unsafe_allow_html=True)

def paper(p, idx):
    st.markdown(f"""
    <div class="paper">
        <div class="paper-num">{str(idx).zfill(2)}</div>
        <div>
            <div class="paper-meta">{p['authors']} · {p['date']}</div>
            <div class="paper-title">{p['title']}</div>
            <div class="paper-summary">{p['summary']}</div>
            <a class="item-link" href="{p['url']}" target="_blank">Ver en ArXiv →</a>
        </div>
    </div>""", unsafe_allow_html=True)

def empty(msg="Sin resultados por el momento."):
    st.markdown(f'<div class="empty">{msg}</div>', unsafe_allow_html=True)


# ─── CONTENIDO ────────────────────────────────────────────
col_tech, col_arg = st.columns([3, 2], gap="large")

with col_tech:
    st.markdown('<span class="sect-label">Tecnología</span>', unsafe_allow_html=True)
    arts = obtener_noticias(
        "artificial intelligence OR machine learning OR startups",
        dias_atras=14,
        dominios="techcrunch.com,wired.com,arstechnica.com,venturebeat.com,technologyreview.com",
        cantidad=4, idioma='en'
    )
    if arts:
        hero(arts[0])
        for a in arts[1:]: item(a)
    else:
        empty()

with col_arg:
    st.markdown('<span class="sect-label">Argentina</span>', unsafe_allow_html=True)
    arts = obtener_noticias(
        "economía OR inflación OR dólar OR política económica",
        dias_atras=7,
        dominios="lanacion.com.ar,infobae.com,cronista.com,ambito.com",
        cantidad=4, idioma='es'
    )
    if arts:
        hero(arts[0])
        for a in arts[1:]: item(a)
    else:
        empty()

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ─── PAPERS ───────────────────────────────────────────────
st.markdown('<span class="sect-label">Ciencia</span>', unsafe_allow_html=True)

papers_data = []
for q in ["large language models", "economic complexity", "network science social systems"]:
    papers_data += obtener_papers(q, cantidad=2)
    if len(papers_data) >= 6: break
papers_data = papers_data[:6]

if papers_data:
    pc1, pc2 = st.columns(2, gap="large")
    for i, p in enumerate(papers_data):
        with (pc1 if i % 2 == 0 else pc2):
            paper(p, i + 1)
else:
    empty()
