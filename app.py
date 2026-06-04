import streamlit as st
from utils.pdf_extractor import pdf_file_c
from utils.chunk_splitter import chunks_split
from utils.embedding import embeddings
from utils.pinecone import store_embeddings, search

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mini Search Engine",
    page_icon="🔍",
    layout="centered"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Hide default streamlit elements ── */
#MainMenu, footer, header {visibility: hidden;}

/* ── Background ── */
.stApp {
    background: #0a0a0f;
}

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem 0;
}
.hero h1 {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -1px;
    margin-bottom: 0.4rem;
}
.hero p {
    color: #6b7280;
    font-size: 1rem;
    font-weight: 300;
    letter-spacing: 0.5px;
}
.accent {
    color: #7c6cfc;
}

/* ── Upload section ── */
.upload-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #7c6cfc;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

/* ── Search bar ── */
.stTextInput > div > div > input {
    background: #13131a !important;
    border: 1px solid #2a2a3a !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.8rem 1.2rem !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: #7c6cfc !important;
    box-shadow: 0 0 0 3px rgba(124,108,252,0.15) !important;
}

/* ── Search button ── */
.stButton > button {
    background: linear-gradient(135deg, #7c6cfc, #5b4ef5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    transition: opacity 0.2s, transform 0.1s !important;
    width: 100%;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}

/* ── Result card ── */
.result-card {
    background: #13131a;
    border: 1px solid #1e1e2e;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.result-card:hover {
    border-color: #7c6cfc;
}
.result-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.8rem;
}
.result-source {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #7c6cfc;
    background: rgba(124,108,252,0.1);
    padding: 0.25rem 0.7rem;
    border-radius: 20px;
    letter-spacing: 0.5px;
}
.result-score {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #4ade80;
    background: rgba(74,222,128,0.1);
    padding: 0.25rem 0.7rem;
    border-radius: 20px;
}
.result-text {
    color: #9ca3af;
    font-size: 0.9rem;
    line-height: 1.7;
    font-weight: 300;
}

/* ── Success message ── */
.stSuccess {
    background: rgba(74,222,128,0.08) !important;
    border: 1px solid rgba(74,222,128,0.2) !important;
    border-radius: 10px !important;
    color: #4ade80 !important;
}

/* ── Divider ── */
.custom-divider {
    border: none;
    border-top: 1px solid #1e1e2e;
    margin: 2rem 0;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: #374151;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 1px;
    padding: 1rem 0 2rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🔍 Mini <span class="accent">Vector</span> Search</h1>
    <p>Semantic search across your PDF documents</p>
</div>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "processed" not in st.session_state:
    st.session_state.processed = False

# ── Upload section ─────────────────────────────────────────────────────────────
st.markdown('<div class="upload-label">📄 Upload Documents</div>', unsafe_allow_html=True)
uploaded_files = st.file_uploader(
    "Drop up to 5 PDF files here",
    accept_multiple_files=True,
    type=["pdf"]
)

if uploaded_files and not st.session_state.processed:
    with st.spinner("Processing documents..."):
        for file in uploaded_files:
            text = pdf_file_c(file)
            chunks = chunks_split(text)
            embeds = embeddings(chunks)
            store_embeddings(chunks, embeds, file.name)
            st.success(f"✓  {file.name}")
    st.session_state.processed = True

# ── Search section ─────────────────────────────────────────────────────────────
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
st.markdown('<div class="upload-label">🔎 Search</div>', unsafe_allow_html=True)

query = st.text_input("", placeholder="Ask anything about your documents...")

if st.button("SEARCH"):
    if query:
        with st.spinner("Searching..."):
            query_embedding = embeddings(query).tolist()
            results = search(query_embedding)

        if results.matches:
            st.markdown(f"<p style='color:#6b7280; font-size:0.85rem; margin-bottom:1rem;'>Found {len(results.matches)} results</p>", unsafe_allow_html=True)
            for match in results.matches:
                score_pct = round(match.score * 100, 1)
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-meta">
                        <span class="result-source">📄 {match.metadata['source']}</span>
                        <span class="result-score">⚡ {score_pct}% match</span>
                    </div>
                    <div class="result-text">{match.metadata['text']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No results found. Try a different query.")
    else:
        st.warning("Please enter a search query.")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
st.markdown('<div class="footer">BUILT BY HAFIZ RAYYAN &nbsp;·&nbsp; MINI VECTOR SEARCH ENGINE</div>', unsafe_allow_html=True)