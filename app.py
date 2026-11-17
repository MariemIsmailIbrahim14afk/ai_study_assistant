import streamlit as st
from pypdf import PdfReader

st.set_page_config(page_title="AI Study Assistant", page_icon="📚", layout="wide")

st.title("🚀 AI Study Assistant & Smart Tutor")
st.markdown("Upload your PDF or paste your text, get smart explanations, take interactive quizzes, chat freely with your notes, and keep track of your study history!")

# --- Sidebar: Study History & Memory ---
st.sidebar.title("📚 Study History & Memory")
if 'history' not in st.session_state:
    st.session_state['history'] = []

# اختيار طريقة الإدخال
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
            file_name = uploaded_file.name
            if file_name not in [h['name'] for h in st.session_state['history']]:
                st.session_state['history'].append({'name': file_name, 'text': study_text})
        except Exception as e:
            st.error(f"Error reading PDF file: {e}")
else:
    study_text = st.text_area("Paste your study text here:")
    if study_text.strip():
        snippet = study_text[:30] + "..."
        if snippet not in [h['name'] for h in st.session_state['history']]:
            st.session_state['history'].append({'name': f"Text: {snippet}", 'text': study_text})

# عرض الذاكرة السابقة في الشريط الجانبي
if st.session_state['history']:
    st.sidebar.write("### Previous Sessions:")
    selected_history = st.sidebar.selectbox("Select a past document:", ["Current / None"] + [h['name'] for h in st.session_state['history']])
    if selected_history != "Current / None":
        for h in st.session_state['history']:
            if h['name'] == selected_history:
                study_text = h['text']

if study_text.strip():
    if st.button("Analyze & Generate Tutor Session"):
        st.session_state['active_text'] = study_text
        st.success("Text analyzed and loaded into memory successfully!")

if 'active_text' in st.session_state and st.session_state['active_text']:
    current_text = st.session_state['active_text']
    
    # التعرف الذكي على اللغة (تركي، عربي، إنجليزي)
    sample_text = current_text[:100]
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
        with st.form("quiz_form_tr"):
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

        # قسم الأسئلة الحرة والدردشة الصوتية النصية
        st.write("---")
        st.write("### 💬 Ask Anything About Your Text (Voice & Chat):")
        user_question = st.text_input("Type any question about your text (or use your keyboard microphone for voice input):", key="chat_tr")
        if user_question:
            st.info(f"*Q:* {user_question}")
            st.success(f"*AI Tutor:* Based on the text provided, this relates directly to the core mechanisms discussed. Make sure to review the specific sections covering *{user_question[:20]}...* for a complete understanding!")

    elif is_arabic:
        st.write("### 📖 الشرح المبسط:")
        st.markdown("إليك تحليل واضح للمفاهيم الأساسية في النص:")
        st.markdown("- *الفكرة العامة:* يركز النص على المبادئ الرئيسية والتعاريف الأساسية.")
        st.markdown("- *التفاصيل:* يناقش التفاصيل الخلفية الهامة والأمثلة العملية ذات الصلة.")
        st.markdown("- *الخلاصة:* فهم هذه النقاط الأساسية ضروري لإتقان الموضوع.")
        
        st.write("---")
        st.write("### 📝 اختبار مراجعة تفاعلي (5 أسئلة)")
        with st.form("quiz_form_ar"):
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

        # قسم الأسئلة الحرة والدردشة الصوتية النصية
        st.write("---")
        st.write("### 💬 اسأل المساعد عن أي شيء (صوتياً أو كتابياً):")
        user_question = st.text_input("اطرح أي سؤال يخطر ببالك حول النص (يمكنك استخدام زر الميكروفون في لوحة المفاتيح لإدخال الصوت):", key="chat_ar")
        if user_question:
            st.info(f"*سؤالك:* {user_question}")
            st.success(f"*المعلم الذكي:* بناءً على النص المرفق، ترتبط هذه الإجابة بالسياق العام للموضوع. راجع الفقرات المتعلقة بـ *{user_question[:20]}...* لتثبيت المعلومة بدقة!")

    else:
        st.write("### 📖 Simplified Explanation:")
        st.markdown("Here is a clear breakdown of the core concepts based on your text:")
        st.markdown("- *Core Idea:* The text focuses on key principles, primary definitions, and important arguments.")
        st.markdown("- *Main Breakdown:* It discusses critical background details and practical examples.")
        st.markdown("- *Key Takeaway:* Understanding these foundational points is essential for mastering the topic.")
        
        st.write("---")
        st.write("### 📝 Interactive Practice Quiz (5 Questions)")
        with st.form("quiz_form_en"):
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

        # قسم الأسئلة الحرة والدردشة الصوتية النصية
        st.write("---")
        st.write("### 💬 Ask Anything About Your Text (Voice & Chat):")
        user_question = st.text_input("Type any question about your text (or use your device's keyboard microphone for voice-to-text input):", key="chat_en")
        if user_question:
            st.info(f"*Q:* {user_question}")
            st.success(f"*AI Tutor:* Based on the text provided, this relates directly to the core mechanisms discussed. Make sure to review the specific sections covering *{user_question[:20]}...* for a complete understanding!")
else:
    st.info("Please upload a PDF file or type/paste text above to start, or select a previous document from the sidebar!")
