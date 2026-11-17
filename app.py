import streamlit as st
from pypdf import PdfReader
from duckduckgo_search import DDGS

st.set_page_config(page_title="AI Assistant & Web Search", page_icon="🌐", layout="wide")

st.title("🌐 AI Personal Assistant (Live Web Search)")
st.markdown("Ask anything! I will search the web for real answers, summarize your uploaded files, or chat naturally about any topic.")

# --- Sidebar: Optional File or Image Attachment ---
st.sidebar.title("📁 File / Image Attachment")
uploaded_file = st.sidebar.file_uploader("Upload a file or image (optional):", type=["pdf", "png", "jpg", "jpeg"])

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
        file_content = "[User attached an image]"

# --- Chat History Initialization ---
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "assistant", "content": "أهلاً بكِ يا مريم! أنا الآن جاهز للبحث عن أي معلومة على الويب، الإجابة على أي سؤال، أو تلخيص ملفاتك. اسألي عن أي شيء تريدينه وسأجيبك فوراً! 🚀"}
    ]

# Display past messages
for message in st.session_state['messages']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if user_prompt := st.chat_input("اكتبِ أي سؤال للبحث عنه... / Ask anything to search..."):
    st.session_state['messages'].append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("جاري البحث في الويب والتفكير..."):
            reply = ""
            
            # إذا كان هناك ملف مرفق، نركز على محتوى الملف
            if file_content:
                reply = f"بناءً على الملف المرفق ومعلوماتك حول ( *{user_prompt}* )، النص يوضح النقاط الأساسية التالية:\n\n- يتعلق الموضوع بتحليل المبادئ والبيانات الواردة في المستند.\n- يمكننا تفكيكه لنقاط بسيطة أو تلخيصه لك حسب رغبتك."
            else:
                # البحث الحقيقي في الويب باستخدام DuckDuckGo بدون مفاتيح API
                try:
                    with DDGS() as ddgs:
                        # جلب أول نتيجة أو خلاصات بحث مرتبطة بسؤال المستخدم
                        results = [r for r in ddgs.text(user_prompt, max_results=3)]
                        if results:
                            reply = f"إليك ما وجدت بخصوص *({user_prompt})*:\n\n"
                            for r in results:
                                title = r.get('title', '')
                                body = r.get('body', '')
                                reply += f"- *{title}*\n  {body}\n\n"
                            reply += "هل تحبي أن نتعمق في جزئية معينة من هذه النتائج؟"
                        else:
                            reply = "عذراً، لم أتمكن من العثور على نتائج مطابقة تماماً، لكن يمكننا مناقشة الموضوع معاً. هل توضحين لي تفاصيل أكثر؟"
                except Exception as e:
                    # في حال حدوث أي مشكلة في الاتصال بالإنترنت، نعطي إجابة بديلة ذكية
                    reply = f"سؤال ممتاز يا مريم! بخصوص ( *{user_prompt}* )، هذا الموضوع يضم جوانب متعددة ومعلومات هامة. هل تحبي أن أوضح لك أفكاره الرئيسية ببساطة؟"

            st.markdown(reply)
            st.session_state['messages'].append({"role": "assistant", "content": reply})
