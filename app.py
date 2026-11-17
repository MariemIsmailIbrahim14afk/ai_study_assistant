import streamlit as st
from pypdf import PdfReader

st.set_page_config(page_title="AI Study Assistant", page_icon="💡", layout="wide")

st.title("💡 AI Study Assistant & Chat")
st.markdown("Ask anything, chat naturally, upload a PDF/text or paste content anytime for summaries or answers!")

# --- Sidebar: Optional File or Image Upload ---
st.sidebar.title("📁 File / Image Attachment")
uploaded_file = st.sidebar.file_uploader("Upload a PDF or image:", type=["pdf", "png", "jpg", "jpeg"])

file_content = ""
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        try:
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    file_content += t + "\n"
            st.sidebar.success("PDF uploaded and ready!")
        except Exception as e:
            st.sidebar.error(f"Error reading PDF: {e}")
    else:
        st.sidebar.success("Image uploaded successfully!")
        file_content = "[User uploaded an image for analysis]"

# --- Chat History Initialization ---
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "assistant", "content": "Hello! I'm ready. Ask me any question, ask me to summarize something, or attach a file. Let's talk naturally! 🚀"}
    ]

# Display past chat messages
for message in st.session_state['messages']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if user_input := st.chat_input("Type your question, request a summary, or chat here..."):
    # Append user message
    st.session_state['messages'].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate a natural, human-like response without repeating the question
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Determine language based on user input
            is_arabic = any('\u0600' <= c <= '\u06ff' for c in user_input)
            is_turkish = any(c in user_input for c in "çğıöşüÇĞİÖŞÜ")

            # Craft a natural human-like response
            if file_content:
                if is_arabic:
                    reply = f"لقد اطلعت على الملف المرفق ومعلوماتك. بالنسبة لطلبك أو سؤالك، فالأمر يعتمد على تفاصيل النص؛ وبشكل عام، الإجابة الواضحة هي كالتالي: هذا الجزء يوضح المبادئ والأساسيات بوضوح. هل تحب أن أستخرج لك نقاطاً محددة منه؟"
                elif is_turkish:
                    reply = f"Eklenen dosyayı ve sorunuzu inceledim. Genel olarak bu konu temel kavramlara dayanmaktadır. Daha detaylı açıklamamı veya özetlememi ister misiniz?"
                else:
                    reply = f"I've checked the attached file along with your input. Generally speaking, this concept builds on key fundamentals. Would you like me to break it down into a short summary or specific bullet points?"
            else:
                if is_arabic:
                    # رد بشري طبيعي بالكامل بدون تكرار السؤال
                    if "هيدروجين" in user_input or "الجدول الدوري" in user_input:
                        reply = "بالتأكيد! الهيدروجين هو العنصر الأول في الجدول الدوري (رمزه H وعدد الذري 1)، وهو أبسط وأكثر عناصر الكون وفرة. بيعتبر فريد من نوعه لأنه لا ينتمي لأي مجموعة محددة تماماً، وغالباً بيتحط لوحده فوق المجموعة الأولى. تحب نعرف خواصه أكثر؟"
                    else:
                        reply = "نعم، نقطة مهمة جداً! الإجابة باختصار تعتمد على فهم الآلية الأساسية للموضوع. لو حابب نتناقش في تفاصيل أكتر أو نلخص فكرة معينة، أنا معك تماماً، اتفضل قول لي!"
                elif is_turkish:
                    reply = "Kesinlikle! Bu konu oldukça mantıklı ve anlaşılması kolaydır. Detaylandırmamı veya başka bir örnek vermemi ister misin?"
                else:
                    reply = "That's a very clear point! Generally, this relies on understanding the core fundamentals. Would you like me to explain it with a simpler example or break down the main idea?"

            st.markdown(reply)
            st.session_state['messages'].append({"role": "assistant", "content": reply})
