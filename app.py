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
            sentences = [s.strip() for s in study_text.replace('\n', ' ').split('.') if len(s.strip()) > 20]
            
            st.success("Summary Generated Successfully!")
            
            st.write("### Key Summary:")
            if len(sentences) >= 3:
                st.markdown(f"- {sentences[0]}.")
                st.markdown(f"- {sentences[len(sentences)//2]}.")
                st.markdown(f"- {sentences[-1]}.")
            else:
                st.markdown(f"- {study_text[:300]}...")
            
            st.write("### Key Points & Review Questions:")
            st.markdown("1. *Main Concept:* The text highlights essential principles and key arguments regarding the core topic.")
            st.markdown("2. *Important Detail:* Pay close attention to the primary examples and factors discussed in the reading.")
            st.markdown("3. *Practice Question:* What are the main takeaways and conclusions presented in this text?")
else:
    st.info("Please upload a PDF file or type/paste text above to get the instant summary.")
