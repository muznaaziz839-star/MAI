import re
import streamlit as st
from sidebar import render_sidebar, is_math_question
from calculus import chapters as calculus
from linear_algebra import abstract_algebra
from topics_content import generate_topic_prompt
from sidebar import render_sidebar
from groq_service import ask_groq
from mcq_generator import render_mcq_generator
from plotly_graphs import plot_graph

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="MAI | Mathematical Artificial Intelligence",
    layout="wide",
    page_icon="📘",
    initial_sidebar_state="expanded"
)

# =========================================================
# SESSION STATE
# =========================================================
default_states = {
    "lecture": None,
    "mcqs": [],
    "last_topic": None,
    "chat_history": []
}

for key, value in default_states.items():

    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# PROFESSIONAL UI STYLING
# =========================================================
st.markdown("""
<style>

/* ================= GLOBAL ================= */

.stApp{
    background-color:#F5F7FB;
    color:#111827;
}

/* ================= SIDEBAR ================= */

[data-testid="stSidebar"]{
    background: linear-gradient(180deg, #0F172A 0%, #111827 100%);
    border-right: 1px solid #1F2937;
}

[data-testid="stSidebar"] *{
    color:white;
}

/* ================= TYPOGRAPHY ================= */

.main-title{
    font-size:42px;
    font-weight:700;
    color:#111827;
    margin-bottom:5px;
}

.sub-title{
    font-size:18px;
    color:#6B7280;
    margin-bottom:25px;
}

/* ================= CARDS ================= */

.main-card{
    background:white;
    border-radius:18px;
    padding:28px;
    border:1px solid #E5E7EB;
    box-shadow:0 2px 10px rgba(0,0,0,0.04);
    margin-bottom:24px;
}

.section-title{
    font-size:24px;
    font-weight:600;
    margin-bottom:18px;
    color:#111827;
}

/* ================= BUTTONS ================= */

.stButton > button{
    width:100%;
    background: linear-gradient(90deg,#2563EB,#1D4ED8);
    color:white;
    border:none;
    border-radius:12px;
    height:48px;
    font-size:15px;
    font-weight:600;
}

.stButton > button:hover{
    background: linear-gradient(90deg,#1D4ED8,#1E40AF);
}

/* ================= INPUTS ================= */

.stTextArea textarea,
.stTextInput input,
.stSelectbox div[data-baseweb="select"]{
    border-radius:12px !important;
}

/* ================= CHAT ================= */

.chat-box{
    background:#FFFFFF;
    padding:18px;
    border-radius:14px;
    border:1px solid #E5E7EB;
    margin-bottom:16px;
}

/* ================= FOOTER ================= */

footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
mode = render_sidebar()

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="main-title">
Mathematical Artificial Intelligence
</div>

<div class="sub-title">
AI-Powered Interactive Learning Platform for Calculus and Abstract Algebra
</div>
""", unsafe_allow_html=True)

# =========================================================
# COURSE SELECTION
# =========================================================
course_col1, course_col2 = st.columns(2)

with course_col1:

    course = st.selectbox(
        "Select Course",
        ["Calculus", "Abstract Algebra"]
    )

if course == "Calculus":
    syllabus = calculus
else:
    syllabus = abstract_algebra

with course_col2:

    selected_chapter = st.selectbox(
        "Select Chapter",
        list(syllabus.keys())
    )

selected_topic = st.selectbox(
    "Select Topic",
    syllabus[selected_chapter]
)

# =========================================================
# RESET LECTURE
# =========================================================
if st.session_state.last_topic != selected_topic:

    st.session_state.lecture = None
    st.session_state.last_topic = selected_topic

# =========================================================
# GRAPH DETECTION
# =========================================================
GRAPH_PATTERNS = [

    r"x\^?\*?\*?\d+",
    r"sin\(x\)",
    r"cos\(x\)",
    r"tan\(x\)",
    r"log\(x\)",
    r"exp\(x\)",
    r"\(x.*\)",
    r"x\s*[\+\-\*/]\s*\d+"
]


# =========================================================
# EXTRACT GRAPHABLE EXPRESSION
# =========================================================
def extract_expression(text):
    """
    Extract graphable mathematical expression
    from text.
    """

    text = text.lower()

    # Remove spaces
    cleaned = text.replace(" ", "")

    for pattern in GRAPH_PATTERNS:

        match = re.search(pattern, cleaned)

        if match:
            return match.group(0)

    return None


# =========================================================
# RENDER GRAPH
# =========================================================
def render_graph(expression, key_name):
    """
    Render Plotly graph safely.
    """

    if expression:

        try:

            st.markdown("### Mathematical Visualization")

            fig = plot_graph(expression)

            st.plotly_chart(
                fig,
                use_container_width=True,
                key=f"graph_{key_name}"
            )

        except Exception:
            pass


# =========================================================
# LECTURE GENERATOR
# =========================================================
if mode == "Lecture Generator":

    st.markdown(
        '<div class="main-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">'
        'Lecture Generator'
        '</div>',
        unsafe_allow_html=True
    )

    if st.button("Generate AI Lecture"):

        with st.spinner(
            "Generating lecture..."
        ):

            prompt = generate_topic_prompt(
                course,
                selected_topic
            )

            response = ask_groq(prompt)

            st.session_state.lecture = response

            st.rerun()

    # =====================================================
    # DISPLAY LECTURE
    # =====================================================
    if st.session_state.lecture:

        st.markdown(
            st.session_state.lecture
        )

        # =================================================
        # AUTO GRAPH
        # =================================================
        detected_expr = extract_expression(
            selected_topic
        )

        if detected_expr:
            render_graph(
                detected_expr,
                selected_topic
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

# =========================================================
# PROBLEM SOLVER
# =========================================================
elif mode == "Problem Solver":

    st.markdown(
        '<div class="main-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">'
        'Problem Solver'
        '</div>',
        unsafe_allow_html=True
    )

    problem = st.text_area(
        "Enter a mathematical problem",
        height=180,
        placeholder="Example: Solve x^2 - 4x + 3 = 0"
    )

    if st.button("Solve Problem"):

        if problem.strip():

            with st.spinner(
                "Solving problem..."
            ):

                prompt = f"""
Solve the following mathematics problem step-by-step.

Problem:
{problem}

Requirements:
- Explain each step clearly
- Show formulas
- Provide final answer
- Include interpretation
"""

                response = ask_groq(prompt)

                st.markdown(response)

                # =============================================
                # AUTO GRAPH
                # =============================================
                expression = extract_expression(
                    problem
                )

                if expression:

                    render_graph(
                        expression,
                        "problem_solver"
                    )

        else:
            st.warning(
                "Please enter a mathematics problem."
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

# =========================================================
# MCQS GENERATOR
# =========================================================
elif mode == "MCQs Generator":

    st.markdown(
        '<div class="main-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">'
        'MCQs Generator'
        '</div>',
        unsafe_allow_html=True
    )

    render_mcq_generator(
        selected_topic
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )
# =========================================================
# AI CHATBOT
# =========================================================
elif mode == "AI Chatbot":

    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    st.markdown('<div class="section-title">AI Mathematics Chatbot</div>', unsafe_allow_html=True)

    user_query = st.text_input(
        "Ask a mathematics question",
        placeholder="Example: Explain the graph of x^2"
    )

    if st.button("Ask AI"):

        if user_query.strip():

            # ❌ NOT MATH → STOP
            if not is_math_question(user_query):
                st.warning("I can only help with mathematics-related questions.")
            else:

                with st.spinner("Generating response..."):

                    chatbot_prompt = f"""
You are a STRICT mathematics-only AI tutor.

RULES:
- Only answer mathematics-related questions
- If not math → say: "I can only help with mathematics-related questions."

QUESTION:
{user_query}

FORMAT:
- Conceptual explanation
- Step-by-step reasoning (if needed)
- Final answer (if applicable)
"""

                    response = ask_groq(chatbot_prompt)

                    st.session_state.chat_history.append({
                        "question": user_query,
                        "answer": response
                    })

    # =====================================================
# CHAT HISTORY
# =====================================================
for chat in reversed(st.session_state.chat_history):

    st.markdown(f"""
    <div class="chat-box">
    <b>Question:</b><br>
    {chat['question']}
    <br><br>
    <b>Answer:</b><br>
    {chat['answer']}
    </div>
    """, unsafe_allow_html=True)

    expression = extract_expression(chat["question"])
    if expression:
        render_graph(expression, chat["question"])

st.markdown("</div>", unsafe_allow_html=True)
# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.markdown(
    """
<div style='
    text-align:center;
    color:#9CA3AF;
    padding-bottom:20px;
    font-size:14px;
'>

MAI © 2026 | Mathematical Artificial Intelligence Platform

</div>
""",
    unsafe_allow_html=True
)

