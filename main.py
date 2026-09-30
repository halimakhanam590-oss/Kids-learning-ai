import streamlit as st
import google.generativeai as genai
import os

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="Kids Learning AI - Worldwide",
    page_icon="🧒",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. API KEY - USER ER KACHE CHAIBE NA ---
# Streamlit Cloud -> Settings -> Secrets e GEMINI_API_KEY = "AIza..." bosaba
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    API_KEY = os.getenv("GEMINI_API_KEY", "")

if not API_KEY:
    st.error("⚠️ GEMINI_API_KEY set kora nai! Streamlit Secrets e add koro.")
    st.info("Local e test korle: export GEMINI_API_KEY='your_key'")
    st.stop()

genai.configure(api_key=API_KEY)
model_name = "gemini-1.5-flash"

# --- 3. SESSION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "count" not in st.session_state:
    st.session_state.count = 0
if "is_pro" not in st.session_state:
    st.session_state.is_pro = False

# --- 4. SIDEBAR - CHATGPT STYLE SETTINGS ---
with st.sidebar:
    st.title("⚙️ Settings")
    
    lang = st.selectbox("🌍 Language / Bhasha", [
        "Sundor Bangla (সুন্দর বাংলা)",
        "English",
        "Hindi - हिन्दी",
        "Urdu - اردو",
        "Arabic - العربية",
        "Spanish - Español",
        "French - Français",
        "Malay - Bahasa Melayu"
    ], index=0)
    
    who = st.selectbox("👤 Tumi ke?", [
        "Baccha (5-10 bochor) / Kid",
        "Kishor (11-16 bochor) / Teen",
        "Boro Manush / Baba-Ma / ABBA"
    ], index=0)
    
    style = st.select_slider("🎭 Kotha bolar dhoron", 
        options=["Moja-r / Funny", "Normal / Friendly", "ABBA-r moto / Caring & Strict"],
        value="Normal / Friendly"
    )
    
    st.divider()
    st.subheader("💎 Pro Plan")
    if st.session_state.is_pro:
        st.success("✅ Pro Active - Unlimited Chat")
    else:
        st.metric("Free Messages", f"{st.session_state.count} / 10")
        st.caption("Pro kinle unlimited, voice, sob language paba!")
        
        t1, t2, t3 = st.tabs(["bKash", "PayPal", "Card"])
        with t1:
            st.write("**bKash - 350 Tk**")
            st.code("017XXXXXXXX - Send Money")
            # Tomar bKash link ekhane bosao
            st.link_button("💳 bKash Payment Link", "https://shop.bkash.com", use_container_width=True)
            if st.button("✅ bKash Payment Done", use_container_width=True):
                st.session_state.is_pro = True
                st.balloons()
                st.rerun()
        with t2:
            st.write("**PayPal - $2.99**")
            st.link_button("🌍 Pay with PayPal", "https://paypal.me/yourname/2.99", use_container_width=True)
            if st.button("✅ PayPal Done", use_container_width=True):
                st.session_state.is_pro = True
                st.rerun()
        with t3:
            st.write("**Card - $2.99 (Stripe)**")
            st.link_button("💳 Pay with Card", "https://buy.stripe.com/test_xxx", use_container_width=True)
            if st.button("✅ Card Done", use_container_width=True):
                st.session_state.is_pro = True
                st.rerun()
    
    if st.button("🗑️ Clear Chat / Chat Muso", use_container_width=True):
        st.session_state.messages = []
        st.session_state.count = 0
        st.rerun()

# --- 5. PROMPT ENGINE - REAL LIFE ---
def build_system_prompt(who_is, language, talking_style):
    p = ""
    if "Baccha" in who_is or "Kid" in who_is:
        p += "You are a 6-year-old kid's best friend. Talk super cute, simple, fun with lots of emojis. Explain everything like a story. Never use hard words. "
    elif "Kishor" in who_is or "Teen" in who_is:
        p += "You are a cool, smart elder brother. Talk friendly, cool, a bit funny but educational for teens. "
    else:
        p += "You are a respectful, wise ABBA / father figure. Talk with respect, love, responsibility. Guide parents how to teach kids. Use respectful tone. "
    
    # Language - Strong instruction
    if "Bangla" in language:
        p += "You MUST speak in beautiful, natural, shuddho, pranobonto Bangla. Not robotic Google Translate Bangla. Like a real Bangladeshi person from Dhaka. Use Bangla fully. "
    elif "Hindi" in language:
        p += "Speak in beautiful natural Hindi. "
    elif "Urdu" in language:
        p += "Speak in beautiful natural Urdu. "
    elif "Arabic" in language:
        p += "Speak in beautiful natural Arabic. "
    else:
        p += f"Speak in {language}. "

    if "Funny" in talking_style:
        p += "Be very funny, use jokes, emojis, stories."
    elif "Caring" in talking_style or "ABBA" in talking_style:
        p += "Be caring but a little strict, like a loving father who wants best for his child."
    
    p += " You are Kids Learning AI. Your goal is to teach kids: math, science, Bangla, English, golpo, quran, general knowledge. Never say bad words. Be 100% safe for kids. Be real-life."
    return p

# --- 6. MAIN CHAT UI ---
st.title("🧒🌍 Kids Learning AI")
st.caption("Bacchader jonno nirapod, mojar, real-life bondhu | Safe AI for Kids Worldwide")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Limit
if not st.session_state.is_pro and st.session_state.count >= 10:
    st.warning("🔒 Free limit sesh! Sidebar theke Pro kino - bKash / PayPal / Card")
    st.stop()

if prompt := st.chat_input("Ekta prosno koro / Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Vabchi... / Thinking..."):
            try:
                sys_prompt = build_system_prompt(who, lang, style)
                model = genai.GenerativeModel(model_name, system_instruction=sys_prompt)
                chat = model.start_chat(history=[])
                
                # Last 8 messages for context
                context = "\n".join([f"{x['role']}: {x['content']}" for x in st.session_state.messages[-8:]])
                response = chat.send_message(context)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.session_state.count += 1
            except Exception as e:
                st.error(f"Error: {e}")
      
