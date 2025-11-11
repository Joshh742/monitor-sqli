import google.generativeai as genai
import os

# --- GANTI INI DENGAN DATA ANDA ---
GEMINI_API_KEY = "API_KEY_GEMINI_ANDA_YANG_VALID"
# -----------------------------------

print("--- [Memulai Pencarian Model Gemini] ---")

try:
    # Konfigurasi API key
    genai.configure(api_key=GEMINI_API_KEY)

    print("Mencari model yang mendukung 'generateContent':")

    found_model = False
    # Meminta daftar model ke Google
    for m in genai.list_models():
        # Kita hanya peduli dengan model yang bisa membuat konten
        if 'generateContent' in m.supported_generation_methods:
            print(f"--> Model Ditemukan: {m.name}")
            found_model = True

    if not found_model:
        print("PERHATIAN: Tidak ada model yang mendukung 'generateContent' ditemukan.")

except Exception as e:
    print(f"!!! Gagal total saat mencari model: {e}")

print("--- [Selesai Pencarian Model] ---")