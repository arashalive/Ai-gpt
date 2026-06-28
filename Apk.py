import streamlit as st
from google import genai
from openai import OpenAI
import os

# تنظیمات ظاهر برنامه در موبایل
st.set_page_config(page_title="Super AI", page_icon="🤖", layout="centered")

st.title("🤖 ابر هوش مصنوعی ترکیبی")
st.write("ترکیب قدرت جمنای، GPT-4o و کیفیت عکس FLUX")

# ۲. بخش تنظیمات کلیدهای امنیتی (جایگذاری کلیدها)
# می‌توانید کلیدها را مستقیم اینجا داخل کوتیشن بذارید یا از بخش Secrets استریم‌لیت استفاده کنید.
GEMINI_KEY = st.sidebar.text_input("Gemini API Key", type="password", value=os.environ.get("GEMINI_API_KEY", ""))
OPENAI_KEY = st.sidebar.text_input("OpenAI API Key", type="password", value=os.environ.get("OPENAI_API_KEY", ""))
TOGETHER_KEY = st.sidebar.text_input("Together AI Key (FLUX)", type="password", value=os.environ.get("TOGETHER_API_KEY", ""))

# شرط اجرای برنامه: حتما باید کلیدها وارد شده باشند
if not GEMINI_KEY or not TOGETHER_KEY:
    st.warning("⚠️ لطفاً ابتدا کلیدهای API را در منوی کناری (Sidebar) وارد کنید.")
else:
    # مقداردهی سرویس‌ها
    gemini_client = genai.Client(api_key=GEMINI_KEY)
    together_client = OpenAI(base_url="https://api.together.xyz/v1", api_key=TOGETHER_KEY)
    
    # منوی انتخاب حالت برنامه (دکمه‌های رادیویی فوقانی)
    mode = st.radio("چهارچوب کاری را انتخاب کنید:", ["💬 گفتگو و ساخت عکس", "🖼️ تحلیل و بررسی عکس"])

    # --- حالت اول: گفتگو و ساخت عکس ---
    if mode == "💬 گفتگو و ساخت عکس":
        user_prompt = st.text_input("پیام یا ایده عکس خود را اینجا بنویسید:")
        
        # دکمه ارسال
        if st.button("🚀 ارسال به هوش مصنوعی"):
            if user_prompt:
                with st.spinner("🧠 در حال پردازش توسط جمنای..."):
                    # تشخیص قصد کاربر
                    intent_check = gemini_client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=f"Does the user want to generate an image? Reply 'yes' or 'no': {user_prompt}"
                    )
                
                if intent_check.text.strip().lower() == 'yes':
                    with st.spinner("🎨 در حال ارتقای کیفیت و تصویرسازی با موتور FLUX..."):
                        # بهینه‌سازی پرامپت
                        prompt_eng = gemini_client.models.generate_content(
                            model='gemini-1.5-flash',
                            contents=f"Convert to detailed English prompt for FLUX.1 Pro: {user_prompt}"
                        )
                        # تولید عکس
                        image_response = together_client.images.generate(
                            prompt=prompt_eng.text,
                            model="black-forest-labs/FLUX.1-pro"
                        )
                        image_url = image_response.data[0].url
                        # نمایش عکس در اپلیکیشن
                        st.image(image_url, caption="✨ عکس تولید شده با کیفیت فوق‌العاده")
                else:
                    with St.spinner("💬 در حال پاسخ‌گویی متنی..."):
                        # گپ و گفت معمولی با جمنای
                        chat_reply = gemini_client.models.generate_content(
                            model='gemini-1.5-pro',
                            contents=user_prompt
                        )
                        st.success(chat_reply.text)

    # --- حالت دوم: تحلیل عکس ---
    elif mode == "🖼️ تحلیل و بررسی عکس":
        # باکس آپلود فایل عکس
        uploaded_file = st.file_uploader("یک عکس انتخاب یا آپلود کنید...", type=["jpg", "png", "jpeg"])
        user_question = st.text_input("سوال شما درباره این عکس (اختیاری):", value="این تصویر را کاملا تحلیل کن.")
        
        if uploaded_file and st.button("🔍 تحلیل عکس"):
            with st.spinner("👁️ در حال آنالیز تصویر..."):
                # ذخیره موقت فایل برای فرستادن به جمنای
                with open("temp_app_img.jpg", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # آپلود در سیستم گوگل و پاسخ‌دهی جمنای
                google_file = gemini_client.files.upload(file="temp_app_img.jpg")
                result = gemini_client.models.generate_content(
                    model='gemini-1.5-pro',
                    contents=[google_file, user_question]
                )
                st.info(result.text)
                
                # پاکسازی فایل موقت
                if os.path.exists("temp_app_img.jpg"):
                    os.remove("temp_app_img.jpg")