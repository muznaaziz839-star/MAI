import streamlit as st

# ========================= IMPORTS =========================
from calculus import chapters
from topics_content import generate_topic_prompt
from content_renderer import render_content
from sidebar import render_sidebar
from groq_service import ask_groq

# ========================= PAGE CONFIG =========================
st.set_page_config(page_title="MAI — Mathematical AI", layout="wide")

# ========================= HEADER =========================
st.title("📘 MAI — Mathematical Artificial Intelligence")
st.write("AI-powered assistant for learning Calculus.")

# ========================= SIDEBAR =========================
render_sidebar()

# ========================= INIT SESSION STATE =========================
if "lecture" not in st.session_state:
    st.session_state.lecture = None

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

# ========================= GENERATE LECTURE =========================
if st.button("Generate Lecture"):

    with st.spinner("Generating lecture..."):
        prompt = generate_topic_prompt(selected_topic)
        response = ask_groq(prompt)

        if response and "🚨" not in response:
            st.session_state.lecture = response
        else:
            st.session_state.lecture = "❌ Failed to generate lecture."

# ========================= DISPLAY LECTURE =========================
if st.session_state.lecture:

    st.markdown("---")
    st.subheader(f"📖 Lecture: {selected_topic}")

    # Render formatted content
    st.markdown(st.session_state.lecture)

# ========================= FOOTER =========================
st.markdown("---")
st.caption("MAI © 2026 | Powered by Groq AI")