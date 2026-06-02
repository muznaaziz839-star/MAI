from groq import Groq
import streamlit as st

# =========================================================
# LOAD GROQ CLIENT
# =========================================================
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# =========================================================
# SYSTEM PROMPT
# =========================================================
SYSTEM_PROMPT = """
You are MAI (Mathematical Artificial Intelligence),
an advanced AI mathematics tutor and educational assistant.

Your responsibilities include:
- Teaching Calculus and Abstract Algebra
- Solving mathematical problems step-by-step
- Explaining concepts clearly and academically
- Generating structured educational content
- Assisting students professionally

Guidelines:
- Use clean mathematical formatting
- Be concise but educational
- Structure responses with headings when appropriate
- Explain formulas before using them
- Maintain a professional academic tone
- Avoid unnecessary emojis
- Ensure mathematical correctness
- Prefer step-by-step reasoning for problem solving
- Use Markdown formatting for readability
"""

# =========================================================
# MODEL CONFIGURATION
# =========================================================
MODEL_NAME = "llama-3.1-8b-instant"

TEMPERATURE = 0.3

MAX_TOKENS = 4096

# =========================================================
# MAIN GROQ FUNCTION
# =========================================================
def ask_groq(prompt, system_prompt=SYSTEM_PROMPT):
    """
    Send prompt to Groq API and return AI response.
    """

    try:

        completion = client.chat.completions.create(

            model=MODEL_NAME,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=TEMPERATURE,

            max_tokens=MAX_TOKENS
        )

        response = completion.choices[0].message.content

        return clean_response(response)

    # =====================================================
    # ERROR HANDLING
    # =====================================================
    except Exception as error:

        return f"""
### System Error

The AI service is temporarily unavailable.

Error Details:
{str(error)}

Please try again in a moment.
"""


# =========================================================
# RESPONSE CLEANING
# =========================================================
def clean_response(text):
    """
    Clean and standardize AI responses.
    """

    if not text:
        return "No response generated."

    # Remove excessive whitespace
    text = text.strip()

    return text
