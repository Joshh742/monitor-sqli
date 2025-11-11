import requests
import google.generativeai as genai
import os

GEMINI_API_KEY = "AIzaSyB_piNVX4sihYS8vPQ4OdJeVX00t746dMU"
FONNTE_TOKEN = "ThMoZ8cPqp8wEQcrMo1x"
NOMOR_WA_ADMIN = "6287775769005" 

LOG_FILE_SQLI = "/var/www/html/unkpresent/logs/sqli_attempts.log"

genai.configure(api_key=GEMINI_API_KEY)
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
            
            # PROMPT Gemini
            prompt_sqli = f"Berikan analisis super singkat (masing-masing 1 kalimat) untuk payload SQLi ini: '{entry.strip()}'. Jelaskan bahayanya DAN solusi pencegahannya. PENTING: Jangan gunakan markdown, bintang (*), atau emoji dalam respons Anda."
            
            analysis = get_gemini_analysis(prompt_sqli)
            
            message = f"""
ALERT SQL INJECTION

Log: {entry.strip()}

Analisis & Solusi Gemini:
{analysis}
"""
            
            send_whatsapp_notification(message)
            
    except Exception as e:
        print(f"Gagal memproses log SQLi: {e}")

if __name__ == "__main__":
    print("--- [Mulai Sesi Monitor SQLi] ---")
    check_sqli_logs()
    print("--- [Sesi Monitor SQLi Selesai] ---")