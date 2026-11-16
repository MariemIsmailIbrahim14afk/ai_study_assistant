import streamlit as st
import requests

st.title("AI Study Assistant")

key = st.text_input("Enter API Key", type="password")

if key:
    text = st.text_area("Paste text here:")
    if text and st.button("Summarize"):
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=" + key
        data = {
            "contents": [{
                "parts": [{"text": "Please summarize this text: " + text}]
            }]
        }
        res = requests.post(url, json=data)
        if res.status_code == 200:
            try:
                st.write(res.json()["candidates"][0]["content"]["parts"][0]["text"])
            except Exception:
                st.write(res.text)
        else:
            st.error(f"Error Code {res.status_code}: {res.text}")
else:
    st.warning("Please enter your API key above.")
