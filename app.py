import streamlit as st
import google.generativeai as genai

# إعداد الصفحة والواجهة الإنجليزية
st.set_page_config(page_title="MARIEM'S Summary & Quiz App", page_icon="📚", layout="centered")

st.title("MARIEM'S Summary & Quiz App")
st.write("Welcome to your smart AI study assistant! Upload a document or type text to get quick explanations, summaries, and rigorous randomized quizzes in your input language.")

# إعداد مفتاح الـ API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    api_key = st.text_input("Enter your Google Gemini API Key:", type="password")
    if api_key:
        genai.configure(api_key=api_key)

# اختيار طريقة الإدخال
input_method = st.radio("Choose input method / Giriş yöntemi / طريقة الإدخال", ["Upload PDF", "Type/Paste Text"])

input_text = ""

if input_method == "Upload PDF":
    uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])
    if uploaded_file is not None:
        st.success("PDF uploaded successfully!")
        input_text = "Sample extracted text from PDF." 
else:
    input_text = st.text_area("Type or paste your study text here:")

# اختيار عدد الأسئلة
num_questions = st.selectbox("Select number of questions / Soru sayısı / عدد الأسئلة:", [3, 5, 10], index=1)

if st.button("Generate Explanation & Quiz"):
    if not input_text:
        st.warning("Please provide some text or upload a PDF first!")
    else:
        try:
            # استخدام الموديل القياسي المدعوم تماماً لتفادي أي خطأ 404
            model = genai.GenerativeModel("models/gemini-1.5-flash")
            
            prompt = f"""
You are an expert AI quiz generator and study assistant. 
1. Read the provided text/document carefully and extract key facts, numbers, names, and specific details.
2. Provide a *Quick & Clear Explanation* breaking down the core concepts.
3. Generate {num_questions} rigorous and direct *quiz questions* based strictly on the facts, numbers, and data in the text. 
   - CRITICAL RULE FOR QUESTIONS: Do NOT ask vague or general questions like "What is the main idea?". Instead, ask direct questions that test specific information, facts, or technical details from the text.
4. CRITICAL RULE FOR LANGUAGE: You MUST generate the entire output (explanation, questions, options, and feedback) *in the exact same language as the input text provided by the user* (whether it is Arabic, English, Turkish, French, Chinese, or any other language).
5. CRITICAL RULE FOR OPTIONS: Randomize the correct answer position thoroughly among options (A, B, C, D) for multiple-choice questions—NEVER keep the correct answer always on option A. For True/False questions, randomly alternate the correct answer between True and False.

Input Text:
{input_text}
"""
            with st.spinner("Generating explanation and direct quiz using AI..."):
                response = model.generate_content(prompt)
                st.markdown("### 📖 Study Results & Direct Quiz:")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
