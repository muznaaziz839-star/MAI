import streamlit as st
from calculus import chapters as calculus
from linear_algebra import linear_algebra
from topics_content import generate_topic_prompt
from sidebar import render_sidebar
from groq_service import ask_groq
from mcq_generator import render_mcq_generator
from plotly_graphs import plot_graph

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="MAI - Mathematical Artificial Intelligence",
    layout="wide",
    page_icon="📘"
)

# ===================== SIDEBAR =====================
mode = render_sidebar()

# ===================== SESSION STATE =====================
if "lecture" not in st.session_state:
    st.session_state.lecture = None

if "mcqs" not in st.session_state:
    st.session_state.mcqs = []

if "last_topic" not in st.session_state:
    st.session_state.last_topic = None

# ===================== UI =====================
st.markdown("""
<style>

.stApp{
    background-color:#F6F8FB;
}

[data-testid="stSidebar"]{
    background-color:#FFFFFF;
    border-right:1px solid #E5E7EB;
}

.stButton > button{
    background-color:#2563EB;
    color:white;
    border:none;
    border-radius:10px;
    height:44px;
    font-weight:600;
}

.stButton > button:hover{
    background-color:#1D4ED8;
}

.card{
    background:white;
    padding:18px;
    border-radius:12px;
    border:1px solid #E5E7EB;
}

footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# ===================== HEADER =====================
st.title("📘 MAI - Mathematical Artificial Intelligence")

# ===================== COURSE =====================
course = st.selectbox(
    "Select Course",
    ["Calculus", "Abstract Algebra"]
)

if course == "Calculus":
    syllabus = calculus
else:
    syllabus = linear_algebra

# ===================== GRAPH MAPPING =====================
TOPIC_GRAPHS = {
    "Limits": "x",
    "Functions": "x**2",
    "Quadratic Functions": "x**2",
    "Derivatives": "x**3",
    "Integrals": "x**2",
    "Trigonometric Functions": "sin(x)",
    "Exponential Functions": "exp(x)",
    "Logarithmic Functions": "log(x)"
}

# ===================== COURSE CONTENT =====================
st.markdown("### Select Course Content")

col1, col2 = st.columns(2)

with col1:
    selected_chapter = st.selectbox(
        "Chapter",
        list(syllabus.keys())
    )

with col2:
    selected_topic = st.selectbox(
        "Topic",
        syllabus[selected_chapter]
    )

graph_expr = TOPIC_GRAPHS.get(selected_topic)

# ===================== CLEAR OLD LECTURE =====================
if st.session_state.last_topic != selected_topic:
    st.session_state.lecture = None
    st.session_state.last_topic = selected_topic

# =========================================================
# LECTURE MODE
# =========================================================
if mode == "Lecture Mode":

    st.markdown("## 📘 Lecture Generator")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    if st.button("Generate Lecture"):

        with st.spinner("Generating Lecture..."):

            prompt = generate_topic_prompt(
                course,
                selected_topic
            )

            response = ask_groq(prompt)

            st.session_state.lecture = response

            st.rerun()

    # ================= DISPLAY LECTURE =================
    if st.session_state.lecture:

        st.markdown(st.session_state.lecture)

        # ================= TOPIC GRAPH =================
        if graph_expr:

            st.markdown("### 📊 Topic Visualization")

            fig = plot_graph(graph_expr)

            st.plotly_chart(
                fig,
                use_container_width=True,
                key=f"graph_{selected_topic}"
            )

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ASSESSMENT MODE
# =========================================================
elif mode == "Assessment Generator":

    render_mcq_generator(selected_topic)

# =========================================================
# SOLVE PROBLEM MODE
# =========================================================
elif mode == "Solve Problem":

    st.markdown("## Solve Problem")

    problem = st.text_area(
        "Enter your mathematics problem"
    )

    if st.button("Solve"):

        if problem.strip():

            with st.spinner("Solving..."):

                prompt = f"""
Solve this mathematics problem step by step.

Problem:
{problem}

Show formulas and final answer.
"""

                response = ask_groq(prompt)

                st.markdown(response)

        else:
            st.warning("Please enter a problem.")

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.markdown(
    "<p style='text-align:center;color:#9CA3AF;'>MAI © 2026 | AI Learning Platform</p>",
    unsafe_allow_html=True
)