import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIG - ENGLISH ---
st.set_page_config(page_title="Kids Learning AI - Worldwide", page_icon="🧒", layout="centered", initial_sidebar_state="expanded")

# --- BEAUTIFUL BACKGROUND & SETTINGS - ENGLISH CSS ---
st.markdown("""
<style>
/* Main App Background - Beautiful Gradient */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 20% 30%, #1a2a6c, #2a3a8c 20%, #0f0c29 80%);
    background-attachment: fixed;
}
[data-testid="stHeader"] {background: rgba(0,0,0,0);}
[data-testid="stSidebar"] {
    background: rgba(10, 15, 40, 0.85) !important;
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255,255,255,0.1);
}
/* Chat bubbles Glass Effect */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
/* Title Glow */
h1 {
    background: linear-gradient(90deg, #fff, #8ec5fc, #e0c3fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    text-shadow: 0 0 30px rgba(142,197,252,0.3);
}
/* Buttons */
.stButton>button, [data-testid="stLinkButton"] a {
    border-radius: 12px !important;
    font-weight: 600;
    transition: all 0.3s;
}
.stButton>button:hover {transform: scale(1.02);}
</style>
""", unsafe_allow_html=True)

# --- API KEY ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    API_KEY = os.getenv("GEMINI_API_KEY", "")

if not API_KEY:
    st.error("⚠️ GEMINI_API_KEY is missing! Add it in Settings > Secrets")
    st.stop()

genai.configure(api_key=API_KEY)

# --- SESSION ---
if "messages" not in st.session_state: st.session_state.messages = []
if "count" not in st.session_state: st.session_state.count = 0
if "is_pro" not in st.session_state: st.session_state.is_pro = False

# --- SIDEBAR - ENGLISH SETTINGS ---
with st.sidebar:
    st.title("⚙️ Settings")
    st.caption("Customize your AI experience")
    
    lang = st.selectbox("🌍 App Language", ["English","Sundor Bangla (সুন্দর বাংলা)","Hindi - हिन्दी","Urdu - اردو","Arabic - العربية","Spanish - Español","French - Français","Malay"], index=0)
    
    who = st.selectbox("👤 Who are you?", ["Kid (5-10 years)", "Teen (11-16 years)", "Parent / ABBA (Adult)"], index=0)
    
    style = st.select_slider("🎭 Talking Style", options=["Funny & Playful","Friendly & Normal","Caring & Strict (ABBA Style)"], value="Friendly & Normal")
    
    theme = st.selectbox("🎨 Background Theme", ["Dark Space (Default)", "Ocean Blue", "Sunset Purple"], index=0)
    if theme == "Ocean Blue":
        st.markdown('<style>[data-testid="stAppViewContainer"]{background: radial-gradient(circle at 50% 50%, #0f2027, #203a43, #2c5364) !important;}</style>', unsafe_allow_html=True)
    elif theme == "Sunset Purple":
        st.markdown('<style>[data-testid="stAppViewContainer"]{background: radial-gradient(circle at 50% 50%, #23074d, #cc5333, #23074d) !important;}</style>', unsafe_allow_html=True)

    st.divider()
    st.subheader("💎 Pro Plan - Worldwide")
    if st.session_state.is_pro:
        st.success("✅ Pro Active - Unlimited Chats")
        if st.button("Cancel Pro (Test)"): st.session_state.is_pro=False; st.rerun()
    else:
        st.metric("Free Messages Left", f"{10 - st.session_state.count} / 10")
        st.progress(st.session_state.count/10)
        t1,t2,t3 = st.tabs(["bKash","PayPal","Card"])
        with t1:
            st.write("🇧🇩 **bKash - 350 TK / month**")
            st.link_button("💳 Pay with bKash", "https://shop.bkash.com", use_container_width=True)
            if st.button("✅ I Paid with bKash", use_container_width=True, key="b1"):
                st.session_state.is_pro=True; st.balloons(); st.success("Pro Activated!"); st.rerun()
        with t2:
            st.write("🌍 **PayPal - $2.99 / month**")
            st.link_button("🌍 Pay with PayPal", "https://paypal.me", use_container_width=True)
            if st.button("✅ I Paid with PayPal", use_container_width=True, key="b2"):
                st.session_state.is_pro=True; st.rerun()
        with t3:
            st.write("💳 **Card - $2.99 / month**")
            st.link_button("💳 Pay with Card", "https://buy.stripe.com/test", use_container_width=True)
            if st.button("✅ I Paid with Card", use_container_width=True, key="b3"):
                st.session_state.is_pro=True; st.rerun()

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages=[]; st.session_state.count=0; st.rerun()

# --- PROMPT BUILDER - ENGLISH BACKGROUND LOGIC ---
def build_prompt(who_is, language, talking_style):
    base = "You are Kids Learning AI, a safe, fun, real-life AI tutor for children worldwide. "
    if "Kid" in who_is: base += "Talk like a cute 5-year-old's best friend, super simple, with lots of emojis. Short sentences. "
    elif "Teen" in who_is: base += "Talk like a cool, smart elder brother for teens, friendly, motivational, with examples. "
    else: base += "Talk like a respectful, wise, loving father (ABBA). Guide parents how to teach kids. Respectful tone. "

    # LANGUAGE HANDLING
    if "Bangla" in language:
        base += "IMPORTANT: User wants Bangla, so reply in beautiful, natural, shuddho Bangla (Sundor Bangla), like a real Bangladeshi teacher from Dhaka. Full Bangla with emojis. "
    else:
        base += f"Reply in {language}. Keep it 100% in {language}. "

    if "Funny" in talking_style: base += "Be very funny, add jokes and emojis. "
    elif "Caring" in talking_style or "ABBA" in talking_style: base += "Be caring, loving, a bit strict like a father. Give life lessons. "
    else: base += "Be friendly, warm, normal. "

    base += "You teach Math, Science, English, Bangla, Stories, General Knowledge, Islamic values. NEVER give harmful content. Always safe for kids. Use real-life examples. End with a small question to keep conversation going."
    return base

# --- MAIN UI - ENGLISH ---
st.title("🧒🌍 Kids Learning AI")
st.caption("Safe, Fun & Real-Life Friend for Kids Worldwide | Bacchader jonno nirapod bondhu")
st.markdown("---")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if not st.session_state.is_pro and st.session_state.count >= 10:
    st.error("🔒 **Free limit reached (10 messages).** Please upgrade to Pro from the sidebar to continue unlimited chatting!")
    st.stop()

if prompt := st.chat_input("Ask something / Ekta prosno koro..."):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking... / Vabchi..."):
            try:
                sys_prompt = build_prompt(who, lang, style)
                # BEST MODEL - 2026 Latest
                models_to_try = [
                    "models/gemini-2.0-flash",
                    "models/gemini-2.0-flash-exp",
                    "models/gemini-1.5-flash-latest",
                    "models/gemini-1.5-flash",
                    "models/gemini-1.5-pro-latest",
                    "gemini-2.0-flash",
                    "gemini-1.5-flash"
                ]
                success = False
                last_err = ""
                for model_name in models_to_try:
                    try:
                        model = genai.GenerativeModel(model_name, system_instruction=sys_prompt)
                        # Get last 8 messages for context
                        context = "\n".join([f"{x['role']}: {x['content']}" for x in st.session_state.messages[-8:]])
                        response = model.generate_content(context)
                        if response.text:
                            st.markdown(response.text)
                            st.session_state.messages.append({"role":"assistant","content":response.text})
                            st.session_state.count += 1
                            success = True
                            break
                    except Exception as e:
                        last_err = str(e)
                        continue
                
                if not success:
                    st.error(f"Model Error: {last_err}\n\nPlease try again or check your API key. If using AQ. key, enable Generative Language API in Google Cloud Console.")
            except Exception as e:
                st.error(f"Error: {e}")
  
