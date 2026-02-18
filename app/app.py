import streamlit as st

# from retrieval.rag_answerer import rag_answer
from agent.functionCalling import toolRAG

# ---------- Page Config ----------
st.set_page_config(
    page_title="Incident Solving RAG",
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
    st.markdown("Top-k: Number of nearst vectors to be searched")
    top_k = st.slider("Top-K Chunks", 1, 8, 3)
    st.markdown("Temprature: Affects AI creativness when presenting answers")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.2)
    st.markdown("---")
    st.markdown(
        """
        **About**  
        This system uses:
        - Gemini embeddings  
        - FAISS semantic search  
        - Retrieval-Augmented Generation (RAG)  
        """
    )
    st.markdown(
        """ 
        **Rate Limits:** 
        - Requests per dat(RPD): 20  
        - Requests per minute(RPM): 5

            Contact abel97.ag@gmail.com for any inquires. 
        """
    )


# ---------- Header ----------
st.markdown("## 🧠 Incident Solving Assistant")
st.markdown(
    "Ask a questions to this Agentic RAG system. Questions can be about an encountred issue which the AI uses our historical incident reports to find and present grounded, source-based solutions. The system can also present live metrics on system usage\n\n"
    " ℹ️ Example queries: RAG - 'We're having database issues'. Metrics - 'how are out systems currently?'. Both/Agentic - 'we're having cpu overheating issue'\n\n" \
    "Fact-check is not a UI trick. It really does fact check!"
)

# ---------- Query Input ----------
query = st.text_input(
    "🔎 Ask a question",
    placeholder="e.g. We're having a database issue right now or How are our systems looking",
)

run = st.button("Run Search", use_container_width=True)

# ---------- Run RAG ----------
if (run or query) and query.strip():
    with st.spinner("Retrieving and reasoning..."):
        answer, sources, status = toolRAG(
            prmpt=query, top_k=top_k, temperature=temperature
        )

    # ---------- Answer ----------
    st.markdown("### ✅ Answer")
    st.markdown(f"<div class='answer-box'>{answer}</div>", unsafe_allow_html=True)

    # If the AI says 'never experienced', we know it's a 'SUPPORTED' negative result.
    if "never experienced" in answer.lower() and status == "PARTIALLY_SUPPORTED":
        status = "SUPPORTED"
    # Display Status with Colors
    if status == "SUPPORTED":
        st.success(f"✅ Fact-Check: {status}")
    elif "PARTIALLY_SUPPORTED" in status.upper():
        st.warning(f"⚠️ Fact-Check: {status}")
    elif "NOT_SUPPORTED" in status.upper():
        st.error(f"❌ Fact-Check: {status}")
    else:
        st.info(f"ℹ️ Fact-Check: {status}")

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
