import streamlit as st
import re
def is_math_question(text):
    keywords = [
        "equation", "integral", "derivative", "limit", "function",
        "matrix", "vector", "algebra", "geometry", "calculate",
        "solve", "prove", "differentiate", "integrate",
        "log", "sin", "cos", "tan",
        "graph", "plot", "curve", "mathematics", "math"
    ]

    text_lower = text.lower()

    keyword_match = any(word in text_lower for word in keywords)

    # detect math expressions like x^2, x+2, sin(x)
    math_pattern = bool(re.search(r"[xX]\s*[\+\-\*/\^]|sin|cos|tan|log|\d+", text_lower))

    return keyword_match or math_pattern

def render_sidebar():
    """
    Professional AI Learning Platform Sidebar
    Controls navigation + module context + UI branding.
    """


    # =====================================================
    # SECTION TITLE
    # =====================================================
    st.sidebar.markdown("""
    <div style="
        margin-top:10px;
        margin-bottom:10px;
        font-size:12px;
        letter-spacing:1px;
        color:#94A3B8;
        font-weight:600;
        text-transform:uppercase;
    ">
    Learning Modules
    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # MODULE NAVIGATION
    # =====================================================
    mode = st.sidebar.radio(
        "Select Module",
        [
            "Lecture Generator",
            "Problem Solver",
            "MCQs Generator",
            "AI Chatbot"
        ],
        label_visibility="collapsed"
    )

    # =====================================================
    # MODULE DESCRIPTIONS
    # =====================================================
    descriptions = {
        "Lecture Generator": (
            "Generate structured mathematical lectures with "
            "concepts, intuition, examples, and visual insights."
        ),

        "Problem Solver": (
            "Solve mathematical problems step-by-step using "
            "symbolic reasoning and explanatory AI guidance."
        ),

        "MCQs Generator": (
            "Create intelligent quizzes with difficulty levels "
            "and conceptual mathematical assessment."
        ),

        "AI Chatbot": (
            "Interact with an AI mathematics tutor for explanations, "
            "concept clarification, and problem understanding."
        )
    }


    # =====================================================
    # FOOTER
    # =====================================================
    st.sidebar.markdown("""
    <div style="
        margin-top:28px;
        text-align:center;
        color:#64748B;
        font-size:12px;
    ">
        MAI © 2026 • AI Learning System
    </div>
    """, unsafe_allow_html=True)

    return mode