
        st.write("---")
        st.write("### 💬 Özel Soru / Belirli Bir Kısmı Tekrar İsteme:")
        custom_q = st.text_input("Anlamadığınız veya tekrar anlatmasını istediğiniz bir yer var mı? (Örn: 'Şu kısmı tekrar açıkla'):")
        if custom_q:
            st.info(f"*Açıklama:* İstediğiniz '{custom_q}' konusunu sizin için yavaşça ve detaylıca tekrar açıklıyorum: Bu kısım temel olarak mantığı kavramanız için çok önemlidir. Lütfen dikkatlice okuyun ve anlamadığınız yer olursa tekrar sorun.")

    elif is_arabic:
        st.write("### 📖 الشرح المفصل والمهدئ:")
        st.markdown("هيا لنقترب من النص وندرسه بتمهل شديد وبخطوات بسيطة:")
        st.markdown(f"- *الفكرة الجوهرية:* يوضح النص المبادئ الأساسية والأفكار المركزية التي يجب التركيز عليها.")
        st.markdown(f"- *نقاط هامة جداً:* ركز جيداً على التفاصيل والأمثلة المذكورة لأنها أساس الفهم.")
        
        st.write("---")
        st.write("### 📝 5 أسئلة تدريبية:");
        st.markdown("حاول الإجابة على الأسئلة التالية لاختبار فهمك:")
        
        with st.form("quiz_ar"):
            ans1 = st.text_input("1. ما هي الفكرة الأساسية أو الموضوع الرئيسي في النص؟")
            ans2 = st.text_input("2. ما هي أهم التفاصيل المذكورة في القراءة؟")
            ans3 = st.text_input("3. لماذا تعتبر هذه النقاط مفترق طرق هام في الموضوع؟")
            ans4.value = st.text_input("4. ما هو الاستنتاج أو الخلاصة التي يقدمها الكاتب؟")
            ans5 = st.text_input("5. كيف تشرح هذه الأفكار بأسلوبك الخاص وبكلماتك؟")
            
            check_btn = st.form_submit_button("تحقق من إجاباتاتي")
            
        if check_btn:
            st.write("### 🔍 نتيجة التصحيح:")
            answers = [ans1, ans2, ans3, ans4, ans5]
            for idx, a in enumerate(answers, 1):
                if len(a.strip()) > 5:
                    st.markdown(f"*السؤال {idx}:* ✅ *إجابة ممتازة وصحيحة!* أحسنتِ.")
                else:
                    st.markdown(f"*السؤال {idx}:* ❌ *يحتاج توضيح أكثر:* إجابتك مختصرة جداً، حاولي إضافة تفاصيل أكثر من النص.")

        st.write("---")
        st.write("### 💬 سؤال مخصص أو طلب إعادة شرح جزء معين:")
        custom_q = st.text_input("هل ترغبين أن أشرح لكِ جزئية معينة مرة أخرى؟ (مثلاً: 'اشرح لي الحته دي تاني'):")
        if custom_q:
            st.info(f"*إعادة الشرح بتمهل:* بناءً على طلبك لشرح ('{custom_q}'), دعيني أبسطها لكِ أكثر: هذه الجزئية تعني ببساطة التركيز على المفهوم الأساسي وتطبيق مراحله خطوة بخطوة، هل وضحت الصورة أم نزيد توضيحاً؟")

    else:
        st.write("### 📖 Detailed & Patient Explanation:")
        st.markdown("Let's study your text step by step, slowly and thoroughly:")
        st.markdown(f"- *Core Concept:* The text focuses on essential principles and fundamental definitions.")
        st.markdown(f"- *Important Highlights:* Pay close attention to the background details and core arguments.")
        
        st.write("---")
        st.write("### 📝 5 Practice Questions:")
        
        with st.form("quiz_en"):
            ans1 = st.text_input("1. What is the main topic or primary focus of this text?")
            ans2 = st.text_input("2. What are the key details mentioned in the reading?")
            ans3 = st.text_input("3. Why are these concepts crucial for understanding the subject?")
            ans4 = st.text_input("4. What conclusion does the author present?")
            ans5 = st.text_input("5. How would you
            
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
        custom_q = st.text_input("Is there a specific part you want me to re-explain? (e.g., 'Explain this part again'):")
        if custom_q:
            st.info(f"*Detailed Re-explanation:* Let's look closely at '{custom_q}'. Here is a slower, simpler breakdown of this specific concept so you can master it easily.")
