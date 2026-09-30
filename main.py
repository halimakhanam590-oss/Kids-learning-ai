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
    [data-testid="stChatMessage"] {background: #ffffff !important; border: 1px solid #e5e7eb; border-radius: 18px;}
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
    st.error("Add GEMINI_API_KEY in Secrets")
    st.stop()

client = genai.Client(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("Settings")
    theme_choice = st.radio("Theme", ["☀️ Light", "🌙 Dark"], index=0 if st.session_state.theme=="Light" else 1, horizontal=True)
    new_theme = "Light" if "Light" in theme_choice else "Dark"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()
    st.divider()
    lang = st.selectbox("Language", ["English","Sundor Bangla"], index=0)
    if st.button("Clear Chat"):
        st.session_state.messages=[]
        st.rerun()

st.title("Kids Learning AI")
st.caption("Makhon Smooth - Fixed 3.8 🚀")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            full = f"Reply in {lang}. Be safe fun for kids.\n\n" + "\n".join([f"{x['role']}: {x['content']}" for x in st.session_state.messages[-6:]])
            for model_name in ["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-1.5-flash"]:
                try:
                    resp = client.models.generate_content(
                        model=model_name,
                        contents=full,
                        config=types.GenerateContentConfig(temperature=0.7)
                    )
                    if resp.text:
                        st.markdown(resp.text)
                        st.session_state.messages.append({"role":"assistant","content":resp.text})
                        break
                except Exception as e:
                    last_err = str(e)
                    continue
            else:
                st.error(f"Error: {last_err}")
