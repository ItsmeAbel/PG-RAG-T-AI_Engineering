import streamlit as st
from main import rag_query  # adjust import

st.set_page_config(page_title="RAG Search", layout="centered")

st.title("🔍 RAG Semantic Search")
st.caption("FAISS + Embeddings + LLM")

query = st.text_input("Ask a question:")

if st.button("Search") and query.strip():
    with st.spinner("Thinking..."):
        answer = rag_query(query)

    st.markdown("### Answer")
    st.markdown(answer)
