from groq import Groq
import streamlit as st

# ✅ Load API key from secrets.toml
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def ask_groq(prompt):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ working model
            messages=[
                {"role": "system", "content": "You are a helpful math tutor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"🚨 Groq Error: {str(e)}"