import streamlit as st
import google.generativeai as genai

st.title("AI Study & Summarization Assistant")

user_api_key = st.text_input("Enter your Google AI Studio API Key", type="password")

if user_api_key:
    try:
        genai.configure(api_key=user_api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        uploaded_file = st.file_uploader("Choose a text or PDF file", type=["pdf", "txt"])
        if uploaded_file is not None:
            st.success("File uploaded successfully!")
            if st.button("Start Summarization and Questions"):
                bytes_data = uploaded_file.read()
                text_content = bytes_data.decode("utf-8", errors="ignore")
                
                with st.spinner("Processing..."):
                    response = model.generate_content(f"Please summarize this study text and extract key points and questions: {text_content}")
                    st.write(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Please enter your Google AI Studio API key in the field above to start the app.")import streamlit as st
import google.generativeai as genai

st.title("AI Study & Summarization Assistant")

user_api_key = st.text_input("Enter your Google AI Studio API Key", type="password")

if user_api_key:
    try:
        genai.configure(api_key=user_api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        uploaded_file = st.file_uploader("Choose a text or PDF file", type=["pdf", "txt"])
        if uploaded_file is not None:
            st.success("File uploaded successfully!")
            if st.button("Start Summarization and Questions"):
                bytes_data = uploaded_file.read()
                text_content = bytes_data.decode("utf-8", errors="ignore")
                
                with st.spinner("Processing..."):
                    response = model.generate_content(f"Please summarize this study text and extract key points and questions: {text_content}")
                    st.write(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Please enter your Google AI Studio API key in the field above to start the app.")
