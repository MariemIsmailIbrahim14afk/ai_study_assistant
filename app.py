import streamlit as st
from pypdf import PdfReader

st.title("AI Study Assistant")

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
    if st.button("Summarize"):
        with st.spinner("Analyzing and summarizing..."):
            words = study_text.split()
            summary_length = max(5, len(words) // 3)
            summary = " ".join(words[:summary_length]) + "..."
            
            st.success("Summary Generated Successfully!")
            st.write("### Key Summary:")
            st.write(summary)
            
            st.write("### Key Points & Questions:")
            st.markdown(f"1. Main topic focus: *{words[0] if words else 'Study Text'}*")
            st.markdown("2. This text emphasizes important concepts that require detailed review.")
            st.markdown("3. *Practice Question:* What is the main message conveyed in this text?")
else:
    st.info("Please upload a PDF file or type/paste text above to get the instant summary.")
