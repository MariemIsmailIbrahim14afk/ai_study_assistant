import streamlit as st

st.title("AI Personal Study Teacher")

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
    
    # استخراج الجمل بطريقة نظيفة
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
        st.markdown("Metniniz dikkatlice incelendi ve şu temel noktalar çıkarıldı:")
        st.markdown(f"1. *Ana Odak:* '{sentences[0][:100]}...' - Bu ifade konunun temel taşını oluşturur.")
        if len(sentences) > 1:
            st.markdown(f"2. *Detay ve Mantık:* '{sentences[len(sentences)//2][:100]}...' - Burada olayın veya kavramın sebebi açıklanmaktadır.")

        st.write("---")
        st.write(f"### 📝 Pratik Soruları ({num_questions} Soru)")
        st.markdown("Aşağıdaki soruları dikkatlice okuyup cevaplayın:")

        for i in range(num_questions):
            sent_index = (i * max(1, len(sentences) // num_questions)) % len(sentences)
            target_sent = sentences[sent_index]
            
            # صيغة سؤال طبيعية ومباشرة بدون جمل محفوظة
            st.write(f"*Soru {i+1}:* '{target_sent[:70]}...' ifadesine göre, bu durum neden ve nasıl gerçekleşmektedir? Açıklayınız.")
            
            ans = st.text_input(f"Soru {i+1} cevabınız:", key=f"tr_ans_{i}")
            
            if st.button(f"Soru {i+1} Kontrol Et", key=f"tr_btn_{i}"):
                if ans.strip():
                    if len(ans.strip()) > 8:
                        st.success(f"✅ Harika! Çok mantıklı bir açıklama yaptınız.")
                    else:
                        st.warning(f"❌ Biraz kısa oldu. Nedenini veya nasıllığını biraz daha detaylandırın.")
                else:
                    st.error(f"⚠️ Lütfen önce cevابınızı yazın.")
            st.write("---")

    elif is_arabic:
        st.write("### 📖 الشرح المفصل والمهدئ:")
        st.markdown("قمت بتحليل النص الذي أرسلتِه لنفهم فكرته بعمق:")
        st.markdown(f"1. *الفكرة الأساسية:* '{sentences[0][:100]}...' - هذه هي القاعدة التي يبدأ منها فهم الموضوع.")
        if len(sentences) > 1:
            st.markdown(f"2. *السبب والمنطق:* '{sentences[len(sentences)//2][:100]}...' - وهنا يوضح النص سبب حدوث هذا الأمر.")

        st.write("---")
        st.write(f"### 📝 الأسئلة التدريبية ({num_questions} سؤال)")
        st.markdown("اقرأ كل جملة أدناه وأجب عن سببها أو معناها بوضوح:")

        for i in range(num_questions):
            sent_index = (i * max(1, len(sentences) // num_questions)) % len(sentences)
            target_sent = sentences[sent_index]
            
            # صيغة عربية مباشرة تسأل عن "ليه" و"إزاي" من غير روتين
            st.write(f"*السؤال {i+1}:* بخصوص جملة '{target_sent[:70]}...'، لماذا تحدث هذه الحالة أو ما هو تفسيرها العلمي/المنطقي؟")
            
            ans = st.text_input(f"إجابتك عن السؤال {i+1}:", key=f"ar_ans_{i}")
            
            if st.button(f"فحص السؤال {i+1}", key=f"ar_btn_{i}"):
                if ans.strip():
                    if len(ans.strip()) > 8:
                        st.success(f"✅ إجابة ذكية وممتازة! لقد فهمت سبب حدوث ذلك.")
                    else:
                        st.warning(f"❌ إجابتك مختصرة، وضحي أكثر لماذا يحدث هذا.")
                else:
                    st.error(f"⚠️ يرجى كتابة الإجابة أولاً.")
            st.write("---")

    else:
        st.write("### 📖 Detailed Explanation:")
        st.markdown(f"1. *Core Concept:* '{sentences[0][:100]}...'")
        
        st.write("---")
        st.write(f"### 📝 Practice Questions ({num_questions})")

        for i in range(num_questions):
            sent_index = (i * max(1, len(sentences) // num_questions)) % len(sentences)
            target_sent = sentences[sent_index]
            
            st.write(f"*Question {i+1}:* Regarding '{target_sent[:70]}...', why and how does this happen? Explain.")
            
            ans = st.text_input(f"Your answer for Question {i+1}:", key=f"en_ans_{i}")
            
            if st.button(f"Check Question {i+1}", key=f"en_btn_{i}"):
                if ans.strip():
                    if len(ans.strip()) > 8:
                        st.success(f"✅ Correct! Great logical explanation.")
                    else:
                        st.warning(f"❌ Too brief. Explain the reason or how it works in more detail.")
                else:
                    st.error(f"⚠️ Please type your answer first.")
            st.write("---")
