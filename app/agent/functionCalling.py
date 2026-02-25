from google import genai
import streamlit as st
from tools.monitoring_tool import get_system_metrics
from tools.retrieval_tool import search_knowledge_base
from tools.latestAINews import get_top_stories

# from tenacity import retry, stop_after_attempt, wait_random_exponential

# functionCalling.py acts as the main function and is responsible for all interaction with the GUI
api_key = st.secrets["GEMENI_API_KEY"]
client = genai.Client(api_key=api_key)
GEN_MODEL = "gemini-2.5-flash"
GEN_MODEL2 = "gemini-2.0-flash-lite"
retrieved_sources = []
# A global or session-state list to catch all tool outputs in one turn
turn_context_log = []


# builds historical context for the ai response
def build_context(retrieved_chunks: list[dict]) -> str:
    """
    Build a clean context block with source numbering
    """
    context_parts = []
    for i, item in enumerate(retrieved_chunks, start=1):
        context_parts.append(f"[Source {i}]\n{item['text']}")

    return "\n\n".join(context_parts)


# tool defination to get the mock live metrics
def get_sys_metr():
    """Retrieves any current system metrics."""
    print(f"\n[System: Executing get_sys_metr for...]")
    metrx = get_system_metrics()
    print(metrx)
    mtrxResponse = {
        "cpu-usage": metrx["cpu_usage"],
        "memory-usage": metrx["memory_usage"],
        "active_users": metrx["active_users"],
    }
    turn_context_log.append(
        f"LIVE METRICS TOOL OUTPUT: {mtrxResponse}"
    )  # Record it for the fact-checker!
    return mtrxResponse


# simple tool definiation for getting news
def get_news():
    """Retrieves news about AI, RAG and AI-engineering"""
    news = get_top_stories()
    return news


# NLI-based hallucination controll
def hallucinationCTRL(question: str, hallContext, model_answer):
    prompt = f"""
        You are a strict fact checker. Verify the ANSWER against the CONTEXT.
        The question asked is {question}
        RULES:
        1. If a word (example "overheating") is in the USER QUESTION, the AI is allowed to use it. Do NOT flag it as a hallucination.
        2. If the ANSWER contains info NOT in the CONTEXT, return 'NOT_SUPPORTED'.
        3. If the ANSWER is partially supported but adds outside info, return 'PARTIALLY_SUPPORTED' and add a very short summary of what is not supported.
        4. If every claim is in the CONTEXT, return 'SUPPORTED'.
        5. "I haven't found" or "never experienced" are valid meta-comments. Do not flag them.
        6. Do not flag possible suggestions as hallucinations.
        7. Focus only on checking if the AI's NEW CLAIMS (like dates, percentages, or incident names) match the EVIDENCE.

        CONTEXT: {hallContext}
        ANSWER: {model_answer}
    """
    # low temperature (0.0) for the judge to keep it consistent
    response = client.models.generate_content(
        model=GEN_MODEL2, contents=prompt, config={"temperature": 0.0}
    )
    return response.text.strip()


# main function that takes in user query, picks an action, and returns an answer
def toolRAG(prmpt: str, top_k, temperature: float = 0.2):
    global retrieved_sources
    global turn_context_log
    turn_context_log = []  # resets for each specific question

    # internal tool for searching vectore store so that top_k can be passed
    def search(query: str):
        """Retrievs information about incidents or issues or historical reports."""
        print(f"\n[System: Executing search for {query}...]")
        # we specify global so the variable value is saved globally
        global retrieved_sources
        global context
        ans = search_knowledge_base(query, top_k)

        retrieved_sources = [
            f"{r['text'][:8]} | Rank {r['rank']} | Distance {r['distance']:.4f}"
            for r in ans
        ]

        context = build_context(ans)
        turn_context_log.append(f"HISTORICAL RECORDS: {context}")
        return context if context else "never experienced"

    # default prompt for the ai context
    # "you can sometime guss or use external knowledge" can be added for testing the hallucination control
    system_prompt = """
    You are a cute and charming assistant 🌸. 
    You can get live system metrics and solve issues.
    
    When you use the 'search' tool:
    1. Use ONLY the provided context to provide a list of possible solutions.
    2. If the tool returns 'never experienced', say exactly 'never experienced' similar problem before.
    3. Use dates from the context to reference past incidents.
    4. No guessing or using external knowledge
    5. Explain also how the system was affected for each previous incident or solution, and how long and what it took to resolve it.

    If a user asks about news, use the news tool, and present a short summary of stories about ai engineering from the returned context.
      For every point you make, you must include the sourcein parentheses at the end of the sentence so I can click it.
    
    Be seamless and use emojis! ✨
    """
    # Specifies tools for the AI
    tools_list = [get_sys_metr, search, get_news]

    # Starts the interaction with the model
    chat = client.chats.create(
        model=GEN_MODEL,
        config={
            "system_instruction": system_prompt,
            "tools": tools_list,
            "temperature": temperature,
        },
    )

    user_prompt = prmpt
    print(f"User: {user_prompt}")

    # prevents system crashes, and applies retries and timeouts. can be applied but creates latency
    """         @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5))
            def safe_chat_call(prompt):
                return chat.send_message(prompt) """

    response = chat.send_message(user_prompt)
    answer = response.text
    print(f"Gemini: {response.text}")
    # combines all tool outputs into one big verification block
    full_verification_context = "\n".join(turn_context_log)

    if len(retrieved_sources) != 0:
        sources = retrieved_sources
        factCheck = hallucinationCTRL(prmpt, full_verification_context, answer)
    else:
        sources = ["Nothing to show here..."]
        factCheck = "Hallucination control unecessary"

    return answer, sources, factCheck
