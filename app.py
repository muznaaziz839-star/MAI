import streamlit as st
from calculus import chapters as calculus
from linear_algebra import linear_algebra
from calculus import chapters
from topics_content import generate_topic_prompt
from sidebar import render_sidebar
from groq_service import ask_groq
from mcq_generator import render_mcq_generator

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="MAI -Mathematical Artificial Intelligence",
    layout="wide",
    page_icon=""
)

# ===================== SAAS STYLE UI =====================
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #F6F8FB;
    font-family: 'Arial';
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0F172A;
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: #E5E7EB;
}

/* Buttons */
.stButton > button {
    background-color: #2563EB;
    color: white;
    border-radius: 10px;
    height: 44px;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    background-color: #1D4ED8;
}

/* Cards */
.card {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #E5E7EB;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.04);
}

/* Titles */
h1, h2, h3 {
    color: #111827;
}

/* Remove clutter */
footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# ===================== SIDEBAR =====================
mode = render_sidebar()

# ===================== SESSION =====================
if "lecture" not in st.session_state:
    st.session_state.lecture = None

if "mcqs" not in st.session_state:
    st.session_state.mcqs = []

# ===================== HEADER (SAAS DASHBOARD STYLE) =====================
st.markdown("""
<style>

/* ================= MAIN BACKGROUND ================= */
.stApp {
    background-color: #F6F8FB;
    font-family: 'Arial';
}

/* ================= SIDEBAR (LIGHT THEME) ================= */
[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E5E7EB;
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: #111827;
}

/* ================= BUTTONS (LIGHT SAAS STYLE) ================= */
.stButton > button {
    background-color: #2563EB;
    color: white;
    border-radius: 10px;
    height: 44px;
    font-weight: 600;
    border: none;
    transition: 0.2s ease;
}

/* Hover effect */
.stButton > button:hover {
    background-color: #1D4ED8;
    transform: scale(1.01);
}

/* ================= SELECT BOX ================= */
div[data-baseweb="select"] {
    background-color: white;
    border-radius: 8px;
}

/* ================= CARD STYLE ================= */
.card {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #E5E7EB;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.04);
}

/* ================= HEADINGS ================= */
h1, h2, h3 {
    color: #111827;
}

/* ================= REMOVE FOOTER ================= */
footer {visibility: hidden;}

/* ================= SIDEBAR RADIO BUTTON CLEAN ================= */
[data-testid="stSidebar"] label {
    font-weight: 500;
}

</style>
""", unsafe_allow_html=True)
# ===================== COURSE SELECTION =====================
st.markdown("### **Select Course**")

course = st.selectbox(
    "",
    ["Calculus", "Linear Algebra"]
)

if course == "Calculus":
    syllabus = calculus
else:
    syllabus = linear_algebra

# ===================== MODE TITLE =====================
st.markdown("### Select Course Content")

# ===================== COURSE CONTENT =====================
col1, col2 = st.columns(2)

with col1:
    selected_chapter = st.selectbox("Chapter", list(syllabus.keys()))

with col2:
    selected_topic = st.selectbox("Topic", syllabus[selected_chapter])

# =========================================================
# 📘 LECTURE MODE
# =========================================================
if mode == "Lecture Mode":

    st.markdown("## 📘 Lecture Generator")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    if st.button("Generate Lecture"):

        with st.spinner("Generating AI lecture..."):

            prompt = generate_topic_prompt(course, selected_topic)
            response = ask_groq(prompt)

            st.session_state.lecture = response

    if st.session_state.lecture:
        st.markdown(st.session_state.lecture)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# 📝 ASSESSMENT MODE
# =========================================================
elif mode == "Assessment Generator":


    with st.container():
        render_mcq_generator(selected_topic)

# ====================SOLVE PROBLEM========================#
elif mode == "Solve Problems":

    st.markdown("## Solve Problems")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    problem = st.text_area("Enter your problem here")

    if st.button("Solve Problem"):

        if problem.strip():
            with st.spinner("Solving..."):
                prompt = f"Solve this mathematical problem step by step:\n\n{problem}"
                response = ask_groq(prompt)
                st.markdown(response)

        else:
            st.warning("Please enter a problem first.")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#9CA3AF;'>MAI © 2026 | AI Learning Platform</p>",
    unsafe_allow_html=True
)