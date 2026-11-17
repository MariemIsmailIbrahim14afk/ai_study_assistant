import streamlit as st
from pypdf import PdfReader

st.set_page_config(page_title="AI Study Assistant & Tutor", page_icon="💡", layout="wide")

st.title("💡 AI Study Assistant & Smart Tutor")
st.markdown("Ask anything, discuss academic or programming topics, or upload a PDF/image to analyze and summarize it together!")

# --- Sidebar: File & Image Uploader ---
st.sidebar.title("📁 File / Image Attachment")
uploaded_file = st.sidebar.file_uploader("Upload a PDF or image to study:", type=["pdf", "png", "jpg", "jpeg"])

file_content = ""
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        try:
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    file_content += t + "\n"
            st.sidebar.success("PDF uploaded and loaded successfully!")
        except Exception as e:
            st.sidebar.error(f"Error reading PDF: {e}")
    else:
        st.sidebar.success("Image uploaded successfully!")
        file_content = "[Image attached by user]"

# --- Chat History ---
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "assistant", "content": "Hello! I'm your study assistant. Ask me any question, chat about science or programming, or attach a file to summarize it. Let's study! 🚀"}
    ]

# Display messages
for message in st.session_state['messages']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if user_prompt := st.chat_input("Ask a question, request a summary, or type anything..."):
    st.session_state['messages'].append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Detect language
            is_arabic = any('\u0600' <= c <= '\u06ff' for c in user_prompt)
            is_turkish = any(c in user_prompt for c in "çğıöşüÇĞİÖŞÜ")

            if file_content:
                if is_arabic:
                    reply = f"لقد اطلعت على الملف المرفق. بناءً على سؤالك أو طلبك ( *{user_prompt}* )، النص يحتوي على تفاصيل مهمة. هل تحب أن ألخص لك النقاط الرئيسية أو أشرح لك جزءاً معيناً منه؟"
                elif is_turkish:
                    reply = f"Eklenen belgeyi inceledim. '{user_prompt}' ile ilgili olarak, bu metin temel kavramları açıklamaktadır. Özetlememi veya detaylandırmamı ister misiniz?"
                else:
                    reply = f"I have reviewed the attached file. Regarding your request about '{user_prompt}', would you like a detailed summary or a breakdown of the key points?"
            else:
                if is_arabic:
                    reply = f"سؤال رائع يا مريم! بخصوص ( *{user_prompt}* )، هذا الموضوع يعتمد على قواعد أساسية واضحة. سواء كان في البرمجة، العلوم، أو أي مادة دراسية، يمكننا تفكيكه معاً ببساطة. هل تحبي أن أضرب لك مثالاً عليه أم نتعمق في شرحه؟"
                elif is_turkish:
                    reply = f"Harika bir soru! '{user_prompt}' konusu oldukça önemlidir ve mantığı oldukça basittir. Bunu daha detaylı açıklamamı veya bir örnek vermemi ister misin?"
                else:
                    reply = f"That's a fascinating question about '{user_prompt}'! Whether it's science, programming, or general studies, we can break it down easily. Would you like a practical example or a deeper explanation?"

            st.markdown(reply)
            st.session_state['messages'].append({"role": "assistant", "content": reply})
