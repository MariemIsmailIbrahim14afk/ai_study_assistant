import streamlit as st
import google.generativeai as genai

st.title("AI Study & Summarization Assistant")

user_api_key = st.text_input("Enter your Google AI Studio API Key", type="password")

if user_api_key:
    try:
        genai.configure(api_key=user_api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        study_text = st.text_area("Paste your study text here:")
        if study_text:
            if st.button("Start Summarization"):
                with st.spinner("Processing..."):
                    response = model.generate_content(f"Please summarize this study text and extract key points: {study_text}")
                    st.write(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Please enter your Google AI Studio API key in the field above to start the
