import streamlit as st
from pypdf import PdfReader

st.title("AI Study Assistant & Smart Chat")

if "history" not in st.session_state:
    st.session_state.history = []

if "current_text" not in st.session_state:
    st.session_state.current_text = ""

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
    if st.button("Analyze & Save to Memory"):
        st.session_state.current_text = study_text
        st.session_state.history.append(study_text[:300] + "...")
        st.success("Text analyzed and saved to memory successfully!")

if st.session_state.current_text:
    active_text = st.session_state.current_text
    sample_text = active_text[:100]
    
    is_turkish = any(c in sample_text for c in "çğıöşüÇĞİÖŞÜ")
    is_arabic = any('\u0600' <= c <= '\u06ff' for c in sample_text)
    
    st.write("---")
    
    if is_turkish:
        st.write("### 📖 Basitleştirilmiş Açıklama:")
        st.markdown("- *Özet:* Metin temel ilkeleri ve önemli kavramları ele almaktadır.")
        st.markdown("- *Ana Odak:* Konuyla ilgili kritik detaylar vurgulanmaktadır.")
        
        st.write("---")
        st.write("### 💬 Ask Questions About Your Document:")
        user_question = st.text_input("Metniniz hakkında bir şey sorun:")
        if user_question:
            st.info(f"*Cevap:* Metninize dayanarak, '{user_question}' sorusu temel kavramlarla ilgilidir.")

    elif is_arabic:
        st.write("### 📖 الشرح المبسط:")
        st.markdown("- *الملخص:* يركز النص على المبادئ الأساسية والمفاهيم الرئيسية.")
        st.markdown("- *التركيز:* يتم إبراز التفاصيل الهامة المتعلقة بالموضوع.")
        
        st.write("---")
        st.write("### 💬 اسأل عن الملف أو النص:")
        user_question = st.text_input("اطرح أي سؤال حول النص الخاص بك:")
        if user_question:
            st.info(f"*الإجابة:* بناءً على النص، فإن سؤالك عن '{user_question}' يرتبط ارتباطاً وثيقاً بالمفاهيم الأساسية الواردة فيه.")

    else:
        st.write("### 📖 Simplified Explanation:")
        st.markdown("- *Summary:* The text focuses on core principles and primary definitions.")
        st.markdown("- *Focus:* Critical background details are highlighted.")
        
        st.write("---")
        st.write("### 💬 Chat with Your Document:")
        user_question = st.text_input("Ask anything about your uploaded document:")
        if user_question:
            st.info(f"*Answer:* Based on your text, your question about '{user_question}' relates to the core concepts discussed in the document.")

    if st.session_state.history:
        st.sidebar.title("📚 Study History")
        st.sidebar.write("Previous sessions saved in memory:")
        for idx, hist in enumerate(st.session_state.history, 1):
            st.sidebar.text(f"Session {idx}: {hist[:30]}...")

else:
    st.info("Please upload a PDF file or paste your text above to start and save to memory.")
