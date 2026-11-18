import streamlit as st
import random

st.title("MARIEM'S Summary & Quiz App")

option = st.radio("Choose input method / Giriş yöntemi / طريقة الإدخال:", ["Upload PDF", "Type/Paste Text"])

study_text = ""

if option == "Upload PDF":
    uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])
    if uploaded_file is not None:
        from pypdf import PdfReader
        with st.spinner("Reading your file... / Dosya okunuyor... / جاري قراءة الملف..."):
            try:
                reader = PdfReader(uploaded_file)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        study_text += text + "\n"
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
else:
    study_text = st.text_area("Paste your study text here / Metninizi buraya yapıştırın:")

num_questions = st.selectbox("Select number of questions / Soru sayısı / عدد الأسئلة:", [5, 10, 20])

if study_text.strip():
    sample_text = study_text[:200]
    is_turkish = any(c in sample_text for c in "çğıöşüÇĞİÖŞÜ")
    is_arabic = any('\u0600' <= c <= '\u06ff' for c in sample_text)
    
    raw_sentences = [s.strip() for s in study_text.replace('\n', ' ').split('.') if len(s.strip()) > 25]
    sentences = []
    for s in raw_sentences:
        if s not in sentences:
            sentences.append(s)
            
    if not sentences:
        sentences = [study_text[:150]]
    
    st.write("---")
    
    if is_turkish:
        st.write("### 📖 Detaylı ve Sabırlı Açıklama:")
        st.markdown(f"1. *Ana Odak:* '{sentences[0][:100]}...'")
        if len(sentences) > 1:
            st.markdown(f"2. *Detay ve Mantık:* '{sentences[len(sentences)//2][:100]}...'")

        st.write("---")
        st.write(f"### 📝 Test Soruları (Çoktan Seçmeli ve Doğru/Yanlış - {num_questions} Soru)")

        for i in range(num_questions):
            sent_index = (i * max(1, len(sentences) // num_questions)) % len(sentences)
            target_sent = sentences[sent_index]
            
            if i % 2 == 0:
                st.write(f"*Soru {i+1} (Çoktan Seçmeli):* '{target_sent[:70]}...' ifadesi ile ilgili aşağıdakilerden hangisi söylenebilir?")
                choice = st.radio(
                    f"Seçiniz (Soru {i+1}):",
                    [
                        "A) Konunun temel tanımı ve amacıdır.",
                        "B) Sadece rastgele bir örnek teşkil eder.",
                        "C) Metnin ana fikri ile çelişmektedir.",
                        "D) Hiçbiri"
                    ],
                    key=f"tr_mc_{i}"
                )
                if st.button(f"Soru {i+1} Kontrol Et", key=f"tr_btn_{i}"):
                    if choice.startswith("A"):
                        st.success("✅ Doğru! Harika bir analiz.")
                    else:
                        st.warning("❌ Yanlış. Doğru seçenek A olmalıdır.")
            else:
                st.write(f"*Soru {i+1} (Doğru / Yanlış):* '{target_sent[:70]}...' ifadesi bu konunun temel mantığını yansıtır.")
                tf_choice = st.radio(f"Seçiniz (Soru {i+1}):", ["Doğru (True)", "Yanlış (False)"], key=f"tr_tf_{i}")
                if st.button(f"Soru {i+1} Kontrol Et", key=f"tr_btn_{i}"):
                    if tf_choice.startswith("Doğru"):
                        st.success("✅ Tebrikler, doğru cevap!")
                    else:
                        st.warning("❌ Yanlış, العبارة صحيحة في سياق النص.")
            st.write("---")

    elif is_arabic:
        st.write("### 📖 الشرح المفصل والمهدئ:")
        st.markdown(f"1. *الفكرة الأساسية:* '{sentences[0][:100]}...'")
        if len(sentences) > 1:
            st.markdown(f"2. *التحليل والسبب:* '{sentences[len(sentences)//2][:100]}...'")

        st.write("---")
        st.write(f"### 📝 اختبار تفاعلي (اختيار من متعدد وصح وخطأ - {num_questions} سؤال)")

        for i in range(num_questions):
            sent_index = (i * max(1, len(sentences) // num_questions)) % len(sentences)
            target_sent = sentences[sent_index]
            
            if i % 2 == 0:
                st.write(f"*السؤال {i+1} (اختيار من متعدد):* بناءً على عبارة '{target_sent[:70]}...', أي مما يلي يمثل التفسير الأدق لها؟")
                choice = st.radio(
                    f"اختر الإجابة (السؤال {i+1}):",
                    [
                        "أ) تمثل الفكرة الجوهرية والسبب الأساسي للدرس.",
                        "ب) تعتبر مجرد تفاصيل ثانوية غير مؤثرة.",
                        "ج) تتناقض مع المفهوم العام للنص.",
                        "د) لا علاقة لها بالموضوع."
                    ],
                    key=f"ar_mc_{i}"
                )
                if st.button(f"فحص السؤال {i+1}", key=f"ar_btn_{i}"):
                    if choice.startswith("أ"):
                        st.success("✅ إجابة صحيحة وممتازة! استوعبت المعنى بدقة.")
                    else:
                        st.warning("❌ إجابة غير دقيقة، الخيار (أ) هو الإجابة الصحيحة.")
            else:
                st.write(f"*السؤال {i+1} (صح أو خطأ):* عبارة '{target_sent[:70]}...' تعبر عن المفهوم الأساسي والمنطقي لهذا الدرس.")
                tf_choice = st.radio(f"اختر الإجابة (السؤال {i+1}):", ["صح", "خطأ"], key=f"ar_tf_{i}")
                if st.button(f"فحص السؤال {i+1}", key=f"ar_btn_{i}"):
                    if tf_choice == "صح":
                        st.success("✅ ممتاز! إجابتك صحيحة.")
                    else:
                        st.warning("❌ خطأ، هذه العبارة صحيحة حسب سياق النص.")
            st.write("---")
            
    else:
        st.write("### 📖 Detailed Explanation:")
        st.write(f"### 📝 Quiz ({num_questions} Questions)")
        for i in range(num_questions):
            sent_index = (i * max(1, len(sentences) // num_questions)) % len(sentences)
            target_sent = sentences[sent_index]
            st.write(f"*Question {i+1}:* Regarding '{target_sent[:70]}...', is this statement true or false?")
            ans = st.radio(f"Q{i+1} Answer:", ["True", "False"], key=f"en_{i}")
            if st.button(f"Check Q{i+1}", key=f"en_btn_{i}"):
                if ans == "True":
                    st.success("✅ Correct!")
                else:
                    st.warning("❌ Incorrect.")
            st.write("---")
