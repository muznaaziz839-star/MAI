def generate_topic_prompt(topic):
    """Create structured AI prompt for content sections."""
    return f"""
    Provide structured calculus notes for: {topic}

    Include:
    1. Definition
    2. Key Formulas (LaTeX)
    3. Formula Representation
    4. Conceptual Explanation
    5. One solved example with steps (LaTeX)
    6. When to use this concept
    """