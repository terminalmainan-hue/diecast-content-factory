import streamlit as st
import google.generativeai as genai

st.title("🚗 Diecast Content Factory AI")

# 1. Ambil Gemini API Key dari Streamlit Secrets
api_key = st.secrets["GEMINI_API_KEY"]

# 2. Konfigurasi SDK Gemini
genai.configure(api_key=api_key)

# 3. Inisialisasi model (menggunakan gemini-1.5-flash yang cepat dan efisien)
model_gemini = genai.GenerativeModel("gemini-1.5-flash")

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

    # 4. Panggil API Gemini untuk membuat konten
    response = model_gemini.generate_content(prompt)

    # 5. Tampilkan hasil text secara langsung
    st.write(response.text)
