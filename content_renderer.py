import streamlit as st
import re

def render_content(ai_text):
    """Split AI response into sections and render clean UI."""

    sections = {
        "Definition": "",
        "Formula": "",
        "Representation": "",
        "Explanation": "",
        "Solved Example": "",
        "When to Use": "",
    }

    current_section = None

    for line in ai_text.split("\n"):
        line = line.strip()

        # Detect headings
        match = re.match(r"##\s*(.*)", line)
        if match:
            heading = match.group(1)
            if heading in sections:
                current_section = heading
            continue

        # Add content to section
        if current_section:
            sections[current_section] += line + "\n"

    # ================= DISPLAY =================

    if sections["Definition"]:
        st.subheader("📘 Definition")
        st.write(sections["Definition"])

    if sections["Formula"]:
        st.subheader("🧮 Formula")
        st.latex(sections["Formula"])

    if sections["Representation"]:
        st.subheader("🔣 Representation")
        st.latex(sections["Representation"])

    if sections["Explanation"]:
        st.subheader("💡 Explanation")
        st.write(sections["Explanation"])

    if sections["Solved Example"]:
        st.subheader("✅ Solved Example")
        st.write(sections["Solved Example"])

    if sections["When to Use"]:
        st.subheader("📍 When to Use")
        st.write(sections["When to Use"])