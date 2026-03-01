import streamlit as st

# ========================= IMPORTS =========================
from data.calculus import chapters
from data.topics_content import generate_topic_prompt
from components.content_renderer import render_content
from components.sidebar import render_sidebar
from services.groq_service import ask_groq

# ========================= PAGE CONFIG =========================
st.set_page_config(page_title="MAI — Mathematical AI", layout="wide")

# ========================= HEADER =========================
st.title("📘 MAI — Mathematical Artificial Intelligence")
st.write("AI-powered assistant for learning Calculus.")

# ========================= SIDEBAR =========================
render_sidebar()

# ========================= COURSE =========================
course = "Calculus"

st.header("📚 Select Course Content")
st.write(f"### Course: {course}")

# ========================= CHAPTER & TOPIC =========================
selected_chapter = st.selectbox(
    "Select Chapter",
    list(chapters.keys())
)

selected_topic = st.selectbox(
    "Select Topic",
    chapters[selected_chapter]
)
#=====Lecture======
if st.button("Generate Lecture"):

    with st.spinner("Generating lecture..."):

        prompt = generate_topic_prompt(selected_topic)
        response = ask_groq(prompt)
        # 🔍 DEBUG OUTPUT
        st.write("RESPONSE:")
        st.write(response)
# ========================= FOOTER =========================
st.markdown("---")
st.caption("MAI © 2026 | Powered by Groq AI")