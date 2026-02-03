import streamlit as st
from retrieval.rag_answerer import rag_answer

# ---------- Page Config ----------
st.set_page_config(
    page_title="Incident Intelligence RAG",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Custom CSS ----------
st.markdown(
    """
    <style>
    .main {
        padding: 2rem;
    }
    .block-container {
        padding-top: 1.5rem;
    }
    .answer-box {
        background-color: #0f172a;
        border-radius: 12px;
        padding: 1.2rem;
        color: #e5e7eb;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    .source-box {
        background-color: #020617;
        border-left: 4px solid #38bdf8;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        margin-bottom: 0.6rem;
        font-size: 0.9rem;
        color: #cbd5f5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    top_k = st.slider("Top-K Chunks", 1, 8, 3)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.2)
    st.markdown("---")
    st.markdown(
        """
        **About**  
        This system uses:
        - Gemini embeddings  
        - FAISS semantic search  
        - Retrieval-Augmented Generation (RAG)
            Contact abel97.ag@gmail.com for any inquires.   
        """
    )

# ---------- Header ----------
st.markdown("## 🧠 Incident Intelligence Assistant")
st.markdown(
    "Ask questions about historical incident reports and receive grounded, source-based answers."
)

# ---------- Query Input ----------
query = st.text_input(
    "🔎 Ask a question",
    placeholder="e.g. What incidents were related to SSL certificate issues?",
)

run = st.button("Run Search", use_container_width=True)

# ---------- Run RAG ----------
if run and query.strip():
    with st.spinner("Retrieving and reasoning..."):
        answer, sources = rag_answer(
            query=query,
            top_k=top_k,
            temperature=temperature,
        )

    # ---------- Answer ----------
    st.markdown("### ✅ Answer")
    st.markdown(f"<div class='answer-box'>{answer}</div>", unsafe_allow_html=True)

    # ---------- Sources ----------
    st.markdown("### 📚 Sources")
    for i, src in enumerate(sources, start=1):
        st.markdown(
            f"""
            <div class='source-box'>
            <b>Source {i}</b><br/>
            {src}
            </div>
            """,
            unsafe_allow_html=True,
        )

elif run:
    st.warning("Please enter a question.")
