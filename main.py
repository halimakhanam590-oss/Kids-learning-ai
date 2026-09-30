import streamlit as st
import os
from google import genai
from google.genai import types

st.set_page_config(page_title="Kids Learning AI", page_icon="🧒", layout="centered", initial_sidebar_state="expanded")

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

if st.session_state.theme == "Light":
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {background: #fcfcfd;}
    [data-testid="stSidebar"] {background: #ffffff !important; border-right: 1px solid #eee;}
    [data-testid="stChatMessage"] {background: #ffffff !important; border: 1px solid #e5e7eb; border-radius: 18px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);}
    h1 {color: #111827 !important; font-weight: 800;}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {background: #0f172a;}
    [data-testid="stSidebar"] {background: #0f172a !important;}
    [data-testid="stChatMessage"] {background: #1e293b !important; border: 1px solid #334155; border-radius: 16px;}
    h1 {color: #fff !important;}
    </style>
    """, unsafe_allow_html=True)

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = os.getenv("GEMINI_API_KEY", "")

if not API_KEY:
    st.error("API Key missing! Add GEMINI_API_KEY in Secrets")
    st.stop()

client = genai.Client(api_key=API_KEY)

if "messages" not in st.session_state: st.session_state.messages=[]

with st.sidebar:
    st.title("⚙️ Settings")
    theme_choice = st.radio("🎨 Appearance", ["☀️ Light Mode", "🌙 Dark Mode"], index=0 if st.session_state.theme=="Light" else 1, horizontal=True)
    new_theme = "Light" if "Light" in theme_choice else "Dark"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()
    st.divider()
    lang = st.selectbox("🌍 Language", ["English","Sundor Bangla","Hindi","Urdu","Arabic"], index=0)
    who = st.selectbox("👤 You are", ["Kid (5-10)", "Teen (11-16)", "Parent / ABBA"], index=0)
    style = st.select_slider("🎭 Style", options=["Funny","Friendly","ABBA Style"], value="Friendly")
    if st.button("🗑️ Clear Chat"): st.session_state.messages=[]; st.rerun()

st.title("🧒 Kids Learning AI")
st.caption("Safe, Fun Friend - Makhon Smooth 3.8 🚀")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Ask something / Prosno koro..."):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking... Makhon er moto..."):
            sys_prompt = f"You are Kids Learning AI, safe fun tutor. Reply in {lang}. User is {who}, style {style}. Be safe, cute, educational."
            full = sys_prompt + "\n\n" + "\n".join([f"{x['role']}: {x['content']}" for x in st.session_state.messages[-8:]])
            
            models_to_try = ["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-2.0-flash-exp", "gemini-1.5-flash"]
            success = False
            last_err = ""
            for model_name in models_to_try:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=full,
                        config=types.GenerateContentConfig(temperature=0.8)
                    )
                    if response.text:
                        st.markdown(response.text)
                        st.session_state.messages.append({"role":"assistant","content":response.text})
                        success = True
                        break
                except Exception as e:
                    last_err = str(e)
                    continue
            
            if not success:
                st.error(f"Error: {last_err}")
