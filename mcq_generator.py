import streamlit as st
import json
import re
from groq_service import ask_groq
# =========================================================
# MCQ PROMPT GENERATOR (NO DIFFICULTY)
# =========================================================
def generate_mcq_prompt(topic, count):
    return f"""
You are a strict JSON generator.

Generate {count} MCQs for topic: {topic}

RULES:
- Output ONLY valid JSON array
- No explanations
- No markdown
- No extra text

FORMAT MUST BE EXACT:

[
  {{
    "question": "string",
    "options": {{
      "A": "string",
      "B": "string",
      "C": "string",
      "D": "string"
    }},
    "answer": "A",
    "explanation": "string"
  }}
]
"""


# =========================================================
# JSON EXTRACTION
# =========================================================
def extract_json(text):
    try:
        text = text.replace("```json", "").replace("```", "")

        start = text.find("[")
        end = text.rfind("]")

        if start == -1 or end == -1:
            return None

        return text[start:end + 1]

    except:
        return None


# =========================================================
# VALIDATION
# =========================================================
def validate_mcqs(mcqs):
    required_keys = {"question", "options", "answer", "explanation"}

    for mcq in mcqs:
        if not required_keys.issubset(mcq.keys()):
            return False

    return True


# =========================================================
# MAIN UI
# =========================================================
def render_mcq_generator(topic):

    if "mcqs" not in st.session_state:
        st.session_state.mcqs = []

    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
        
    if "score" not in st.session_state:
        st.session_state.score = 0
    # =====================================================
    # HEADER
    # =====================================================
    st.markdown("""
    <div style="
        font-size:28px;
        font-weight:700;
        margin-bottom:10px;
    ">
    AI MCQs Generator
    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # ONLY NUMBER OF MCQs (REMOVED DIFFICULTY)
    # =====================================================
    count = st.selectbox(
        "Number of Questions",
        [5, 10, 15, 20]
    )

    # =====================================================
    # GENERATE BUTTON
    # =====================================================
    if st.button("Generate Assessment"):

        st.session_state.quiz_submitted = False

        with st.spinner("Generating AI assessment..."):

            prompt = generate_mcq_prompt(topic, count)
            response = ask_groq(prompt)

            json_text = extract_json(response)

            if json_text:
                try:
                    st.session_state.mcqs = json.loads(json_text)
                except Exception:
                    st.error("MCQ format error. Please try again.")
                    st.text(json_text)
            else:
                st.error("No valid MCQ JSON detected.")

    # =====================================================
    # DISPLAY MCQS
    # =====================================================
    if st.session_state.mcqs:

        st.markdown("## Assessment Questions")

        score = 0

        for i, q in enumerate(st.session_state.mcqs):

            st.markdown("""
            <div style="
                background:white;
                border:1px solid #E5E7EB;
                border-radius:16px;
                padding:22px;
                margin-bottom:20px;
                box-shadow:0 2px 8px rgba(0,0,0,0.04);
            ">
            """, unsafe_allow_html=True)

            st.markdown(f"### Question {i+1}")
            st.markdown(f"**{q['question']}**")

            user_answer = st.radio(
                "Select Answer",
                list(q["options"].keys()),
                format_func=lambda x: f"{x}. {q['options'][x]}",
                key=f"mcq_{i}"
            )

            if st.session_state.quiz_submitted:

                if user_answer == q["answer"]:
                    score += 1
                    st.success(
                        f"Correct Answer: {q['answer']} - {q['options'][q['answer']]}"
                    )
                else:
                    st.error(
                        f"Correct Answer: {q['answer']} - {q['options'][q['answer']]}"
                    )

                st.info(f"Explanation: {q['explanation']}")

            st.markdown("</div>", unsafe_allow_html=True)

        # =================================================
        # SUBMIT BUTTON
        # =================================================
        if not st.session_state.quiz_submitted:

            if st.button("Submit Assessment"):
                st.session_state.quiz_submitted = True
                st.rerun()

        # =================================================
        # SCORE
        # =================================================
        if st.session_state.quiz_submitted:

            total = len(st.session_state.mcqs)
            percentage = round((score / total) * 100, 2)

            st.markdown("---")

            st.markdown(f"""
            <div style="
                background:#EFF6FF;
                border:1px solid #BFDBFE;
                padding:24px;
                border-radius:16px;
                text-align:center;
            ">

            <div style="
                font-size:30px;
                font-weight:700;
                color:#1D4ED8;
            ">
            {score} / {total}
            </div>

            <div style="
                font-size:18px;
                color:#374151;
                margin-top:8px;
            ">
            Assessment Score
            </div>

            <div style="
                margin-top:10px;
                font-size:16px;
                color:#6B7280;
            ">
            Performance: {percentage}%
            </div>

            </div>
            """, unsafe_allow_html=True)