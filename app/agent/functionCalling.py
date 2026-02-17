from google import genai
import streamlit as st
import os
from tools.monitoring_tool import get_system_metrics
from tools.retrieval_tool import search_knowledge_base
from tenacity import retry, stop_after_attempt, wait_random_exponential
api_key = st.secrets["GEMENI_API_KEY"]

client = genai.Client(api_key=api_key)
GEN_MODEL = "gemini-2.0-flash-lite"

retrieved_sources = []
#builds historical context for the ai response
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

# tool defination to get live metrics
def get_sys_metr():
    """Retrieves any current system metrics."""
    print(f"\n[System: Executing get_sys_metr for...]")
    metrx = get_system_metrics()
    print(metrx)

    return {
        "cpu-usage": metrx["cpu_usage"],
        "memory-usage": metrx["memory_usage"],
        "active_users": metrx["active_users"]
    }

def toolRAG(prmpt: str, top_k, temperature: float = 0.2):

    #internal tool for searching vectore store so that top_k can be passed
    def search(query: str):
        """Retrievs information about incidents or issues or historical reports."""
        print(f"\n[System: Executing search for {query}...]")
        #we tell python we want to affect the global variable outside
        global retrieved_sources
        ans = search_knowledge_base(query, top_k)
        
        retrieved_sources = [
            f"{r['text'][:8]} | Rank {r['rank']} | Distance {r['distance']:.4f}" 
            for r in ans
        ]

        context = build_context(ans)

        return context if context else "never experienced"

    #default prompt for the ai context
    system_prompt = """
    You are a cute and charming assistant 🌸. 
    You can get live system metrics and solve issues.
    
    When you use the 'search' tool:
    1. Use the provided context to solve the user's issue step-by-step.
    2. If the tool returns 'never experienced', say exactly 'never experienced' similar problem before.
    3. Use dates from the context to reference past incidents.
    
    Be seamless and use emojis! ✨
    """
    # List of tools the rag can call from
    tools_list = [ get_sys_metr, search]

    # 4. Start the interaction
    # 'enable_automatic_function_calling' handles the loop for you!
    chat = client.chats.create(
        model=GEN_MODEL,
        config={
            "system_instruction": system_prompt,
            "tools": tools_list,
            "temperature": temperature
            }
    )

    user_prompt = prmpt
    print(f"User: {user_prompt}")

    #prevents system crashes, and applies retries and timeouts. can be applied but creates latency
    """         @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5))
            def safe_chat_call(prompt):
                return chat.send_message(prompt) """
    

    response = chat.send_message(user_prompt)
    answer = response.text
    print(f"Gemini: {response.text}")

    if "never experienced" in answer.lower():
        sources = ["Nothing to show here..."]
    else:
        sources = retrieved_sources

    return answer, sources
