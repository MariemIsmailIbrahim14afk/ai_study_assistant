import streamlit as st
import requests

st.title("AI Study Assistant")

key = st.text_input("Enter API Key", type="password")

if key:
    text = st.text_area("Paste text here:")
    if text and st.button("Summarize"):
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + key
        data = {
            "contents": [{
                "parts": [{"text": "Summarize this: " + text}]
            }]
        }
        res = requests.post(url, json=data)
        if res.status_code == 200:
            st.write(res.json()["candidates"][0]["content"]["parts"][0]["text"])
        else:
            st.write("Error occurred")
else:
    st.write("Please enter your API key above.")
