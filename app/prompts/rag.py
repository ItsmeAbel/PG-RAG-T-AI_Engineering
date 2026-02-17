from google import genai
import streamlit as st

api_key = st.secrets["GEMENI_API_KEY"]

client = genai.Client(api_key=api_key)

GEN_MODEL = "gemini-2.5-flash"


def build_context(retrieved_chunks: list[dict]) -> str:
    """
    Build a clean context block with source numbering
    """
    context_parts = []

    for i, item in enumerate(retrieved_chunks, start=1):
        context_parts.append(
            f"[Source {i}]\n{item['text']}"
        )

    return "\n\n".join(context_parts)


def generate_rag_answer(query, retrieved_chunks, temperature):
    context = build_context(retrieved_chunks)

    prompt = f"""
    You are a cute and charming assistant that help solve issues using ONLY the provided context.
    Understand the users question, use the context to search for a solution, and provide a step-by-step solution to the asked question.
    Use dates to reference past incidents.
    If the answer is not present, say exactly "never experienced" similar problem before.

    Use appropriate emoji sometimes.
    Seemless answer.
    Context:
    {context}

    Question:
    {query}
    """

    # LLM call here (Gemini)
    response = client.models.generate_content(
        model=GEN_MODEL,
        contents=prompt,
        config={"temperature": temperature}
    )

    return response.text

