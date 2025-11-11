import requests
import google.generativeai as genai
import os

# --- GANTI INI DENGAN DATA ANDA ---
GEMINI_API_KEY = "AIzaSyB_piNVX4sihYS8vPQ4OdJeVX00t746dMU"
FONNTE_TOKEN = "TOKEN_FONNTE_ANDA"
NOMOR_WA_ADMIN = "6281234567890" # Nomor WA Anda
# -----------------------------------

# Path log yang sudah benar
LOG_FILE_SQLI = "/var/www/html/unkpresent/logs/sqli_attempts.log"

# Inisialisasi API
genai.configure(api_key=GEMINI_API_KEY)

# ### INI PERUBAHAN PENTINGNYA ###
# Kita gunakan nama model yang PASTI ADA dari hasil pencarian Anda
gemini_model = genai.GenerativeModel('models/gemini-flash-latest')
# #################################


def get_gemini_analysis(prompt):
    """Mendapatkan analisis cerdas dari Gemini."""
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Kita tambahkan detail error agar lebih jelas
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
            
            prompt_sqli = f"WAF mendeteksi percobaan SQL Injection: '{entry.strip()}'. Analisis bahaya payload ini & beri rekomendasi."
            
            analysis = get_gemini_analysis(prompt_sqli)
            
            message = f"🚨 *ALERT SQL INJECTION* 🚨\n\nLog: {entry.strip()}\n\nAnalisis Gemini:\n{analysis}"
            
            send_whatsapp_notification(message)
            
    except Exception as e:
        print(f"Gagal memproses log SQLi: {e}")

# --- MULAI SKRIP ---
if __name__ == "__main__":
    print("--- [Mulai Sesi Monitor SQLi] ---")
    check_sqli_logs()
    print("--- [Sesi Monitor SQLi Selesai] ---")