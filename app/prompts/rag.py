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


def generate_rag_answer(query: str, retrieved_chunks: list[dict]) -> str:
    context = build_context(retrieved_chunks)

    prompt = f"""
        You are an assistant with cute and charming personality answering questions using ONLY the provided context.

        If the answer is not in the context, say:
        "I don't have enough information to answer that."
        Add appropriate emoji sometimes

        Context:
        {context}

        Question:
        {query}

        Answer (include date of the source):
        """

    response = client.models.generate_content(
        model=GEN_MODEL,
        contents=prompt
    )

    return response.text
