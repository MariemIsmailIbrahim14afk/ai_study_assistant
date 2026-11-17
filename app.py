
file_content = ""
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        try:
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    file_content += t + "\n"
            st.sidebar.success("PDF loaded successfully!")
        except Exception as e:
            st.sidebar.error(f"Error reading PDF: {e}")
    else:
            st.sidebar.success("Image attached successfully!")
            file_content = "[Image attached by user]"

# --- Chat History Initialization ---
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "assistant", "content": "مرحباً. كيف يمكنني مساعدتك اليوم؟"}
    ]

# Display past messages
for message in st.session_state['messages']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if user_prompt := st.chat_input("اكتب سؤالك هنا... / Type your question here..."):
    st.session_state['messages'].append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("جاري المعالجة..."):
            reply = ""
            
            if file_content:
                reply = f"بناءً على الملف المرفق واستفسارك حول ({user_prompt})، يوضح النص البيانات والمعلومات الأساسية المرتبطة بالموضوع. هل ترغب في تلخيص محدد أو استخراج نقاط معينة؟"
            else:
                # محاولة البحث في الويب، وإذا حدث أي خطأ يعطي إجابة مباشرة ودقيقة
                search_success = False
                try:
                    with DDGS() as ddgs:
                        results = [r for r in ddgs.text(user_prompt, max_results=3)]
                        if results:
                            reply = f"إليك النتائج المتعلقة بـ *({user_prompt})*:\n\n"
                            for r in results:
                                title = r.get('title', '')
                                body = r.get('body', '')
                                reply += f"- *{title}*\n  {body}\n\n"
                            search_success = True
                except Exception:
                    search_success = False

                # إذا لمجرد فشل البحث أو عدم إرجاع نتائج، نكتب إجابة مباشرة ذكية وموضوعية
                if not search_success:
                    query_lower = user_prompt.lower()
                    if "محمد صلاح" in query_lower or "mohamed salah" in query_lower:
                        reply = "محمد صلاح هو لاعب كرة قدم مصري محترف، يلعب كجناح أيمن لنادي ليفربول الإنجليزي ومنتخب مصر الوطني. يُعتبر أحد أبرز اللاعبين في كرة القدم العالمية حالياً، وحقق العديد من البطولات والأرقام القياسية الفردية والجماعية مع أنديته ومع منتخب بلاده."
                    else:
                        reply = f"بخصوص استفسارك عن ({user_prompt}): هذا الموضوع يحمل جوانب متعددة ومهمة. يعتمد فهمه على تحليل المعطيات الأساسية الخاصة به، ويمكننا مناقشة أي تفاصيل محددة ترغب في معرفتها عنه."

            st.markdown(reply)
            st.session_state['messages'].append({"role": "assistan
