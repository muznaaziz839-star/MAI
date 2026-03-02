from groq import Groq
import streamlit as st
import os
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

# Priority: Streamlit secrets → .env → system env
api_key = (
    st.secrets.get("GROQ_API_KEY", None)
    or os.getenv("GROQ_API_KEY")
)

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Set it in Streamlit secrets or .env")

client = Groq(api_key=api_key)

MODEL_NAME = "llama-3.3-70b-versatile"

def ask_groq(prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"