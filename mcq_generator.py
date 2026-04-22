import streamlit as st
import json
import re
from groq_service import ask_groq


def generate_mcq_prompt(topic, count):
    return f"""
Generate {count} multiple choice questions for Calculus topic: {topic}

Rules:
1. Each question must have 4 options: A, B, C, D
2. Mention correct answer
3. Give short explanation
4. Output ONLY valid JSON list

[
 {{
   "question":"What is derivative of x^2?",
   "options": {{
      "A":"x",
      "B":"2x",
      "C":"x²",
      "D":"2"
   }},
   "answer":"B",
   "explanation":"Using power rule derivative of x² = 2x."
 }}
]
"""


def extract_json(text):
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        return match.group(0)
    return None


def render_mcq_generator(topic):

    st.header("📝 AI MCQ Generator")

    count = st.selectbox("Select Number of MCQs", [10, 20, 30])

    # Session state
    if "mcqs" not in st.session_state:
        st.session_state.mcqs = []

    if st.button("Generate MCQs"):

        with st.spinner("Generating..."):

            prompt = generate_mcq_prompt(topic, count)
            response = ask_groq(prompt)

            json_text = extract_json(response)

            if json_text:
                st.session_state.mcqs = json.loads(json_text)
            else:
                st.error("Failed to generate MCQs")

    # Show MCQs after generation
    if st.session_state.mcqs:

        for i, q in enumerate(st.session_state.mcqs):

            st.markdown("---")
            st.subheader(f"Q{i+1}. {q['question']}")

            st.radio(
                "Choose Answer",
                list(q["options"].items()),
                format_func=lambda x: f"{x[0]}. {x[1]}",
                key=f"radio_{i}"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Show Answer", key=f"ans{i}"):
                    st.success(
                        f"Correct Answer: {q['answer']} - {q['options'][q['answer']]}"
                    )

            with col2:
                if st.button("Explain", key=f"exp{i}"):
                    st.info(q["explanation"])