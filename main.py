import streamlit as st
import os
from google import genai
from google.genai import types

st.set_page_config(page_title="Kids Learning AI - 3.8", page_icon="🧒", layout="centered", initial_sidebar_state="expanded")

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

if st.session_state.theme == "Light":
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {background: #f9fafb;}
    [data-testid="stSidebar"] {background: #ffffff !important; border-right: 1px solid #eee;}
    [data-testid="stChatMessage"] {background: #ffffff !important; border: 1px solid #eee; border-radius: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);}
    h1 {color: #111827 !important;}
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

client = genai.Client(api_key=API_KEY)

if "messages" not in st.session_state: st.session_state.messages=[]

with st.sidebar:
    st.title("⚙️ Settings")
    theme_choice = st.radio("🎨 Theme", ["☀️ Light Mode", "🌙 Dark Mode"], index=0 if st.session_state.theme=="Light" else 1, horizontal=True)
    new_theme = "Light" if "Light" in theme_choice else "Dark"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()
    st.divider()
    lang = st.selectbox("🌍 Language", ["English","Sundor Bangla","Hindi","Urdu"], index=0)
    who = st.selectbox("👤 You are", ["Kid (5-10)", "Teen (11-16)", "Parent / ABBA"], index=0)
    if st.button("🗑️ Clear Chat"): st.session_state.messages=[]; st.rerun()

st.title("🧒 Kids Learning AI 3.8")
st.caption("Powered by Gemini 2.5 Flash - Latest Interactions API")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking with Gemini 3.8..."):
            sys_prompt = f"You are Kids Learning AI 3.8. Reply in {lang}. User is {who}. Be safe, fun, smart."
            full = sys_prompt + "\n\n" + "\n".join([f"{x['role']}: {x['content']}" for x in st.session_state.messages[-6:]])
            response = client.models.generate_content(
                model="gemini-2.5-flash", # <-- Eita holo 3.8 level er latest model!
                contents=full,
                config=types.GenerateContentConfig(temperature=0.8)
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role":"assistant","content":response.text})
