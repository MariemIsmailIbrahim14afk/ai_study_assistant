import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Study Assistant")
st.title("AI Study & Summarization Assistant")
st.write("Upload any text file or PDF, and the AI will summarize it, extract key abbreviations, and generate quiz questions.")

api_key = st.text_input("Enter your Google AI Studio API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    uploaded_file = st.file_uploader("Choose a text or PDF file", type=["txt", "pdf"])
    
    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8", errors="ignore")
        
        if st.button("Start Summarization and Questions"):
            with st.spinner("Analyzing text with AI..."):
                prompt = f"Summarize this text, extract key abbreviations, and suggest 3 comprehension questions:\n\n{file_content}"
                response = model.generate_content(prompt)
                
                st.subheader("Results:")
                st.write(response.text)
else:
    st.info("Please enter your API key above to get started.")