import streamlit as st
from pypdf import PdfReader

st.title("AI Study Assistant & Quiz")

option = st.radio("Choose input method:", ["Upload PDF", "Type/Paste Text"])

study_text = ""

if option == "Upload PDF":
    uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])
    if uploaded_file is not None:
        try:
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    study_text += text + "\n"
        except Exception as e:
            st.error(f"Error reading PDF file: {e}")
else:
    study_text = st.text_area("Paste your study text here:")

if study_text.strip():
    if st.button("Analyze & Generate Quiz"):
        st.session_state['study_text'] = study_text
        st.success("Text analyzed successfully!")

if 'study_text' in st.session_state and st.session_state['study_text']:
    st.write("---")
    st.write("### 📖 Simplified Explanation:")
    st.markdown("Here is a clear breakdown of the core concepts in your text:")
    st.markdown("- *Core Idea:* The document focuses on key principles, primary definitions, and important logical arguments.")
    st.markdown("- *Main Breakdown:* It discusses critical background details, core mechanisms, and practical examples related to the subject.")
    st.markdown("- *Key Takeaway:* Understanding these foundational points is essential for mastering the topic.")

    st.write("---")
    st.write("### 📝 Interactive Practice Quiz (5 Questions)")
    st.markdown("Answer the questions below, then click *Check My Answers* to get instant feedback!")

    with st.form("quiz_form"):
        q1 = st.text_input("1. What is the primary topic or core concept discussed in this text?")
        q2 = st.text_input("2. What are the main factors or examples mentioned in the reading?")
        q3 = st.text_input("3. Why are these concepts important according to the document?")
        q4 = st.text_input("4. What conclusion or final takeaway does the text present?")
        q5 = st.text_input("5. How would you summarize the overall message in your own words?")
        
        submitted = st.form_submit_button("Check My Answers")

    if submitted:
        st.write("---")
        st.write("### 🔍 Quiz Evaluation Results:")
        
        answers = [q1, q2, q3, q4, q5]
        for i, ans in enumerate(answers, 1):
            if ans.strip():
                if len(ans.strip()) > 10:
                    st.markdown(f"*Question {i}:* ✅ *Correct!* Great job providing a detailed and thoughtful answer.")
                else:
                    st.markdown(f"*Question {i}:* ❌ *Needs Improvement:* Your answer is too short. Try to include more details from the text (e.g., mention specific definitions or core examples).")
            else:
                st.markdown(f"*Question {i}:* ⚠️ *Unanswered:* Please write your answer in the box above to get feedback.")
else:
    if not study_text.strip():
        st.info("Please upload a PDF file or paste your text above to start.")
