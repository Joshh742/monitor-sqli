import requests
import google.generativeai as genai
import os

# --- GANTI INI DENGAN DATA ANDA ---
GEMINI_API_KEY = "AIzaSyB_piNVX4sihYS8vPQ4OdJeVX00t746dMU"
FONNTE_TOKEN = "ThMoZ8cPqp8wEQcrMo1x"
NOMOR_WA_ADMIN = "6287775769005" # (Pastikan ini juga benar)
# -----------------------------------

# Path log yang sudah benar
LOG_FILE_SQLI = "/var/www/html/unkpresent/logs/sqli_attempts.log"

# Inisialisasi API
genai.configure(api_key=GEMINI_API_KEY)
# Kita gunakan model yang sudah Anda temukan
gemini_model = genai.GenerativeModel('models/gemini-flash-latest')


def get_gemini_analysis(prompt):
    """Mendapatkan analisis cerdas dari Gemini."""
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Analisis Gemini gagal: {e}"

def send_whatsapp_notification(message):
    """Mengirim notifikasi via Fonnte."""
    print(f"Mengirim notifikasi: {message[:50]}...")
    try:
        requests.post(
            "https://api.fonnte.com/send",
            headers={"Authorization": FONNTE_TOKEN},
            data={"target": NOMOR_WA_ADMIN, "message": message}
        )
    except Exception as e:
        print(f"Gagal kirim Fonnte: {e}")

# --- ALUR UTAMA ---
def check_sqli_logs():
    print("Mengecek log SQLi (sqli_attempts.log)...")
    
    if not os.path.exists(LOG_FILE_SQLI) or os.path.getsize(LOG_FILE_SQLI) == 0:
        print("Tidak ada serangan baru.")
        return 

    try:
        with open(LOG_FILE_SQLI, 'r') as f:
            log_entries = f.readlines()
        
        open(LOG_FILE_SQLI, 'w').close() 

        for entry in log_entries:
            print(f"DETEKSI SQLi: {entry.strip()}")
            
            # ### PERUBAHAN 1: PROMPT GEMINI DIBUAT SINGKAT ###
            # Kita minta Gemini untuk penjelasan 1 kalimat.
            prompt_sqli = f"Jelaskan bahaya payload SQLi ini dalam 1 kalimat singkat: '{entry.strip()}'"
            
            analysis = get_gemini_analysis(prompt_sqli)
            
            # ### PERUBAHAN 2: PESAN WHATSAPP DIBUAT SINGKAT ###
            message = f"""
🚨 *ALERT SQL INJECTION* 🚨

*Log:* {entry.strip()}

*Analisis Gemini:*
{analysis}
"""
            
            send_whatsapp_notification(message)
            
    except Exception as e:
        print(f"Gagal memproses log SQLi: {e}")

# --- MULAI SKRIP ---
if __name__ == "__main__":
    print("--- [Mulai Sesi Monitor SQLi] ---")
    check_sqli_logs()
    print("--- [Sesi Monitor SQLi Selesai] ---")