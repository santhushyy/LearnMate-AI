import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Page Config 
st.set_page_config(page_title="AI Learning Agent", layout="centered")

# Load API Key 
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Custom Styling 
st.markdown("""
<style>
.big-title {
    font-size: 42px;
    font-weight: 700;
}
.subtitle {
    color: gray;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🤖 AI Learning Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Smart assistant with memory, reasoning & study tools</div>', unsafe_allow_html=True)

# Memory 
if "history" not in st.session_state:
    st.session_state.history = []

# Demo Response Function 
def demo_response(text):
    t = text.lower()

    # Subject detection
    if any(word in t for word in ["ai", "machine learning", "data", "algorithm"]):
        subject = "Artificial Intelligence"
    elif any(word in t for word in ["economics", "market", "demand", "supply"]):
        subject = "Economics"
    elif any(word in t for word in ["business", "marketing", "branding"]):
        subject = "Business"
    elif any(word in t for word in ["science", "physics", "chemistry"]):
        subject = "Science"
    else:
        subject = "General Knowledge"

    # Special features
    if "quiz" in t:
        return f"""
### 🧠 Quiz on {subject}
1. What is the basic concept of {subject}?  
2. Give one real-world example.  
3. Why is {subject} important?
"""

    if "plan" in t:
        return f"""
### 📅 Study Plan for {subject}
Day 1: Understand fundamentals  
Day 2: Learn key concepts  
Day 3: Practice examples  
Day 4: Revise and test yourself  
"""

    # Structured response
    return f"""
### 📘 Topic: {text}

**Definition:**  
{text.capitalize()} is an important concept in {subject}.

**Explanation:**  
It involves understanding principles, analyzing patterns, and applying knowledge.

**Example:**  
A practical example can be seen in real-world applications.

**Why it matters:**  
Understanding {text} improves critical thinking and decision-making skills.
"""

# Chat Input
user_input = st.text_input("Ask something (e.g., AI, economics, quiz, study plan):")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful learning assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        answer = response.choices[0].message.content

    except:
        st.info("⚙️ Demo Mode Active: Simulated intelligent responses")

        with st.spinner("Thinking..."):
            answer = demo_response(user_input)

    st.session_state.history.append({"role": "assistant", "content": answer})

    st.markdown(f"### 🤖 Answer\n{answer}")

    # Memory display
    if len(st.session_state.history) > 2:
        prev = [m["content"] for m in st.session_state.history if m["role"] == "user"]
        if len(prev) >= 2:
            st.success(f"🧠 Memory: I remember you asked about '{prev[-2]}'")

# Feature Buttons 
st.subheader("🚀 Agent Features")

col1, col2 = st.columns(2)

with col1:
    if st.button("🧠 Generate Quiz"):
        st.markdown(demo_response("quiz"))

with col2:
    if st.button("📅 Study Plan"):
        st.markdown(demo_response("plan"))

# Explanation Section 
st.divider()
st.markdown("""
### 🧠 How this AI Agent Works
- Understands user queries  
- Detects subject domain  
- Generates structured responses  
- Remembers previous interactions  
- Provides learning tools (quiz & study plans)
""")

# Footer 
st.success("✅ AI Agent Ready")