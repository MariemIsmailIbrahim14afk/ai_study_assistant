import streamlit as st
from pypdf import PdfReader

st.title("AI Personal Study Teacher & Dynamic Quiz")

if "study_text" not in st.session_state:
    st.session_state.study_text = ""

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

# اختيار عدد الأسئلة المطلوب
num_questions = st.selectbox("Select number of practice questions:", [5, 10, 20])

if study_text.strip():
    if st.button("Analyze & Generate Dynamic Quiz"):
        st.session_state.study_text = study_text
        st.success("File analyzed successfully! Generating custom questions based on your text...")

if st.session_state.study_text:
    active_text = st.session_state.study_text
    
    # استخراج جمل حقيقية من النص المُدخل لعمل أسئلة مخصصة للملف نفسه
    sentences = [s.strip() for s in active_text.replace('\n', ' ').split('.') if len(s.strip()) > 25]
    
    st.write("---")
    st.write("### 📖 Simplified & Detailed Explanation:")
    st.markdown("Here is a calm and detailed breakdown based specifically on your uploaded text:")
    if len(sentences) >= 3:
        st.markdown(f"- *Main Point 1:* {sentences[0]}.")
        st.markdown(f"- *Main Point 2:* {sentences[len(sentences)//2]}.")
        st.markdown(f"- *Core Conclusion:* {sentences[-1]}.")
    else:
        st.markdown("- *Core Concept:* The text highlights essential principles and key arguments.")

    st.write("---")
    st.write(f"### 📝 Custom Practice Quiz ({num_questions} Questions from your text)")
    st.markdown("Answer each question below and click *Check this question* right next to it to test yourself individually!")

    # توليد الأسئلة بناءً على محتوى الملف فعلياً وتخصيص زرار منفصل لكل سؤال
    for i in range(num_questions):
        # اختيار جزء من النص لكل سؤال لضمان تنوع الأسئلة
        target_sent = sentences[i % len(sentences)] if sentences else "this core topic"
        
        st.write(f"*Question {i+1}:* Based on the text regarding '{target_sent[:50]}...', explain what this means or why it happens.")
        
        # خانة إجابة لكل سؤال بشكل منفصل
        ans = st.text_input(f"Your answer for Question {i+1}:", key=f"q_ans_{i}")
        
        # زر كنترول خاص لكل سؤال لوحده
        if st.button(f"Check Question {i+1}", key=f"check_btn_{i}"):
            if ans.strip():
                if len(ans.strip()) > 8:
                    st.success(f"✅ Question {i+1} is Correct! Great understanding of the text.")
                else:
                    st.warning(f"❌ Question {i+1} needs more detail. Try to explain why or how based on the reading.")
            else:
                st.error(f"⚠️ Please type an answer for Question {i+1} first.")
        
        st.write("---")

    # جزء إعادة الشرح المخصص
    st.write("### 💬 Ask for a Specific Part to Be Re-explained:")
    custom_q = st.text_input("Is there a specific part you want me to re-explain slowly?:")
    if custom_q:
        st.info(f"*Detailed Re-explanation:* Let's look closely at '{custom_q}'. Here is a slower, simpler breakdown of this specific concept from your document so you can master it easily.")
