from google import genai

client = genai.Client()

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
    context = "\n\n".join(
        f"[Source {i+1}]\n{r['text']}"
        for i, r in enumerate(retrieved_chunks)
    )

    prompt = f"""
    You are a cute and charming assistant answering questions using ONLY the provided context.
    Answer the question using ONLY the context below.
    If the answer is not present, say you don't know.
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

