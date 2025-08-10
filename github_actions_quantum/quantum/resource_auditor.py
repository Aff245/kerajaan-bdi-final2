#!/usr/bin/env python3
import os
import sys
import requests
import json
from datetime import datetime

def log(message):
    """Mencatat aktivitas agen penghemat."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] [ResourceOptimizerAgent] {message}")

def get_github_actions_usage(repo, token):
    """Mengambil data penggunaan menit GitHub Actions."""
    log("Memeriksa penggunaan menit GitHub Actions...")
    if not token or not repo:
        log("WARNING: GITHUB_TOKEN atau GITHUB_REPOSITORY tidak diatur. Audit dilewatkan.")
        return None
    
    try:
        # API untuk mendapatkan penggunaan menit untuk repo
        url = f"https://api.github.com/repos/{repo}/actions/usage"
        headers = {"Authorization": f"token {token}"}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        log(f"ERROR: Gagal mengambil data penggunaan GitHub Actions: {e}")
        return None

def analyze_efficiency(usage_data):
    """Menganalisis efisiensi dan memberikan rekomendasi."""
    log("Menganalisis efisiensi sumber daya...")
    recommendations = []
    
    if not usage_data:
        return [{"source": "System", "type": "ERROR", "message": "Tidak bisa mendapatkan data penggunaan."}]

    # Total menit gratis per bulan untuk akun publik adalah 2000
    free_minutes_limit = 2000
    minutes_used = usage_data.get('total_minutes_used', {}).get('total', 0)
    
    percentage_used = (minutes_used / free_minutes_limit) * 100
    
    log(f"Total menit terpakai bulan ini: {minutes_used} menit ({percentage_used:.2f}% dari batas gratis).")

    if percentage_used > 90:
        recommendations.append({
            "source": "GitHub Actions", "type": "PERINGATAN KRITIS",
            "message": f"Penggunaan menit sudah mencapai {percentage_used:.2f}%! Segera optimalkan workflow."
        })
    elif percentage_used > 50:
         recommendations.append({
            "source": "GitHub Actions", "type": "PERINGATAN",
            "message": f"Penggunaan menit di atas 50%. Waspada terhadap pemborosan."
        })
    else:
         recommendations.append({
            "source": "GitHub Actions", "type": "INFO",
            "message": f"Penggunaan menit AMAN ({percentage_used:.2f}%). Efisiensi terjaga."
        })
    return recommendations

def generate_report(recommendations):
    """Menghasilkan laporan optimisasi."""
    log("Menghasilkan laporan optimisasi sumber daya...")
    print("\n" + "="*50)
    print("ðŸ’¸ LAPORAN OPTIMISASI SUMBER DAYA ðŸ’¸")
    print("="*50)
    for rec in recommendations:
        icon = {"ERROR": "â Œ", "PERINGATAN KRITIS": "ðŸš¨", "PERINGATAN": "âš ï¸ ", "INFO": "â„¹ï¸ "}.get(rec['type'], "ðŸ“")
        print(f"{icon} Tipe: {rec['type']} | Sumber: {rec['source']}")
        print(f"   -> Pesan: {rec['message']}")
    print("="*50)

if __name__ == "__main__":
    log("Misi dimulai: Audit dan optimisasi sumber daya kerajaan...")
    github_repo = os.getenv("GITHUB_REPOSITORY")
    github_token = os.getenv("GITHUB_TOKEN")
    
    usage_info = get_github_actions_usage(github_repo, github_token)
    efficiency_recommendations = analyze_efficiency(usage_info)
    generate_report(efficiency_recommendations)
    log("Misi selesai.")
