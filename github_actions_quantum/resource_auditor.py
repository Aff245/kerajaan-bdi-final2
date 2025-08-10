#!/usr/bin/env python3
import os
import sys
import requests
from datetime import datetime

def log(message):
    """Mencatat aktivitas agen penghemat."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] [ResourceOptimizerAgent] {message}")

def get_github_actions_usage():
    """Mengambil data penggunaan menit dari GitHub API."""
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")

    if not token or not repo:
        log("ERROR: GITHUB_TOKEN atau GITHUB_REPOSITORY tidak ditemukan. Audit dibatalkan.")
        return None

    log(f"Menghubungi GitHub API untuk audit penggunaan di {repo}...")
    try:
        # API untuk mendapatkan penggunaan menit Actions
        url = f"https://api.github.com/repos/{repo}/actions/usage"
        headers = {"Authorization": f"token {token}"}
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            log("Audit penggunaan berhasil diambil.")
            return response.json()
        else:
            log(f"ERROR: Gagal mengambil data penggunaan (Status: {response.status_code}) - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        log(f"ERROR: Koneksi ke GitHub API gagal: {e}")
        return None

def analyze_usage_data(data):
    """Menganalisis data penggunaan dan memberikan rekomendasi."""
    if not data:
        return []

    log("Menganalisis data penggunaan menit...")
    # Free tier GitHub memberikan 2000 menit/bulan untuk repo publik/pribadi
    free_tier_limit_minutes = 2000
    total_used_ms = data.get('total_ms', 0)
    total_used_minutes = total_used_ms / 60000 # Konversi milidetik ke menit

    percentage_used = (total_used_minutes / free_tier_limit_minutes) * 100
    
    log(f"Total menit terpakai bulan ini: {total_used_minutes:.2f} dari {free_tier_limit_minutes} menit.")
    log(f"Persentase penggunaan: {percentage_used:.2f}%")
    
    recommendations = []
    if percentage_used > 90:
        recommendations.append({
            "level": "KRITIS",
            "message": f"Penggunaan sudah {percentage_used:.2f}%! Segera optimalkan workflow atau pertimbangkan upgrade.",
            "action": "Nonaktifkan pemicu 'schedule' untuk sementara."
        })
    elif percentage_used > 50:
        recommendations.append({
            "level": "PERINGATAN",
            "message": f"Penggunaan sudah melebihi 50%. Waspada terhadap pemborosan.",
            "action": "Periksa durasi setiap job. Gabungkan langkah 'pip install' jika memungkinkan."
        })
    else:
        recommendations.append({
            "level": "AMAN",
            "message": f"Penggunaan {percentage_used:.2f}%. Efisiensi terjaga.",
            "action": "Tidak ada tindakan yang diperlukan."
        })
    return recommendations

def generate_report(recommendations):
    """Menghasilkan laporan audit."""
    log("Menghasilkan laporan audit sumber daya...")
    if not recommendations:
        log("Tidak ada data untuk dilaporkan.")
        return

    print("\n" + "="*50)
    print("ðŸ’¸ LAPORAN AUDIT SUMBER DAYA OTONOMUS ðŸ’¸")
    print("="*50)
    for rec in recommendations:
        icon = {"KRITIS": "ðŸ”¥", "PERINGATAN": "âš ï¸ ", "AMAN": "âœ…"}
        print(f"{icon.get(rec['level'], 'ðŸ“ ')} Level: {rec['level']}")
        print(f"   - Pesan: {rec['message']}")
        print(f"   - Rekomendasi Aksi: {rec['action']}")
        print("-" * 20)
    print("="*50)

if __name__ == "__main__":
    log("Misi dimulai: Audit dan optimisasi sumber daya kerajaan...")
    usage_data = get_github_actions_usage()
    efficiency_recommendations = analyze_usage_data(usage_data)
    generate_report(efficiency_recommendations)
    log("Misi selesai.")
