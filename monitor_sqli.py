import requests
import google.generativeai as genai
import os

# --- GANTI INI DENGAN DATA ANDA ---
GEMINI_API_KEY = "AIzaSyB_piNVX4sihYS8vPQ4OdJeVX00t746dMU"
FONNTE_TOKEN = "ThMoZ8cPqp8wEQcrMo1x"
NOMOR_WA_ADMIN = "6287775769005" # Nomor WA Anda
# -----------------------------------

# File log yang akan kita pantau
LOG_FILE_SQLI = "/var/www/html/unkpresent/logs/sqli_attempts.log"

# Inisialisasi API
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.0-pro')

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
    
    # Cek apakah file log ada dan berisi sesuatu
    if not os.path.exists(LOG_FILE_SQLI) or os.path.getsize(LOG_FILE_SQLI) == 0:
        print("Tidak ada serangan baru.")
        return # Tidak ada serangan, keluar

    try:
        # Buka dan baca semua serangan yang tercatat
        with open(LOG_FILE_SQLI, 'r') as f:
            log_entries = f.readlines()
        
        # PENTING: Kosongkan file log agar tidak diproses berulang kali
        open(LOG_FILE_SQLI, 'w').close() 

        # Proses setiap serangan yang tadi dibaca
        for entry in log_entries:
            print(f"DETEKSI SQLi: {entry.strip()}")
            
            # Buat prompt untuk Gemini
            prompt_sqli = f"WAF mendeteksi percobaan SQL Injection: '{entry.strip()}'. Analisis bahaya payload ini & beri rekomendasi."
            
            # Minta analisis dari Gemini
            analysis = get_gemini_analysis(prompt_sqli)
            
            # Buat pesan notifikasi
            message = f"🚨 *ALERT SQL INJECTION* 🚨\n\nLog: {entry.strip()}\n\nAnalisis Gemini:\n{analysis}"
            
            # Kirim ke WhatsApp
            send_whatsapp_notification(message)
            
    except Exception as e:
        print(f"Gagal memproses log SQLi: {e}")

# --- MULAI SKRIP ---
if __name__ == "__main__":
    print("--- [Mulai Sesi Monitor SQLi] ---")
    check_sqli_logs()
    print("--- [Sesi Monitor SQLi Selesai] ---")