import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.predict import predict_tbc

st.set_page_config(page_title="Deteksi TBC", layout="centered")

st.title("🩺 Deteksi Penyakit TBC")
st.markdown("Masukkan gejala berikut untuk mengetahui kemungkinan TBC dan mendapatkan saran medis.")

# Form input
with st.form("tbc_form"):
    st.subheader("Isi Gejala Pasien")
    col1, col2 = st.columns([1, 1], gap='large')
    with col1:
        age = st.number_input("Usia (Tahun)", min_value=0, max_value=120, step=1)
        gender = st.selectbox("Jenis Kelamin", ["Male", "Female"])
        chest_pain = st.selectbox("Nyeri Dada", ["Yes", "No"])
        cough = st.slider("Tingkat Batuk (0-9)", 0, 9, 0)
        breath = st.slider("Tingkat Sesak Napas (0-4)", 0, 4, 0)
        fatigue = st.slider("Tingkat Kelelahan (0-9)", 0, 9, 0)
    with col2:
        weight_loss = st.number_input("Penurunan Berat Badan (kg)", 0.0)
        fever = st.selectbox("Demam", ["Mild", "Moderate", "High"])
        night_sweats = st.selectbox("Berkeringat Malam", ["Yes", "No"])
        sputum_prod = st.selectbox("Produksi Dahak", ["Low", "Medium", "High"])
        blood_sputum = st.selectbox("Darah dalam Dahak", ["Yes", "No"])
        smoking = st.selectbox("Riwayat Merokok", ["Never", "Current", "Former"])
        prev_tb = st.selectbox("Riwayat TBC Sebelumnya", ["Yes", "No"])

    submit = st.form_submit_button("Lakukan Prediksi")

if submit:
    input_data = {
        "Age": age,
        "Gender": gender,
        "Chest_Pain": chest_pain,
        "Cough_Severity": cough,
        "Breathlessness": breath,
        "Fatigue": fatigue,
        "Weight_Loss": weight_loss,
        "Fever": fever,
        "Night_Sweats": night_sweats,
        "Sputum_Production": sputum_prod,
        "Blood_in_Sputum": blood_sputum,
        "Smoking_History": smoking,
        "Previous_TB_History": prev_tb
    }

    from utils.gemini_configure import get_rekoemdasi_gemini

    result = predict_tbc(input_data)

    if result == "Tuberculosis":
        st.error("Hasil: Terindikasi Tuberculosis")
        # with st.spinner("Mendapatkan rekomendasi dari Gemini..."):
        #     rekomendasi = get_rekoemdasi_gemini(input_data, status = "Tuberculosis")
    else:
        st.success("Hasil: Tidak Terindikasi Tuberculosis")
        # with st.spinner("Mendapatkan rekomendasi dari Gemini..."):
        # rekomendasi = get_rekoemdasi_gemini(input_data, status = "Normal")

    # with st.expander("Lihat rekomendasi dari Gemini"):
    #     st.markdown(rekomendasi)
