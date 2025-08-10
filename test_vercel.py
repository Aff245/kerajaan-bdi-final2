import requests
import json

# ALAMAT MENARA PENGAWAS (PASTIKAN INI BENAR)
VERCEL_URL = "https://kerajaan-bdi-final2.vercel.app" # GANTI JIKA NAMA PROYEK BEDA

# ISI LAPORAN YANG AKAN DIKIRIM
payload = {
    "component": "termux_agent",
    "status": "active",
    "data": {"test_message": "HALO, APAKAH LAPORAN SAYA SAMPAI?"}
}

print(f"Mengirim laporan tes ke: {VERCEL_URL}/api/status")
print(f"Isi Laporan: {json.dumps(payload)}")

try:
    # Kirim laporan dengan timeout 20 detik
    response = requests.post(f"{VERCEL_URL}/api/status", json=payload, timeout=20)
    
    # Cetak hasil dari Vercel
    print("\n--- HASIL DARI VERCEL ---")
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    print("--------------------------\n")

    if response.status_code == 200:
        print("ðŸš€ðŸš€ðŸš€ LAPORAN BERHASIL TERKIRIM! JEMBATAN TERBUKA! ðŸš€ðŸš€ðŸš€")
    else:
        print("â Œâ Œâ Œ LAPORAN GAGAL! JEMBATAN MASIH TERTUTUP. â Œâ Œâ Œ")

except requests.exceptions.RequestException as e:
    print("\n!!! KESALAHAN KONEKSI FATAL !!!")
    print(f"Tidak bisa terhubung ke Vercel sama sekali. Error: {e}")
