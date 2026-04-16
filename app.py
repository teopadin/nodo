st.markdown("""
    <style>
    /* Fondo de la página ligeramente gris para que resalten las tarjetas */
    .stApp { background-color: #f8f9fa; color: #1a1a1a; }
    
    /* Contenedor principal centrado y con ancho controlado */
    .main .block-container { max-width: 900px; padding-top: 3rem; }

    h1 { font-size: 2.8rem; font-weight: 800; color: #000; margin-bottom: 2rem; }
    h2 { font-size: 1.1rem; font-weight: 700; color: #555 !important; text-transform: uppercase; letter-spacing: 0.12em; margin-top: 3rem; margin-bottom: 1.5rem; }
    
    /* Tarjetas con relieve y bordes claros */
    .card {
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #e1e4e8;
        margin-bottom: 1.5rem;
        background-color: #ffffff; /* Blanco puro sobre fondo gris */
        box-shadow: 0 2px 4px rgba(0,0,0,0.02); /* Sombra casi imperceptible pero efectiva */
    }
    
    h3 { font-size: 1.4rem; font-weight: 700; color: #1a1a1a !important; margin-bottom: 0.8rem; line-height: 1.25; }
    .metadata { font-size: 0.8rem; color: #666 !important; margin-bottom: 1rem; font-family: monospace; }
    .source-tag { color: #0066cc; font-weight: 700; text-transform: uppercase; }
    
    .stMarkdown p { font-size: 1.05rem; color: #333 !important; line-height: 1.6; }
    
    a { color: #0066cc !important; text-decoration: none; font-weight: 600; font-size: 0.95rem; }
    a:hover { text-decoration: underline; }
    
    hr { border: 0; margin: 2rem 0; }
    </style>
    """, unsafe_allow_html=True)
