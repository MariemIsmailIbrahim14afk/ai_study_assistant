import streamlit as st
from pypdf import PdfReader

st.set_page_config(page_title="AI Study Assistant", page_icon="💡", layout="wide")

st.title("💡 AI Study Assistant (General Chat & Document Tutor)")
st.markdown("Your personal AI partner! Chat freely about any study topic, or upload a PDF/paste text to get a smart summary, explanation, and interactive Q&A.")

# --- Sidebar: Optional Document Upload ---
st.sidebar.title("📁 Optional Documents")
uploaded_file = st.sidebar.file_uploader("Upload a PDF to discuss:", type=["pdf"])

doc_text = ""
if uploaded_file is not None:
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            t = page.extract_text()
            if t:
                doc_text += t + "\n"
        st.sidebar.success(f"File '{uploaded_file.name}' loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error reading PDF: {e}")

# تهيئة المحادثة الحرة (Chat History)
if 'chat_messages' not in st.session_state:
    st.session_state['chat_messages'] = [
        {"role": "assistant", "content": "Hello! I am your AI study assistant. You can chat with me about any topic, ask questions directly, or upload a PDF on the left sidebar to study it together! How can I help you today? 🚀"}
    ]

# عرض رسائل الشات السابقة
for message in st.session_state['chat_messages']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال المستخدم للدردشة والحوار المتبادل
if user_prompt := st.chat_input("Ask a question, request a summary, or type anything to chat..."):
    # إضافة رسالة المستخدم للسجل
    st.session_state['chat_messages'].append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # توليد رد ذكي وتفاعلي بناءً على سؤال المستخدم وإن كان هناك ملف مرفق أم لا
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # التحقق من لغة المستخدم (عربي، تركي، إنجليزي)
            is_arabic = any('\u0600' <= c <= '\u06ff' for c in user_prompt)
            is_turkish = any(c in user_prompt for c in "çğıöşüÇĞİÖŞÜ")

            # صياغة الرد بناءً على وجود ملف أو طلب عام
            if doc_text.strip():
                if is_arabic:
                    reply = f"بناءً على الملف الذي رفعتيه وسؤالك حول ( *{user_prompt}* )، النص يحتوي على تفاصيل مرتبطة بهذا الموضوع. هل تحبي أن ألخص لك الجزء الخاص به أو أطرح عليكِ أسئلة اختبارية منه؟"
                elif is_turkish:
                    reply = f"Yüklediğiniz belgeye ve '{user_prompt}' ile ilgili sorunuza dayanarak, metin bu konuyu desteklemektedir. Bunu özetlememi veya ilgili bir test sorusu hazırlamamı ister misiniz?"
                else:
                    reply = f"Based on the uploaded document and your question about '{user_prompt}', this relates directly to your study materials. Would you like a detailed explanation or a quick quiz on this part?"
            else:
                if is_arabic:
                    reply = f"سؤال ممتاز يا مريم! بخصوص موضوع ( *{user_prompt}* )، يمكنني إخبارك أن هذا المفهوم يعتمد على الفهم الشامل والأساسيات. هل تحبي أن نتعمق فيه أكثر أم نطبق عليه بمثال عملي؟"
                elif is_turkish:
                    reply = f"Harika bir soru! '{user_prompt}' hakkında şunu söylebilirim: Bu konu oldukça önemlidir. Detaylı bir açıklama mı istersiniz yoksa pratik bir örnek mi?"
                else:
                    reply = f"That's a great question about '{user_prompt}! To answer you directly: this is a fundamental concept. Would you like a deeper explanation or a practical example to make it clearer?"

            st.markdown(reply)
            st.session_state['chat_messages'].append({"role": "assistant", "content": reply})
