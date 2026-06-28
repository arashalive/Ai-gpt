import streamlit as st
from google import genai

st.set_page_config(page_title="ابر هوش مصنوعی ترکیبی", layout="wide")
st.title("🤖 ابر هوش مصنوعی ترکیبی")

# منوی کناری برای دریافت کلید
with st.sidebar:
    st.header("⚙️ تنظیمات اتصال")
    gemini_key = st.text_input("Gemini API Key", type="password")

if not gemini_key:
    st.warning("⚠️ لطفاً ابتدا کلید API جمنای را در منوی کناری وارد کنید.")
else:
    # راه‌اندازی کلاینت با کلید وارد شده
    client = genai.Client(api_key=gemini_key)
    
    st.subheader("💬 گفتگو با هوش مصنوعی")
    user_input = st.text_input("پیام خود را بنویسید:", key="user_msg")
    
    if st.button("ارسال به هوش مصنوعی") and user_input:
        try:
            with st.spinner("در حال پردازش..."):
                # استفاده از مدل استاندارد و هماهنگ با پکیج جدید
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_input,
                )
                st.success("🤖 پاسخ هوش مصنوعی:")
                st.write(response.text)
        except Exception as e:
            st.error(f"❌ خطایی رخ داد: {e}")
            