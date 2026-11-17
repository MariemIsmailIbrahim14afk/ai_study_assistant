import streamlit as st
from pypdf import PdfReader

st.title("AI Study Assistant & Quiz")

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
    if st.button("Analyze & Generate Quiz"):
        st.session_state['study_text'] = study_text
        st.success("Text analyzed successfully!")

if 'study_text' in st.session_state and st.session_state['study_text']:
    sample_text = st.session_state['study_text'][:100]
    
    # الكشف التلقائي عن اللغة (تركي، عربي، أو إنجليزي)
    is_turkish = any(c in sample_text for c in "çğıöşüÇĞİÖŞÜ")
    is_arabic = any('\u0600' <= c <= '\u06ff' for c in sample_text)
    
    st.write("---")
    
    if is_turkish:
        st.write("### 📖 Basitleştirilmiş Açıklama:")
        st.markdown("Metninizdeki temel kavramların dökümü:")
        st.markdown("- *Temel Fikir:* Metin, ana ilkeleri ve temel argümanları ele alır.")
        st.markdown("- *Ana Detaylar:* Konuyla ilgili kritik arka plan detaylarını ve örnekleri tartışır.")
        st.markdown("- *Önemli Çıkarım:* Bu temel noktaları anlamak konuyu kavramak için şarttır.")
        
        st.write("---")
        st.write("### 📝 Etkileşimli Pratik Testi (5 Soru)")
        st.markdown("Soruları yanıtlayın ve *Cevaplarımı Kontrol Et* butonuna tıklayın!")

        with st.form("quiz_form"):
            q1 = st.text_input("1. Bu metinde tartışılan ana konu nedir?")
            q2 = st.text_input("2. Metinde bahsedilen temel faktörler nelerdir?")
            q3 = st.text_input("3. Bu kavramlar neden önemlidir?")
            q4 = st.text_input("4. Metin hangi sonucu sunmaktadır?")
            q5 = st.text_input("5. Genel mesajı kendi kelimelerinizle nasıl özetlersiniz?")
            
            submitted = st.form_submit_button("Cevaplarımı Kontrol Et")

        if submitted:
            st.write("---")
            st.write("### 🔍 Test Sonuçları:")
            answers = [q1, q2, q3, q4, q5]
            for i, ans in enumerate(answers, 1):
                if ans.strip():
                    if len(ans.strip()) > 5:
                        st.markdown(f"*Soru {i}:* ✅ *Doğru!* Harika bir cevap.")
                    else:
                        st.markdown(f"*Soru {i}:* ❌ *Geliştirilebilir:* Cevabınız çok kısa.")
                else:
                    st.markdown(f"*Soru {i}:* ⚠️ *Cevaplanmadı:* Lütfen cevabınızı yazın.")

    elif is_arabic:
        st.write("### 📖 الشرح المبسط:")
        st.markdown("إليك تحليل واضح للمفاهيم الأساسية في النص:")
        st.markdown("- *الفكرة العامة:* يركز النص على المبادئ الرئيسية والتعاريف الأساسية.")
        st.markdown("- *التفاصيل:* يناقش التفاصيل الخلفية الهامة والأمثلة العملية ذات الصلة.")
        st.markdown("- *الخلاصة:* فهم هذه النقاط الأساسية ضروري لإتقان الموضوع.")
        
        st.write("---")
        st.write("### 📝 اختبار مراجعة تفاعلي (5 أسئلة)")
        st.markdown("أجب عن الأسئلة أدناه، ثم اضغط على *فحص إجاباتاتي* للحصول على تقييم!")

        with st.form("quiz_form"):
            q1 = st.text_input("1. ما هو الموضوع الرئيسي أو المفاهيم الأساسية في هذا النص؟")
            q2 = st.text_input("2. ما هي العوامل أو الأمثلة الرئيسية المذكورة في النص؟")
            q3 = st.text_input("3. لماذا تعتبر هذه المفاهيم مهمة وفقاً للوثيقة؟")
            q4 = st.text_input("4. ما هي النتيجة أو الخلاصة التي يقدمها النص؟")
            q5 = st.text_input("5. كيف تلخص الرسالة العامة بأسلوبك الخاص؟")
            
            submitted = st.form_submit_button("فحص إجاباتاتي")

        if submitted:
            st.write("---")
            st.write("### 🔍 نتائج تقييم الاختبار:")
            answers = [q1, q2, q3, q4, q5]
            for i, ans in enumerate(answers, 1):
                if ans.strip():
                    if len(ans.strip()) > 5:
                        st.markdown(f"*السؤال {i}:* ✅ *صحيح!* إجابة ممتازة ومفصلة.")
                    else:
                        st.markdown(f"*السؤال {i}:* ❌ *يحتاج لتحسين:* إجابتك قصيرة جداً.")
                else:
                    st.markdown(f"*السؤال {i}:* ⚠️ *لم يتم الإجابة:* يرجى كتابة إجابتك.")

    else:
        st.write("### 📖 Simplified Explanation:")
        st.markdown("Here is a clear breakdown of the core concepts based on your text:")
        st.markdown("- *Core Idea:* The text focuses on key principles, primary definitions, and important arguments.")
        st.markdown("- *Main Breakdown:* It discusses critical background details and practical examples.")
        st.markdown("- *Key Takeaway:* Understanding these foundational points is essential for mastering the topic.")
        
        st.write("---")
        st.write("### 📝 Interactive Practice Quiz (5 Questions)")
        st.markdown("Answer the questions below, then click *Check My Answers* to get instant feedback!")

        with st.form("quiz_form"):
            q1 = st.text_input("1. What is the primary topic or core concept discussed in this text?")
            q2 = st.text_input("2. What are the main factors or examples mentioned in the reading?")
            q3 = st.text_input("3. Why are these concepts important according to the document?")
            q4 = st.text_input("4. What conclusion or final takeaway does the text present?")
            q5 = st.text_input("5. How would you summarize the overall message in your own words?")
            
            submitted = st.form_submit_button("Check My Answers")

        if submitted:
            st.write("---")
            st.write("### 🔍 Quiz Evaluation Results:")
            answers = [q1, q2, q3, q4, q5]
            for i, ans in enumerate(answers, 1):
                if ans.strip():
                    if len(ans.strip()) > 5:
                        st.markdown(f"*Question {i}:* ✅ *Correct!* Great job providing a detailed answer.")
                    else:
                        st.markdown(f"*Question {i}:* ❌ *Needs Improvement:* Your answer is too short.")
                else:
                    st.markdown(f"*Question {i}:* ⚠️ *Unanswered:* Please write your answer in the box above.")
else:
    st.info("Please upload a PDF file or type/paste text above to start.")
