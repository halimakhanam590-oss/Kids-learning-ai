import os
import streamlit as st
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

# অ্যাপের টাইটেল ও ডিজাইন
st.title("🧸 মজার পাঠশালা - Kids Learning AI")
st.write("যেকোনো মজার প্রশ্ন করো, আর জেনে নাও নতুন কিছু!")

# ব্যবহারকারীর ইনপুট নেওয়ার জায়গা
user_input = st.text_input("তোমার প্রশ্নটি এখানে লেখো (যেমন: চাঁদ কেন আলো দেয়?):")

# বাটন তৈরি
if st.button("উত্তর জানো! ✨"):
    if not api_key:
        st.error("অ্যাপটি চালাতে GEMINI_API_KEY নামের একটি Secret যোগ করো।")
    elif user_input:
        with st.spinner("মজিক উত্তর খোঁজা হচ্ছে... 🧙‍♂️"):
            try:
                # AI কে নির্দেশ দেওয়া
                prompt = f"তুমি একজন খুব বন্ধুসুলভ এবং মজার শিক্ষক। একটি ৬-৮ বছরের বাচ্চার জন্য খুব সহজ, ছোট এবং গল্পের মতো করে বাংলায় এই প্রশ্নটির উত্তর দাও। প্রচুর ইমোজি ব্যবহার করবে। প্রশ্ন: {user_input}"
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                st.success(response.text)
            except Exception as e:
                st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")
              
