#!/usr/bin/env python3
import os
import sys
import random
from datetime import datetime

def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [ResourceOptimizerAgent] {message}")

def simulate_github_actions_usage():
    log("Memulai audit penggunaan (SIMULASI)...")
    # Simulasi penggunaan menit antara 100 dan 1500
    simulated_used_minutes = random.uniform(100.0, 1500.0)
    return {"total_minutes_used": simulated_used_minutes}

def analyze_usage_data(data):
    if not data: return []
    free_tier_limit = 2000
    total_used = data.get("total_minutes_used", 0)
    percentage_used = (total_used / free_tier_limit) * 100
    
    log(f"Total menit terpakai (simulasi): {total_used:.2f} dari {free_tier_limit} menit ({percentage_used:.2f}%).")
    
    recommendations = []
    if percentage_used > 90:
        recommendations.append({"level": "KRITIS", "message": "Penggunaan mendekati batas!"})
    elif percentage_used > 50:
        recommendations.append({"level": "PERINGATAN", "message": "Penggunaan melebihi 50%."})
    else:
        recommendations.append({"level": "AMAN", "message": "Efisiensi terjaga."})
    return recommendations

def generate_report(recommendations):
    if not recommendations: return
    print("\n" + "="*50)
    print("ðŸ’¸ LAPORAN AUDIT SUMBER DAYA (SIMULASI) ðŸ’¸")
    print("="*50)
    for rec in recommendations:
        print(f"Level: {rec['level']} - Pesan: {rec['message']}")
    print("="*50)

if __name__ == "__main__":
    log("Misi dimulai...")
    usage_data = simulate_github_actions_usage()
    efficiency_recommendations = analyze_usage_data(usage_data)
    generate_report(efficiency_recommendations)
    log("Misi selesai.")
