import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests
import base64
import time

st.title("🚗 Diecast Content Factory AI + Auto Video")

# 1. Pastikan semua API Key sudah ada di Streamlit Secrets
GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
IMGBB_KEY = st.secrets["IMGBB_API_KEY"]
LUMA_KEY = st.secrets["LUMA_API_KEY"]

# Konfigurasi Gemini
genai.configure(api_key=GEMINI_KEY)
model_gemini = genai.GenerativeModel("gemini-3-flash-preview")

# Fungsi pembantu untuk upload ke ImgBB
def upload_to_imgbb(uploaded_file):
    url = "https://api.imgbb.com/1/upload"
    image_bytes = uploaded_file.getvalue()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    payload = {"key": IMGBB_KEY, "image": base64_image}
    try:
        response = requests.post(url, data=payload)
        res_json = response.json()
        if response.status_code == 200 and res_json["success"]:
            return res_json["data"]["url"]
    except:
        return None
    return None

uploaded_file = st.file_uploader("Pilih foto diecast (JPG/PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Foto diecast berhasil diunggah", use_container_width=True)

    if st.button("Generate Teks & Video Sinematik"):
        
        # --- LANGKAH A: GENERATE TEKS DENGAN GEMINI ---
        with st.spinner("1. Menganalisis foto & membuat teks SEO..."):
            prompt_text = """
            Anda adalah kolektor diecast profesional dan pakar SEO YouTube.
            Analisis foto ini, sebutkan Brand dan Model nya di paling atas.
            Lalu buatkan: 2 Pilihan Judul YouTube, Deskripsi Review SEO, dan 10 Hashtag relevan.
            """
            response_text = model_gemini.generate_content([prompt_text, image])
            st.success("Teks SEO Berhasil Dibuat!")
            st.write(response_text.text)
        
        st.divider()

        # --- LANGKAH B: UBAH FOTO JADI URL PUBLIK (IMGBB) ---
        with st.spinner("2. Membuat tautan gambar publik via ImgBB..."):
            public_image_url = upload_to_imgbb(uploaded_file)
            
        if not public_image_url:
            st.error("Gagal mengonversi gambar ke URL publik. Cek kembali IMGBB_API_KEY Anda.")
        else:
            # --- LANGKAH C: KIRIM PERMINTAAN VIDEO KE LUMA AI ---
            with st.spinner("3. Memulai proses pembuatan video di Luma AI..."):
                luma_endpoint = "https://api.lumalabs.ai/dream-machine/v1/generations"
                headers = {
                    "Authorization": f"Bearer {LUMA_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "prompt": "Cinematic camera slowly panning around the 1/64 diecast car, photorealistic, 4k resolution, studio lighting, smooth motion",
                    "keyframes": {
                        "frame0": {
                            "type": "image",
                            "url": public_image_url
                        }
                    }
                }
                
                # Kirim request pembuatan video
                luma_response = requests.post(luma_endpoint, json=payload, headers=headers)
                
                if luma_response.status_code != 201:
                    st.error(f"Gagal terhubung ke Luma API: {luma_response.text}")
                else:
                    generation_data = luma_response.json()
                    generation_id = generation_data["id"]
                    
                    # --- LANGKAH D: LOOPING MENUNGGU VIDEO SELESAI ---
                    status = "dreaming"
                    video_url = None
                    
                    # Buat kontainer teks status kosong di Streamlit agar bisa diupdate dinamis
                    status_message = st.empty()
                    
                    while status in ["dreaming", "queued"]:
                        status_message.info("Video sedang diproses/antre di server Luma AI... Cek berkala setiap 10 detik.")
                        time.sleep(10)
                        
                        # Cek status video menggunakan ID generasi
                        check_url = f"https://api.lumalabs.ai/dream-machine/v1/generations/{generation_id}"
                        check_response = requests.get(check_url, headers=headers)
                        
                        if check_response.status_code == 200:
                            check_data = check_response.json()
                            status = check_data["state"]
                            
                            if status == "completed":
                                video_url = check_data["assets"]["video"]
                                break
                            elif status == "failed":
                                st.error("Luma AI gagal memproses video dari gambar ini.")
                                break
                    
                    # Tampilkan video jika statusnya sudah 'completed'
                    if video_url:
                        status_message.empty() # Hapus teks loading info
                        st.success("🔥 Video Sinematik Berhasil Dibuat!")
                        st.video(video_url)
