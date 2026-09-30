import streamlit as st
import os

try:
    from google import genai
    from google.genai import types
    NEW_SDK = True
except:
    import google.generativeai as genai
    NEW_SDK = False

st.set_page_config(page_title="Kids Learning AI", page_icon="🧒", layout="centered", initial_sidebar_state="expanded")

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

if st.session_state.theme == "Light":
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #f8f9ff 0%, #eef2ff 50%, #ffffff 100%);
    }
    [data-testid="stHeader"]{background: rgba(255,255,255,0);}
    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e5e7eb;
        box-shadow: 2px 0 10px rgba(0,0,0,0.05);
    }
    [data-testid="stChatMessage"] {
        background: #ffffff !important;
        border: 1px solid #e5e7eb;
        border-radius: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li {color: #1f2937 !important;}
    h1 {color: #111827 !important; font-weight: 800;}
    .stCaption {color: #6b7280 !important;}
    [data-testid="stChatInput"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(ellipse at top, #1e1b4b 0%, #111827 100%);
    }
    [data-testid="stHeader"]{background: rgba(0,0,0,0);}
    [data-testid="stSidebar"] {
        background: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stChatMessage"] {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid #334155;
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }
    h1 {
        background: linear-gradient(90deg, #a5b4fc, #f0abfc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    [data-testid="stChatInput"] {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 24px;
    }
    </style>
    """, unsafe_allow_html=True)

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = os.getenv("GEMINI_API_KEY", "")

if not API_KEY:
    st.error("GEMINI_API_KEY missing in Secrets!")
    st.stop()

if NEW_SDK:
    client = genai.Client(api_key=API_KEY)
else:
    genai.configure(api_key=API_KEY)

if "messages" not in st.session_state: st.session_state.messages=[]
if "count" not in st.session_state: st.session_state.count=0
if "is_pro" not in st.session_state: st.session_state.is_pro=False

with st.sidebar:
    st.title("⚙️ Settings")
    st.subheader("🎨 Appearance")
    theme_choice = st.radio("Theme", ["☀️ Light Mode", "🌙 Dark Mode"], 
                            index=0 if st.session_state.theme=="Light" else 1,
                            horizontal=True)
    new_theme = "Light" if "Light" in theme_choice else "Dark"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()
    st.divider()
    lang = st.selectbox("🌍 Language", ["English","Sundor Bangla (সুন্দর বাংলা)","Hindi","Urdu","Arabic","Spanish"], index=0)
    who = st.selectbox("👤 You are", ["Kid (5-10)", "Teen (11-16)", "Parent / ABBA"], index=0)
    style = st.select_slider("🎭 Style", options=["Funny & Playful","Friendly & Normal","Caring ABBA Style"], value="Friendly & Normal")
    st.divider()
    st.subheader("💎 Pro Plan")
    if st.session_state.is_pro:
        st.success("✅ Pro Active")
        if st.button("Cancel Pro"): st.session_state.is_pro=False; st.rerun()
    else:
        st.metric("Free Left", f"{10-st.session_state.count} / 10")
        st.progress(st.session_state.count/10)
        c1,c2 = st.columns(2)
        with c1:
            if st.button("🔓 Unlock Pro", use_container_width=True): 
                st.session_state.is_pro=True; st.balloons(); st.rerun()
        with c2:
            if st.button("🗑️ Clear", use_container_width=True): 
                st.session_state.messages=[]; st.session_state.count=0; st.rerun()

def build_prompt(who_is, language, talking_style):
    p="You are Kids Learning AI, safe fun tutor. "
    if "Kid" in who_is: p+="Talk cute simple emojis. "
    elif "Teen" in who_is: p+="Talk cool elder brother. "
    else: p+="Talk wise respectful ABBA father. "
    if "Bangla" in language: p+="Reply in beautiful natural Bangla. "
    else: p+=f"Reply in {language}. "
    if "Funny" in talking_style: p+="Be funny. "
    elif "ABBA" in talking_style: p+="Be caring strict father. "
    p+="Teach Math, Science, Stories. 100% safe."
    return p

st.title("🧒 Kids Learning AI")
st.caption("Safe, Fun & Real-Life Friend for Kids Worldwide")
st.markdown("---")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if not st.session_state.is_pro and st.session_state.count>=10:
    st.warning("Free limit over - Unlock Pro from sidebar")
    st.stop()

if prompt := st.chat_input("Ask something / Ekta prosno koro..."):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                sys_prompt = build_prompt(who, lang, style)
                context = "\n".join([f"{x['role']}: {x['content']}" for x in st.session_state.messages[-10:]])
                full_prompt = f"{sys_prompt}\n\nConversation:\n{context}"
                if NEW_SDK:
                    last_err=""
                    for model_name in ["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-1.5-flash"]:
                        try:
                            response = client.models.generate_content(
                                model=model_name,
                                contents=full_prompt,
                                config=types.GenerateContentConfig(temperature=0.7)
                            )
                            txt = response.text
                            if txt:
                                st.markdown(txt)
                                st.session_state.messages.append({"role":"assistant","content":txt})
                                st.session_state.count+=1
                                break
                        except Exception as e:
                            last_err=str(e)
                            continue
                    else:
                        st.error(f"Model Error: {last_err}")
                else:
                    model = genai.GenerativeModel("gemini-1.5-flash-latest", system_instruction=sys_prompt)
                    response = model.generate_content(context)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role":"assistant","content":response.text})
                    st.session_state.count+=1
            except Exception as e:
                st.error(f"Error: {e}")
