# src/chains/ai_suggester.py
import os
import re
import streamlit as st
from src.core.fallback_data import get_fallback_spots, get_fallback_description

# ----------------- Initialize Variables -----------------
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
llm = None
spot_prompt = None
desc_prompt = None

def init_llm(api_key: str = None, model_name: str = None):
    """
    Initializes the Groq LLM with the provided API key (or environment key) and model.
    Sets the global llm, spot_prompt, and desc_prompt variables.
    Imports LangChain modules lazily to optimize application startup time.
    """
    global llm, spot_prompt, desc_prompt
    key = api_key or GROQ_API_KEY
    if not key:
        llm = None
        return
        
    try:
        from langchain_groq import ChatGroq
        from langchain_core.prompts import ChatPromptTemplate
        
        selected_model = model_name or st.session_state.get("llm_model", "llama-3.3-70b-versatile")
        
        llm = ChatGroq(
            groq_api_key=key,
            model_name=selected_model,
            temperature=0.3,
            top_p=0.9,
            max_tokens=800
        )

        # Spot list prompt
        spot_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "List top 10 famous tourist places to visit in {city}. "
             "Give exact spot names people visit, no generic names. "
             "Output as comma separated list only."),
            ("human", "Give the list now.")
        ])

        # Spot description prompt
        desc_prompt = ChatPromptTemplate.from_messages([
            ("system",
              "Provide a short, clear description why {spot} is famous in {city}. "
              "Keep it 1-2 lines for tourists.")
        ])
    except Exception:
        llm = None

# Initialize on module load if key exists
if GROQ_API_KEY:
    init_llm(GROQ_API_KEY)


def get_llm_instance():
    """
    Returns the current LLM instance. Safe helper for dynamic key loading.
    """
    global llm
    return llm


# ----------------- Helpers -----------------
def _parse_spots(text: str):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    cleaned = []
    for l in lines:
        cleaned.extend(re.split(r'[,;\n]+', re.sub(r'^[\-\d\.\)\s]+', '', l)))
    return [c.strip() for c in cleaned if c.strip()]


# ----------------- Main Functions -----------------
@st.cache_data(ttl=86400)
def suggest_spots_for_city(city: str):
    """
    Suggests famous spots. Falls back to a local database if LLM is unavailable.
    """
    if not city:
        return []
        
    global llm, spot_prompt
    if not llm or not spot_prompt:
        # Fall back to local DB
        fallback = get_fallback_spots(city)
        if fallback:
            return fallback
        return []

    try:
        messages = spot_prompt.format_messages(city=city)
        resp = llm.invoke(messages)
        text = resp.content if hasattr(resp, "content") else str(resp)
        spots = _parse_spots(text)[:10]
        if not spots:
            # Try fallback database if parser returned nothing
            return get_fallback_spots(city)
        return spots
    except Exception:
        # Fall back to local DB on error
        return get_fallback_spots(city)


@st.cache_data(ttl=86400)
def get_spot_description(city: str, spot: str):
    """
    Retrieves spot description. Falls back to local database if LLM is unavailable.
    """
    if not city or not spot:
        return "Popular spot worth visiting."
        
    global llm, desc_prompt
    if not llm or not desc_prompt:
        return get_fallback_description(spot)

    try:
        messages = desc_prompt.format_messages(city=city, spot=spot)
        resp = llm.invoke(messages)
        text = resp.content if hasattr(resp, "content") else str(resp)
        return text.strip()
    except Exception:
        return get_fallback_description(spot)
