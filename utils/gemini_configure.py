import os
import google.generativeai as gemini
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
gemini.configure(api_key=api_key)

model = gemini.GenerativeModel("gemini-2.0-flash")

def get_rekoemdasi_gemini(input, status="Normal"):
    """
    Menghasilkan saran kesehatan berdasarkan gejala pasien dan status prediksi.
    
    Parameters:
        input_dict (dict): Gejala pasien
        status (str): 'Normal' atau 'Tuberculosis'

    Returns:
        str: Saran dari Gemini
    """

    # Ubah input menjadi teks deskripsi gejala
    gejala = "\n".join([f"- {key.replace('_', ' ')}: {value}" for key, value in input.items()])

    # Buat prompt berbeda tergantung hasil diagnosis
    if status == "Tuberculosis":
        prompt = (f"""
                  Kamu adalah asisten medis digital. Seorang pasien didiagnosis memiliki kemungkinan Tuberkulosis berdasarkan gejala berikut:

            {gejala}

            Berdasarkan informasi tersebut, berikan rekomendasi pengobatan awal yang sesuai untuk penderita Tuberkulosis. Jelaskan secara ringkas namun jelas dalam bahasa Indonesia.
            Sertakan juga catatan bahwa pasien tetap perlu konsultasi lebih lanjut ke dokter.
        """)
    else:
        prompt = (f"""
                  Seorang pasien memiliki kemungkinan **Normal** berdasarkan hasil prediksi sistem klasifikasi TBC.
            Pasien mengisi gejala sebagai berikut:

            {gejala}

            Sebagai asisten medsis digital, berikan saran kesehatan untuk menjaga kesehatan pasien berdasarkan gejalanya, tambahkan juga informasi dan pentingnya menjaga kesehatan paru-paru dan mencegah penyakit TBC.
            Gunakan bahasa Indonesia yang sopan, ringkas, dan mudah dipahami masyarakat awam.
        """)

    # Kirim ke Gemini
    response = model.generate_content(prompt)
    return response.text

