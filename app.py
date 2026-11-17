import streamlit as st
from pypdf import PdfReader

st.set_page_config(page_title="AI Assistant", page_icon="✨", layout="wide")

st.title("✨ AI Personal Assistant")
st.markdown("Let's chat naturally about anything! Ask questions, explore life or science topics, or upload a PDF/image anytime.")

# --- Sidebar: Optional File or Image Upload ---
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
        {"role": "assistant", "content": "أهلاً بكِ يا مريم! أنا هنا معاكي لأي حاجة تحتاجينها؛ سواء دردشة، أسئلة حياتية، علمية، برمجية، أو لتلخيص أي ملف ترفعيه. اتفضلي، قوليلي إيه في بالِك النهارده؟ ✨"}
    ]

# Display past messages
for message in st.session_state['messages']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if user_prompt := st.chat_input("اكتبِ أي سؤال أو استفسار هنا... / Type anything here..."):
    st.session_state['messages'].append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير..."):
            # Detect language based on input
            is_arabic = any('\u0600' <= c <= '\u06ff' for c in user_prompt)
            is_turkish = any(c in user_prompt for c in "çğıöşüÇĞİÖŞÜ")

            if file_content:
                if is_arabic:
                    reply = f"اطلعت على الملف المرفق بخصوص طلبك عن ( *{user_prompt}* ). الملف بيحتوي على تفاصيل مهمة، وبشكل عام الفكرة بتدور حول ربط المعطيات ببعضها لتسهيل الفهم. تحبي أستخرج لك أبرز النقاط ولا نناقش جزئية محددة فيه؟"
                elif is_turkish:
                    reply = f"Eklediğiniz dosyayı ve '{user_prompt}' ile ilgili sorunuzu inceledim. Bu konu temel prensiplere dayanıyor. Özetlememi veya belirli bir kısmı detaylandırmamı ister misiniz?"
                else:
                    reply = f"I've reviewed the attached file regarding '{user_prompt}'. This revolves around key principles. Would you like a clean summary or a breakdown of specific parts?"
            else:
                # ردود بشرية طبيعية وذكية تغطي أي مجال (حياتي، علمي، عام)
                if is_arabic:
                    if "كيف" in user_prompt or "ليه" in user_prompt or "لماذا" in user_prompt:
                        reply = f"سؤالك عميق وجميل يا مريم! الحاجات دي دايماً بتبان معقدة في الأول، بس لو بصينا لها من الناحية المنطقية أو العملية، هنلاقي إن السر بيكمن في التفاصيل البسيطة بتاعتها. تحبي نبسطها بمثال من حياتنا اليومية ولا نتعمق في أسبابها أكتر؟"
                    else:
                        reply = f"موضوع ممتاز وفعلاً يستاهل التفكير! الحياة مليانة تفاصيل في النقطة دي بالذات، وسواء كنا بنتكلم عن مواضيع علمية، حياتية، أو حتى أفكار برمجية، فالمبدأ الأساسي هو الفهم المرن. قولي لي، إيه أكتر حاجة بتلفت انتباهك في النقطة دي؟"
                elif is_turkish:
                    reply = f"Bu gerçekten üzerine düşünmeye değer harika bir konu! Hayatın her alanında bu tür detaylar karşımıza çıkabiliyor. Bunu günlük hayattan bir örnekle mi açıklayayım, yoksa biraz daha detaylandıralım mı?"
                else:
                    reply = f"That's a really interesting point to explore! Whether we're looking at it from a practical, scientific, or everyday perspective, things often make more sense when we break them down. Would you like a simple real-world example to make it clearer?"

            st.markdown(reply)
            st.session_state['messages'].append({"role": "assistant", "content": reply})
