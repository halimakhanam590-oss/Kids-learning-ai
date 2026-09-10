import os
import streamlit as st
import google.generativeai as genai

# API Configuration
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

# Page Configuration
st.set_page_config(page_title="Nexora AI", page_icon="🤖")

# UI Layout (All in English)
st.title("🤖 Nexora AI")
st.write("Your smart, versatile personal assistant.")

# Input field
user_input = st.text_input("Enter your prompt or question:")

if st.button("Send 🚀"):
    if not api_key:
        st.error("GEMINI_API_KEY is not configured in Vercel.")
    elif user_input:
        with st.spinner("Thinking..."):
            try:
                system_instruction = (
                    "You are Nexora AI, a helpful, intelligent, and natural AI assistant. "
                    "Automatically detect the user's language: "
                    "If the user asks or speaks in Bengali, reply naturally and fluently in Bengali. "
                    "If the user speaks in English, reply in English. "
                    "Keep your responses direct, clear, and engaging without robotic filler."
                )
                
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=system_instruction
                )
                
                response = model.generate_content(user_input)
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
                
