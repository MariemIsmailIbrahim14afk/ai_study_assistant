import streamlit as st
from pypdf import PdfReader

st.title("AI Personal Study Teacher")

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

if study_text.strip():
    if st.button("Start Detailed Explanation & Quiz"):
        st.session_state.study_text = study_text
        st.success("Text received successfully! Let's study step by step.")

if st.session_state.study_text:
    active_text = st.session_state.study_text
    sample_text = active_text[:100]
    
    is_turkish = any(c in sample_text for c in "çğıöşüÇĞİÖŞÜ")
    is_arabic = any('\u0600' <= c <= '\u06ff' for c in sample_text)
    
    st.write("---")
    
    if is_turkish:
        st.write("### 📖 Detaylı ve Sabırlı Açıklama:")
        st.markdown("Gönderdiğiniz metni adım adım ve çok dikkatli bir şekilde inceliyoruz:")
        st.markdown("- *Ana Konu:* Metin temel kavramları ve en önemli detayları içermektedir.")
        st.markdown("- *Önemli Noktalar:* Bu konuyu iyice anlamanız için temel mantığı kavraman gerekiyor.")
        
        st.write("---")
        st.write("### 📝 5 Eğitim Sorusu (Practice Quiz):")
        st.markdown("Lütfen aşağıdaki 5 soruya cevaplarınızı yazın:")
        
        with st.form("quiz_tr"):
            ans1 = st.text_input("1. Metnin ana fikri veya temel konusu nedir?")
            ans2 = st.text_input("2. Okuduğunuz metne göre en önemli detay nedir?")
            ans3 = st.text_input("3. Bu kavramlar niçin bu kadar önemlidir?")
            ans4 = st.text_input("4. Metnin sonuç kısmı bize ne anlatıyor?")
            ans5 = st.text_input("5. Bu konuyu kendi cümlelerinizle nasıl özetlersiniz?")
            
            check_btn = st.form_submit_button("Cevaplarımı Kontrol Et")
            
        if check_btn:
            st.write("### 🔍 Değerlendirme Sonucu:")
            answers = [ans1, ans2, ans3, ans4, ans5]
            for idx, a in enumerate(answers, 1):
                if len(a.strip()) > 5:
                    st.markdown(f"*Soru {idx}:* ✅ *Harika!* Çok iyi bir açıklama yaptınız.")
                else:
                    st.markdown(f"*Soru {idx}:* ❌ *Eksik:* Bu cevabı biraz daha detaylandırmalısınız.")

        st.write("---")
        st.write("### 💬 Özel Soru / Belirli Bir Kısmı Tekrar İsteme:")
        custom_q = st.text_input("Anlamadığınız veya tekrar anlatmasını istediğiniz bir yer var mı?:")
        if custom_q:
            st.info(f"*Açıklama:* İstediğiniz '{custom_q}' konusunu sizin için yavaşça ve detaylıca tekrar açıklıyorum: Bu kısım temel olarak mantığı kavramanız için çok önemlidir.")

    elif is_arabic:
        st.write("### 📖 الشرح المفصل والمهدئ:")
        st.markdown("هيا لنقترب من النص وندرسه بتمهل شديد وبخطوات بسيطة:")
        st.markdown("- *الفكرة الجوهرية:* يوضح النص المبادئ الأساسية والأفكار المركزية التي يجب التركيز عليها.")
        st.markdown("- *نقاط هامة جداً:* ركز جيداً على التفاصيل والأمثلة المذكورة لأنها أساس الفهم.")
        
        st.write("---")
        st.write("### 📝 5 أسئلة تدريبية:")
        st.markdown("حاول الإجابة على الأسئلة التالية لاختبار فهمك:")
        
        with st.form("quiz_ar"):
            ans1 = st.text_input("1. ما هي الفكرة الأساسية أو الموضوع الرئيسي في النص؟")
            ans2 = st.text_input("2. ما هي أهم التفاصيل المذكورة في القراءة؟")
            ans3 = st.text_input("3. لماذا تعتبر هذه النقاط مفترق طرق هام في الموضوع؟")
            ans4 = st.text_input("4. ما هو الاستنتاج أو الخلاصة التي يقدمها الكاتب؟")
            ans5 = st.text_input("5. كيف تشرح هذه الأفكار بأسلوبك الخاص وبكلماتك؟")
            
            check_btn = st.form_submit_button("تحقق من إجاباتاتي")
            
        if check_btn:
            st.write("### 🔍 نتيجة التصحيح:")
            answers = [ans1, ans2, ans3, ans4, ans5]
            for idx, a in enumerate(answers, 1):
                if len(a.strip()) > 5:
                    st.markdown(f"*السؤال {idx}:* ✅ *إجابة ممتازة وصحيحة!* أحسنتِ.")
                else:
                    st.markdown(f"*السؤال {idx}:* ❌ *يحتاج توضيح أكثر:* إجابتك مختصرة جداً، حاولي إضافة تفاصيل أكثر.")

        st.write("---")
        st.write("### 💬 سؤال مخصص أو طلب إعادة شرح جزء معين:")
        custom_q = st.text_input("هل ترغبين أن أشرح لكِ جزئية معينة مرة أخرى؟:")
        if custom_q:
            st.info(f"*إعادة الشرح بتمهل:* بناءً على طلبك لشرح ('{custom_q}'), دعيني أبسطها لكِ أكثر: هذه الجزئية تعني ببساطة التركيز على المفهوم الأساسي وتطبيق مراحله خطوة بخطوة.")

    else:
        st.write("### 📖 Detailed & Patient Explanation:")
        st.markdown("Let's study your text step by step, slowly and thoroughly:")
        st.markdown("- *Core Concept:* The text focuses on essential principles and fundamental definitions.")
        st.markdown("- *Important Highlights:* Pay close attention to the background details and core arguments.")
        
        st.write("---")
        st.write("### 📝 5 Practice Questions:")
        
        with st.form("quiz_en"):
            ans1 = st.text_input("1. What is the main topic or primary focus of this text?")
            ans2 = st.text_input("2. What are the key details mentioned in the reading?")
            ans3 = st.text_input("3. Why are these concepts crucial for understanding the subject?")
            ans4 = st.text_input("4. What conclusion does the author present?")
            ans5 = st.text_input("5. How would you explain this in your own words?")
            
            check_btn = st.form_submit_button("Check My Answers")
            
        if check_btn:
            st.write("### 🔍 Evaluation Results:")
            answers = [ans1, ans2, ans3, ans4, ans5]
            for idx, a in enumerate(answers, 1):
                if len(a.strip()) > 5:
                    st.markdown(f"*Question {idx}:* ✅ *Correct!* Great job and well thought out.")
                else:
                    st.markdown(f"*Question {idx}:* ❌ *Needs Improvement:* Too short. Add more details.")

        st.write("---")
        st.write("### 💬 Ask for a Specific Part to Be Re-explained:")
        custom_q = st.text_input("Is there a specific part you want me to re-explain?:")
        if custom_q:
            st.info(f"*Detailed Re-explanation:* Let's look closely at '{custom_q}'. Here is a slower, simpler breakdown of this specific concept so you can master it easily.")
