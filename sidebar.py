# components/sidebar.py

import streamlit as st
from groq_service import ask_groq

def render_sidebar():
    """Render MAI sidebar tools."""

    st.sidebar.title("⚙️ MAI Tools")

    mode = st.sidebar.radio(
        "Choose Mode",
        ["Lecture Mode", "Solve Problem", "Chatbot"]
    )

    # ================= SOLVE MODE =================
    if mode == "Solve Problem":
        st.sidebar.subheader("🧮 Solve a Math Problem")

        problem = st.sidebar.text_area("Enter Problem")

        if st.sidebar.button("Solve"):
            if problem.strip():
                with st.spinner("Solving..."):

                    prompt = f"""
                    Solve this mathematics problem step by step:

                    {problem}

                    Show formulas and final answer.
                    """

                    solution = ask_groq(prompt)

                    st.sidebar.markdown("### ✅ Solution")
                    st.sidebar.write(solution)
            else:
                st.sidebar.warning("Please enter a problem.")

    # ================= CHATBOT =================
    if mode == "Chatbot":
        st.sidebar.subheader("💬 Ask MAI")

        question = st.sidebar.text_input("Your Question")

        if st.sidebar.button("Ask"):
            if question.strip():
                with st.spinner("Thinking..."):

                    prompt = f"""
                    You are MAI, a mathematics assistant.

                    Answer clearly and stay focused on math.

                    Question: {question}
                    """

                    answer = ask_groq(prompt)

                    st.sidebar.markdown("### 🤖 Answer")
                    st.sidebar.write(answer)
            else:
                st.sidebar.warning("Please enter a question.")