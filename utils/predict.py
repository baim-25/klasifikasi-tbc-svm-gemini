import joblib
import pandas as pd
import os

# Tentukan path ke direktori root proyek
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Muat model klasifikasi yang telah dilatih
model = joblib.load(os.path.join(BASE_PATH, "models/svm_model.pkl"))

# Muat LabelEncoder untuk mengubah label numerik (0/1) ke label asli (Normal/Tuberculosis)
label_encoder = joblib.load(os.path.join(BASE_PATH, "models/label_encoder_target.pkl"))

# Daftar kolom kategorikal untuk diencoding
categorical_columns = [
    "Gender", "Chest_Pain", "Fever", "Night_Sweats",
    "Sputum_Production", "Blood_in_Sputum",
    "Smoking_History", "Previous_TB_History"
]

# Muat semua encoder per kolom kategorikal
encoders = {}
for col in categorical_columns:
    encoders[col] = joblib.load(os.path.join(BASE_PATH, f"models/encoder_{col}.pkl"))

def predict_tbc(input_dict):

    import streamlit as st
    """
    Menerima input berupa dictionary gejala pasien,
    lalu mengembalikan hasil prediksi: 'Normal' atau 'Tuberculosis'.
    """

    # Konversi input menjadi DataFrame satu baris
    df = pd.DataFrame([input_dict])

    # Encoding kolom kategorikal
    for col in categorical_columns:
        le = encoders[col]
        val = df[col].iloc[0]

        # Tangani jika nilai input tidak dikenali oleh encoder
        if val not in le.classes_:
            st.warning(f"⚠️ Nilai '{val}' tidak dikenal di kolom {col}. Diganti dengan '{le.classes_[0]}'")
            val = le.classes_[0]  # fallback ke nilai default pertama
        df[col] = le.transform([val])
    
    # Tampilkan hasil encoding
    st.write("📦 Setelah encoding:")
    st.write(df)

    # Prediksi menggunakan model
    pred_num = model.predict(df)[0]

    # Ubah hasil prediksi numerik ke label asli
    result = label_encoder.inverse_transform([pred_num])[0]

    st.write(f"🔍 Prediksi numerik: {pred_num}, label: {result}")

    return result
