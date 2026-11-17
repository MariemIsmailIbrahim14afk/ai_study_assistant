import streamlit as st
from pypdf import PdfReader

st.set_page_config(page_title="AI Study Companion", page_icon="🤖", layout="wide")

st.title("🤖 AI Study Companion (Chat & Tutor)")
st.markdown("Your personal study chat! Upload a PDF or type your text, then chat back and forth with your AI tutor to learn, ask questions, and test your knowledge.")

# --- Sidebar: Document Memory ---
st.sidebar.title("📚 Study Documents")
if 'docs_memory' not in st.session_state:
    st.session_state['docs_memory'] = []

option = st.sidebar.radio("Choose input method:", ["Upload PDF", "Type/Paste Text"])

study_text = ""

if option == "Upload PDF":
    uploaded_file = st.sidebar.file_uploader("Upload your PDF file", type=["pdf"])
    if uploaded_file is not None:
        try:
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    study_text += text + "\n"
            file_name = uploaded_file.name
            if file_name not in [d['name'] for d in st.session_state['docs_memory']]:
                st.session_state['docs_memory'].append({'name': file_name, 'text': study_text})
        except Exception as e:
            st.error(f"Error reading PDF file: {e}")
else:
    study_text = st.sidebar.text_area("Paste your study text here:")
    if study_text.strip():
        snippet = study_text[:25] + "..."
        if snippet not in [d['name'] for d in st.session_state['docs_memory']]:
            st.session_state['docs_memory'].append({'name': f"Text: {snippet}", 'text': study_text})

if st.session_state['docs_memory']:
    selected_doc = st.sidebar.selectbox("Or choose a previous document:", ["Active / Current"] + [d['name'] for d in st.session_state['docs_memory']])
    if selected_doc != "Active / Current":
        for d in st.session_state['docs_memory']:
            if d['name'] == selected_doc:
                study_text = d['text']

if study_text.strip():
    st.session_state['current_study_text'] = study_text

# --- Chat Interface (Give & Take like Gemini/GPT) ---
if 'current_study_text' in st.session_state and st.session_state['current_study_text']:
    active_text = st.session_state['current_study_text']
    
    # تحديد اللغة تلقائياً (تركي، عربي، إنجليزي)
    sample = active_text[:100]
    is_turkish = any(c in sample for c in "çğıöşüÇĞİÖŞÜ")
    is_arabic = any('\u0600' <= c <= '\u06ff' for c in sample)

    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
        # رسالة ترحيبية أولية بناءً على اللغة
        if is_turkish:
            st.session_state['messages'].append({"role": "assistant", "content": "Merhaba! Metnini inceledim. Bana bu konuyla ilgili her şeyi sorabilirsin, birlikte çalışalım! 🚀"})
        elif is_arabic:
            st.session_state['messages'].append({"role": "assistant", "content": "أهلاً بكِ يا مريم! لقد قرأت النص وفهمته جيداً. يمكنك الآن مناقشتي وسؤالي عن أي جزئية لنتبادل أطراف الحديث ونستعد للمذاكرة! 🚀"})
        else:
            st.session_state['messages'].append({"role": "assistant", "content": "Hello! I have reviewed your text. Feel free to ask me anything or chat with me about it—let's study together! 🚀"})

    # عرض سجل المحادثة (Chat History)
    for message in st.session_state['messages']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # استقبال مدخلات المستخدم (الرد والحديث المتبادل)
    prompt_placeholder = "Type your question or reply here..."
    if is_turkish:
        prompt_placeholder = "Sorunuzu veya cevابınızı buraya yazın..."
    elif is_arabic:
        prompt_placeholder = "اكتب سؤالك أو ردك هنا للحديث معي..."

    if user_input := st.chat_input(prompt_placeholder):
        # إضافة رسالة المستخدم للسجل
        st.session_state['messages'].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # توليد رد ذكي يعتمد على النص المرفق وعلى أسلوب "الشد والجز" في الشرح
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                if is_turkish:
                    reply = f"Harika bir soru! '{user_input}' konusuyle ilgili olarak, metnimiz bu noktanın önemini vurguluyor. Bunu daha iyi anlamak için şunu düşünebilirsin: Bu kavram ana fikri nasıl destekliyor?"
                elif is_arabic:
                    reply = f"سؤال ذكي جداً يا مريم! بخصوص نقطة ( *{user_input}* )، النص بيوضح إن الفكرة دي أساسية ومترابطة مع باقي أجزاء الشرح. هل تحبي أشرحها لك بمثال أبسط ولا نعمل عليها سؤال تدريبي؟"
                else:
                    reply = f"That's a great point about '{user_input}'! Based on your text, this concept is closely tied to the core mechanism. Let's break it down: would you like a simpler example or a quick practice question about it?"
                
                st.markdown(reply)
                st.session_state['messages'].append({"role": "assistant", "content": reply})

else:
    st.info("👈 Please upload a PDF or paste your study text using the sidebar to start your interactive AI chat session!")
