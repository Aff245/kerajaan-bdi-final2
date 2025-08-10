#!/usr/bin/env python3
import os
import sys
import requests
import json
from datetime import datetime

def log(message):
    """Mencatat aktivitas agen penghemat."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] [ResourceOptimizer] {message}")

def get_github_actions_usage():
    """Mengambil data penggunaan menit GitHub Actions."""
    log("Memeriksa penggunaan menit GitHub Actions...")
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")
    if not token or not repo:
        log("WARNING: GITHUB_TOKEN atau GITHUB_REPOSITORY tidak diatur. Melewatkan audit GitHub.")
        return None

    try:
        # API untuk mendapatkan penggunaan Actions untuk sebuah repository
        url = f"https://api.github.com/repos/{repo}/actions/usage"
        headers = {"Authorization": f"token {token}"}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        usage_data = response.json()
        
        # Free tier GitHub adalah 2000 menit/bulan untuk repo publik/pribadi
        minutes_used = usage_data.get('billable', {}).get('UBUNTU', {}).get('total_ms', 0) / 60000
        log(f"-> Penggunaan bulan ini: {minutes_used:.2f} dari 2000 menit (Free Tier).")
        return {"minutes_used": minutes_used, "limit": 2000}
    except requests.exceptions.RequestException as e:
        log(f"ERROR: Gagal mengambil data penggunaan GitHub Actions: {e}")
        return None

def analyze_efficiency(data):
    """Menganalisis efisiensi dan memberikan rekomendasi."""
    log("Menganalisis efisiensi sumber daya...")
    recommendations = []

    # Analisis GitHub Actions
    github_usage = data.get("github_actions")
    if github_usage:
        percentage_used = (github_usage['minutes_used'] / github_usage['limit']) * 100
        
        if percentage_used > 90:
            recommendations.append({
                "type": "ANCAMAN KRITIS",
                "source": "GitHub Actions",
                "message": f"Penggunaan menit telah mencapai {percentage_used:.1f}%! Segera optimalkan workflow!",
                "recommendation": "Nonaktifkan trigger 'on: push' dan gunakan 'workflow_dispatch' (manual) saja."
            })
        elif percentage_used > 50:
             recommendations.append({
                "type": "PERINGATAN",
                "source": "GitHub Actions",
                "message": f"Penggunaan menit di atas 50% ({percentage_used:.1f}%). Waspada terhadap pemborosan.",
                "recommendation": "Periksa durasi setiap job. Gabungkan langkah 'pip install' jika memungkinkan."
            })
        else:
             recommendations.append({
                "type": "INFO",
                "source": "GitHub Actions",
                "message": f"Penggunaan menit AMAN ({percentage_used:.1f}%). Efisiensi terjaga.",
                "recommendation": "Tidak ada tindakan yang diperlukan."
            })

    return recommendations

def generate_report(recommendations):
    """Menghasilkan laporan optimisasi."""
    log("Menghasilkan laporan optimisasi sumber daya...")
    if not recommendations:
        log("Tidak ada rekomendasi. Semua sumber daya digunakan secara efisien.")
        return

    print("\n" + "="*50)
    print("ðŸ’¸ LAPORAN OPTIMISASI SUMBER DAYA ðŸ’¸")
    print("="*50)
    for rec in recommendations:
        icon = {"ANCAMAN KRITIS": "ðŸ”¥", "PERINGATAN": "âš ï¸ ", "INFO": "âœ…"}
        print(f"{icon.get(rec['type'], 'ðŸ“ ')} Tipe: {rec['type']} ({rec['source']})")
        print(f"   - Pesan: {rec['message']}")
        print(f"   - Rekomendasi Aksi: {rec['recommendation']}")
        print("-" * 20)
    print("="*50)

if __name__ == "__main__":
    log("Misi dimulai: Audit dan optimisasi sumber daya kerajaan...")
    all_data = {
        "github_actions": get_github_actions_usage()
        # Di masa depan, kita bisa tambah audit Vercel, dll.
    }
    efficiency_recommendations = analyze_efficiency(all_data)
    generate_report(efficiency_recommendations)
    log("Misi selesai.")
