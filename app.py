import streamlit as st
import google.generativeai as genai
from PIL import Image

st.title("🚗 Diecast Content Factory AI + Vision")

# 1. Ambil Gemini API Key dari Streamlit Secrets
api_key = st.secrets["GEMINI_API_KEY"]

# 2. Konfigurasi SDK Gemini
genai.configure(api_key=api_key)

# 3. Inisialisasi model multimodal
model_gemini = genai.GenerativeModel("gemini-3-flash-preview")

st.write("Unggah foto diecast Anda, dan AI akan menganalisisnya secara otomatis untuk membuat konten YouTube!")

# 4. Widget untuk Upload Foto
uploaded_file = st.file_uploader("Pilih foto diecast (JPG/PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Buka gambar menggunakan Pillow
    image = Image.open(uploaded_file)
    
    # Tampilkan preview gambar di aplikasi Streamlit
    st.image(image, caption="Foto diecast yang diunggah", use_container_width=True)

    if st.button("Analisis Foto & Generate Content"):
        with st.spinner("Gemini sedang menganalisis foto diecast Anda..."):
            
            # 5. Buat prompt instruksi yang spesifik untuk menganalisis gambar
            prompt = """
            Anda adalah seorang kolektor diecast profesional dan pakar SEO YouTube.
            
            Tugas Anda:
            1. Analisis foto ini dan tebak apa Brand (misal: Hot Wheels, Mini GT, Matchbox, Pop Race, dll) dan Model mobilnya secara akurat.
            2. Tuliskan hasil tebakan Anda di bagian paling atas dengan format:
               - **Brand Terdeteksi:** [Nama Brand]
               - **Model Terdeteksi:** [Nama Model/Jenis Mobil]
            
            3. Setelah itu, buatkan kelengkapan konten YouTube berikut:
               - **Judul YouTube:** (Buat 2 pilihan judul yang menarik dan cinematic/clickbait berkelas)
               - **Deskripsi YouTube:** (Buat deskripsi review yang menarik, mendetail sesuai visual mobil di foto, dan ramah SEO)
               - **10 Hashtag:** (Hashtag yang relevan untuk target global dan lokal)
            
            Berikan jawaban dalam Bahasa Indonesia yang profesional namun santai khas konten kreator mainan.
            """
            
            # 6. Kirim gambar dan prompt sekaligus ke Gemini
            response = model_gemini.generate_content([prompt, image])
            
            st.success("Selesai!")
            st.write(response.text)
