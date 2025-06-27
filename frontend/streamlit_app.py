import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app import logic
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="SmartSDLC", layout="wide")
st.title("SmartSDLC")
st.caption("AI Assistant for Software Development")

tab1, tab2, tab3 = st.tabs(["📝 Requirement Analysis", "💻 Code Generation", "🧪 Test Case Generator"])

with tab1:
    st.subheader("Upload a PDF or Type a Prompt")
    prompt_input = st.text_area("Type your project idea or paste requirement text:")
    uploaded_file = st.file_uploader("Or upload a PDF", type=["pdf"])

    if st.button("Analyze Requirements"):
        if not prompt_input and not uploaded_file:
            st.warning("Please provide input text or upload a PDF.")
        else:
            pdf_path = None
            if uploaded_file:
                os.makedirs("uploads", exist_ok=True)
                pdf_path = os.path.join("uploads", uploaded_file.name)
                with open(pdf_path, "wb") as f:
                    f.write(uploaded_file.read())
            result = logic.analyze_requirements(prompt_input, pdf_path)
            st.success("✅ Extracted Requirements:")
            st.code(result)

with tab2:
    st.subheader("Generate Frontend/Backend Code")
    requirements = st.text_area("Enter feature requirements:")
    language = st.selectbox("Select Programming Language", ["Python", "JavaScript", "Java", "C++", "HTML", "CSS"])
    framework = st.selectbox("Select Framework", ["Django", "Flask", "React", "FastAPI", "Node.js"])

    if st.button("Generate Code"):
        result = logic.generate_code(requirements, language, framework)
        st.success("✅ Generated Code:")
        st.code(result)

with tab3:
    st.subheader("Generate Test Cases from Code or Requirements")
    test_input = st.text_area("Paste your code or requirements:")

    if st.button("Generate Tests"):
        result = logic.generate_tests(test_input)
        st.success("✅ Generated Test Cases:")
        st.code(result)
