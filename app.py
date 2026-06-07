import streamlit as st
from openai import OpenAI

st.title("🚗 Diecast Content Factory AI")

api_key = st.secrets["OPENAI_API_KEY"]

client = OpenAI(api_key=api_key)

brand = st.text_input("Brand")

model = st.text_input("Model")

if st.button("Generate AI Content"):

    prompt = f"""
    Anda adalah kolektor diecast profesional.

    Buat:

    1. Judul YouTube
    2. Deskripsi YouTube
    3. 10 hashtag

    Untuk:

    Brand: {brand}
    Model: {model}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    st.write(response.choices[0].message.content)
