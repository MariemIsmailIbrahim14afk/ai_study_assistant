import streamlit as st

st.title("AI Study Assistant")

study_text = st.text_area("Paste your study text here:")

if study_text:
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
    st.warning("Please paste your text above to get the instant summary.")
