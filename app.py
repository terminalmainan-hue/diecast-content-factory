import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests
import time

def upload_to_imgbb(uploaded_file):
    """
    Fungsi untuk mengunggah file gambar dari Streamlit ke ImgBB secara gratis
    dan mengembalikan URL gambar publik langsung (.jpg/.png).
    """
    # 1. Ambil API Key dari Streamlit Secrets
    api_key = st.secrets["IMGBB_API_KEY"]
    url = "https://api.imgbb.com/1/upload"
    
    # 2. ImgBB meminta file dalam format teks Base64
    # Kita ubah data biner file upload menjadi string base64
    image_bytes = uploaded_file.getvalue()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    # 3. Siapkan payload data
    payload = {
        "key": api_key,
        "image": base64_image
    }
    
    try:
        # Kirim request POST ke ImgBB
        response = requests.post(url, data=payload)
        response_data = response.json()
        
        # 4. Jika sukses, ambil URL gambar langsung (direct link)
        if response.status_code == 200 and response_data["success"]:
            return response_data["data"]["url"]
        else:
            st.error(f"ImgBB Upload Gagal: {response_data['error']['message']}")
            return None
            
    except Exception as e:
        st.error(f"Terjadi kesalahan koneksi ke ImgBB: {e}")
        return None
st.title("🚗 Diecast Content Factory AI + Auto Video")

# 1. Ambil API Keys dari Streamlit Secrets
GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
LUMA_KEY = st.secrets["LUMA_API_KEY"]  # Daftarkan key Luma Anda di secrets

# Konfigurasi Gemini
genai.configure(api_key=GEMINI_KEY)
model_gemini = genai.GenerativeModel("gemini-3-flash-preview")

st.write("Unggah foto diecast, dapatkan Teks SEO YouTube + Video Sinematik Otomatis!")

uploaded_file = st.file_uploader("Pilih foto diecast (JPG/PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Foto diecast berhasil diunggah", use_container_width=True)

    if st.button("Generate Teks & Video Sinematik"):
        
        # --- LANGKAH A: GENERATE TEKS DENGAN GEMINI ---
        with st.spinner("1. Gemini sedang menganalisis foto & membuat teks SEO..."):
            prompt_text = """
            Anda adalah kolektor diecast profesional dan pakar SEO YouTube.
            Analisis foto ini, sebutkan **Brand** dan **Model** nya di paling atas.
            Lalu buatkan: 2 Pilihan Judul YouTube, Deskripsi Review SEO, dan 10 Hashtag relevan.
            """
            response_text = model_gemini.generate_content([prompt_text, image])
            st.success("Teks SEO Berhasil Dibuat!")
            st.write(response_text.text)
        
        st.divider()

        # --- LANGKAH B: GENERATE VIDEO DENGAN LUMA AI API ---
        with st.spinner("2. Mengirim foto ke Luma AI untuk generate video sinematik..."):
            
            # Persiapan Data untuk Luma API (Image-to-Video)
            luma_url = "https://api.lumalabs.ai/dream-machine/v1/generations"
            headers = {
                "Authorization": f"Bearer {LUMA_KEY}",
                "Content-Type": "application/json"
            }
            
            # Kita meminta Luma membuat pergerakan kamera sinematik mengitari diecast
            payload = {
                "prompt": "Cinematic studio lighting, slow camera pan around the car, realistic reflections, 4k resolution, 3d motion",
                "keyframes": {
                    "frame0": {
                        "type": "image",
                        "url": "ISI_DENGAN_URL_GAMBAR_ANDA" 
                        # Catatan: Luma API membutuhkan URL gambar publik. 
                        # Jika dicoba lokal/Streamlit Cloud, file upload harus di-hosting sementara (misal via Imgur API/Cloudinary)
                        # ATAU jika menggunakan Runway API, bisa langsung upload file biner (binary bytes).
                    }
                }
            }
            
            # Jalankan request ke Video Generator (Contoh REST API umum)
            # response_video = requests.post(luma_url, json=payload, headers=headers)
            
            # Simulasi Proses Antrean Video AI (Biasanya memakan waktu 1-2 menit)
            # Di bawah ini adalah logika berulang (loop) untuk mengecek apakah video sudah selesai dirender di server AI
            
            st.info("Video sedang diproses di server AI (estimasi 1 menit). Harap tunggu...")
            time.sleep(10) # Simulasi loading pasca-request
            
            # Contoh tampilan jika video sudah beres didownload dari API:
            # video_url = response_video.json()["assets"]["video"]
            
            # Untuk keperluan testing interface saat ini, kita beri placeholder sukses:
            st.success("Video Sinematik Selesai Dibuat!")
            
            # Menampilkan video di dashboard Streamlit Anda
            # st.video(video_url)
            st.info("Hubungkan baris kode API di atas dengan akun Luma/Runway Anda untuk mengunduh MP4 aslinya.")
