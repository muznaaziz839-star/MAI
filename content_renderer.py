import streamlit as st
import re

def render_content(ai_text):
    """Render AI lecture content with flexible section detection."""

    if not ai_text:
        st.warning("No content received from AI.")
        return

    # ================= SECTION MAP =================
    section_aliases = {
        "definition": "Definition",
        "key formulas": "Formula",
        "formulas": "Formula",
        "formula": "Formula",
        "formula representation": "Representation",
        "representation": "Representation",
        "conceptual explanation": "Explanation",
        "explanation": "Explanation",
        "solved example": "Solved Example",
        "example": "Solved Example",
        "when to use": "When to Use",
        "applications": "When to Use",
    }

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
        clean_line = line.strip()

        # 🔎 Detect headings like:
        # ### 1. Definition
        # ### Definition
        match = re.match(r"^#{1,3}\s*\d*\.?\s*(.+)", clean_line)

        if match:
            heading = match.group(1).lower()

            for key in section_aliases:
                if key in heading:
                    current_section = section_aliases[key]
                    break
            continue

        if current_section:
            sections[current_section] += line + "\n"

    # ================= DISPLAY =================

    displayed_any = False

    if sections["Definition"]:
        st.subheader("📘 Definition")
        st.markdown(sections["Definition"])
        displayed_any = True

    if sections["Formula"]:
        st.subheader("🧮 Formula")
        st.markdown(sections["Formula"])
        displayed_any = True

    if sections["Representation"]:
        st.subheader("🔣 Representation")
        st.markdown(sections["Representation"])
        displayed_any = True

    if sections["Explanation"]:
        st.subheader("💡 Explanation")
        st.markdown(sections["Explanation"])
        displayed_any = True

    if sections["Solved Example"]:
        st.subheader("✅ Solved Example")
        st.markdown(sections["Solved Example"])
        displayed_any = True

    if sections["When to Use"]:
        st.subheader("📍 When to Use")
        st.markdown(sections["When to Use"])
        displayed_any = True

    # 🔴 Fallback: show full content if parsing failed
    if not displayed_any:
        st.markdown(ai_text)