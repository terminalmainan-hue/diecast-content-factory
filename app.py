import streamlit as st

st.set_page_config(
    page_title="Diecast Content Factory",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Diecast Content Factory")

st.write("Generate artikel, script YouTube, dan SEO diecast secara otomatis.")

brand = st.text_input("Brand Diecast")

model = st.text_input("Model Diecast")

uploaded_file = st.file_uploader(
    "Upload Foto Diecast",
    type=["jpg", "jpeg", "png"]
)

if st.button("Generate Content"):

    st.success("Data berhasil diterima")

    st.write("### Informasi Diecast")
    st.write(f"Brand: {brand}")
    st.write(f"Model: {model}")

    if uploaded_file:
        st.image(uploaded_file, width=400)

    st.write("### Judul YouTube")
    st.write(f"Review {brand} {model} yang Wajib Dimiliki Kolektor!")

    st.write("### Deskripsi")
    st.write(
        f"Pada video ini kita membahas {brand} {model}, "
        "mulai dari detail casting, sejarah rilisan, hingga nilai koleksinya."
    )
