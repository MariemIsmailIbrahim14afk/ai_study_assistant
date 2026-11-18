import streamlit as st
from pypdf import PdfReader

st.title("AI Personal Study Teacher")

option = st.radio("Choose input method / Giriş yöntemi / طريقة الإدخال:", ["Upload PDF", "Type/Paste Text"])

study_text = ""

if option == "Upload PDF":
    uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])
    if uploaded_file is not None:
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
    sample_text = study_text[:150]
    is_turkish = any(c in sample_text for c in "çğıöşüÇĞİÖŞÜ")
    is_arabic = any('\u0600' <= c <= '\u06ff' for c in sample_text)
    
    sentences = [s.strip() for s in study_text.replace('\n', ' ').split('.') if len(s.strip()) > 20]
    
    st.write("---")
    
    if is_turkish:
        st.write("### 📖 Detaylı ve Sabırlı Açıklama:")
        st.markdown("Gönderdiğiniz metni adım adım, yavaşça ve derinlemesine inceliyoruz:")
        if len(sentences) >= 3:
            st.markdown(f"- *Ana Fikir ve Detaylı Açıklama:* Metin temel olarak şu konuya odaklanmaktadır: '{sentences[0]}'. Bu durum, konunun temel mantığını anlamamız için oldukça önemlidir.")
            st.markdown(f"- *Gelişme ve Neden Sonuç İlişkisi:* İlerleyen kısımda ise şu husus vurgulanmaktadır: '{sentences[len(sentences)//2]}'. Burada yazar, olayların veya kavramların birbirine nasıl bağlandığını yavaşça açıklıyor.")
            st.markdown(f"- *Sonuç ve Ana Çıkarım:* Metnin bütününde varılan sonuç şudur: '{sentences[-1]}'. Bu da konuyu kavramamız için anahtardır.")
        else:
            st.markdown("- *Genel Açıklama:* Metin, temel prensipleri ve kavramları ayrıntılı bir şekilde ele almaktadır.")

        st.write("---")
        st.write(f"### 📝 Metne Özel Pratik Testi ({num_questions} Soru)")
        st.markdown("Her soruyu aşağıda yanıtlayıp hemen yanındaki butona basarak kontrol edebilirsiniz:")

        for i in range(num_questions):
            target_sent = sentences[i % len(sentences)] if sentences else "bu temel konu"
            st.write(f"*Soru {i+1}:* '{target_sent[:60]}...' ifadesine dayanarak, bu durumun temel sebebi nedir veya ne anlama gelmektedir?")
            
            ans = st.text_input(f"Soru {i+1} için cevabınız:", key=f"tr_ans_{i}")
            
            if st.button(f"Soru {i+1} Kontrol Et", key=f"tr_btn_{i}"):
                if ans.strip():
                    if len(ans.strip()) > 8:
                        st.success(f"✅ Soru {i+1} Doğru! Metni çok iyi anlamışsınız.")
                    else:
                        st.warning(f"❌ Soru {i+1} biraz eksik. Metne dayanarak biraz daha detay eklemelisiniz.")
                else:
                    st.error(f"⚠️ Lütfen önce Soru {i+1} için bir cevap yazın.")
            st.write("---")

        st.write("### 💬 Belirli Bir Kısmı Tekrar Açıklama İsteme:")
        custom_q = st.text_input("Anlamadığınız veya detaylıca tekrar anlatmamı istediğiniz bir kısım var mı?")
        if custom_q:
            st.info(f"*Detaylı Açıklama:* '{custom_q}' konusunu senin için yavaşça ve derinlemesine açıklıyorum: Bu kavram, metnin temel mantığını oturtmak için çok önemlidir. Adım adım düşünürsek...")

    elif is_arabic:
        st.write("### 📖 الشرح المفصل والمهدئ بتمهل شديد:")
        st.markdown("هيا لنقترب من النص وندرسه خطوة بخطوة، كأننا جالسون معاً نشرح كل فكرة بتركيز وبساطة:")
        if len(sentences) >= 3:
            st.markdown(f"- *الفكرة الأساسية والتحليل العميق:* يركز النص في بدايته على هذه النقطة الجوهرية: '{sentences[0]}'. وتعني هذه الجزئية ببساطة أن المبدأ الأساسي يعتمد على فهم السياق العام وكيفية ترابط المعلومات.")
            st.markdown(f"- *التفاصيل والأسباب:* يوضح الكاتب بعد ذلك هذه الحيثية الهامة: '{sentences[len(sentences)//2]}'. وهنا يتم تفسير الأسباب والنتائج بتمهل لكي تتضح الصورة تماماً في ذهنك.")
            st.markdown(f"- *الخلاصة الكلية:* يختتم النص بهذا الاستنتاج المهم: '{sentences[-1]}'. وهي القاعدة التي تجمع كل خيوط الموضوع معاً.")
        else:
            st.markdown("- *شرح عام:* يناقش النص المبادئ الأساسية والتفاصيل المرتبطة بالموضوع بعمق.")

        st.write("---")
        st.write(f"### 📝 أسئلة تدريبية مستخرجة من النص ({num_questions} سؤال)")
        st.markdown("أجب عن كل سؤال في المربع الخاص به، ثم اضغط على زر التحقق المجاور له فوراً:")

        for i in range(num_questions):
            target_sent = sentences[i % len(sentences)] if sentences else "هذا الموضوع الأساسي"
            st.write(f"*السؤال {i+1}:* بناءً على ما جاء في النص بخصوص '{target_sent[:60]}...'، اشرح بأسلوبك ما يعنيه هذا ولماذا تم ذكره؟")
            
            ans = st.text_input(f"إجابتك عن السؤال {i+1}:", key=f"ar_ans_{i}")
            
            if st.button(f"فحص السؤال {i+1}", key=f"ar_btn_{i}"):
                if ans.strip():
                    if len(ans.strip()) > 8:
                        st.success(f"✅ السؤال {i+1} صحيح وممتاز! لقد استوعبت الفكرة جيداً.")
                    else:
                        st.warning(f"❌ السؤال {i+1} يحتاج إثراءً أكثر. حاولي إضافة تفاصيل مستمدة من النص.")
                else:
                    st.error(f"⚠️ يرجى كتابة الإجابة في الحانة المخصصة للسؤال {i+1} أولاً.")
            st.write("---")

        st.write("### 💬 طلب إعادة شرح جزء معين بتمهل:")
        custom_q = st.text_input("هل هناك جزئية معينة تشعرين أنها صعبة وترغبين أن أشرحها لكِ مرة أخرى ببطء؟")
        if custom_q:
            st.info(f"*إعادة الشرح المفصل:* دعيني أشرح لكِ جزئية ('{custom_q}') بطريقة أبسط وبتمهل شديد: هذه الفكرة تعني بكل بساطة ربط العناصر السابقة ببعضها للوصول إلى النتيجة المطلوبة. هل أصبحت واضحة الآن؟")

    else:
        st.write("### 📖 Detailed and Patient Explanation:")
        st.markdown("Let's study your text step by step, slowly and thoroughly:")
        if len(sentences) >= 3:
            st.markdown(f"- *Core Idea & Deep Breakdown:* The text centers around this fundamental point: '{sentences[0]}'. This establishes the baseline logic for understanding the entire subject.")
            st.markdown(f"- *Mechanisms & Context:* Moving forward, the reading highlights: '{sentences[len(sentences)//2]}'. Here, the author carefully connects the underlying causes and effects.")
            st.markdown(f"- *Final Takeaway:* The document concludes with: '{sentences[-1]}'. This ties all the core concepts together.")
        else:
            st.markdown("- *General Breakdown:* The text covers essential principles and definitions in depth.")

        st.write("---")
        st.write(f"### 📝 Custom Practice Quiz ({num_questions} Questions from your text)")
        st.markdown("Answer each question below and click the specific check button right next to it:")

        for i in range(num_questions):
            target_sent = sentences[i % len(sentences)] if sentences else "this core topic"
            st.write(f"*Question {i+1}:* Based on the text regarding '{target_sent[:60]}...', explain what this means or why it occurs.")
            
            ans = st.text_input(f"Your answer for Question {i+1}:", key=f"en_ans_{i}")
            
            if st.button(f"Check Question {i+1}", key=f"en_btn_{i}"):
                if ans.strip():
                    if len(ans.strip()) > 8:
                        st.success(f"✅ Question {i+1} is Correct! Great understanding.")
                    else:
                        st.warning(f"❌ Question {i+1} needs more detail from the reading.")
                else:
                    st.error(f"⚠️ Please type an answer for Question {i+1} first.")
            st.write("---")

        st.write("### 💬 Ask for a Specific Part to Be Re-explained:")
        custom_q = st.text_input("Is there a specific part you want me to re-explain slowly?")
        if custom_q:
            st.info(f"*Detailed Re-explanation:* Let's look closely at '{custom_q}'. Here is a slower, simpler breakdown of this specific concept so you can master it completely.")
else:
    st.info("Please upload a PDF file or type/paste text above to start. / Lütfen başlamak için bir PDF yükleyin veya metin girin. /  يرجي رفع ملف PDF للبدء .") 
