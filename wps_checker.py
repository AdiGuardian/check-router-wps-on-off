
import os
import json
import socket
import subprocess
from datetime import datetime

C = "\033[96m"
G = "\033[92m"
Y = "\033[93m"
R = "\033[91m"
W = "\033[0m"

def run(cmd, timeout=3):
    try:
        p = subprocess.run(
            cmd, capture_output=True,
            text=True, timeout=timeout
        )
        return p.stdout.strip()
    except Exception:
        return ""

def wifi_info():
    raw = run(["termux-wifi-connectioninfo"])
    try:
        return json.loads(raw) if raw else {}
    except json.JSONDecodeError:
        return {}

def gateway_info(ip):
    if not ip or "." not in ip:
        return None

    parts = ip.split(".")
    if len(parts) != 4:
        return None

    # Metode umum jaringan rumahan.
    candidates = [
        ".".join(parts[:3] + ["1"]),
        ".".join(parts[:3] + ["254"])
    ]

    for gw in candidates:
        try:
            with socket.create_connection(
                (gw, 80), timeout=0.5
            ):
                return gw
        except OSError:
            continue

    return None

def admin_check(gateway):
    if not gateway:
        return "UNKNOWN"

    for port in (80, 443):
        try:
            with socket.create_connection(
                (gateway, port), timeout=0.7
            ):
                return "WEB ADMIN TERDETEKSI"
        except OSError:
            pass

    return "TIDAK TERDETEKSI"

def main():
    os.system("clear")

    print(C + "=" * 42)
    print("     WPS CHECKER UNIVERSAL PRO")
    print("              FAST v2.1")
    print("=" * 42 + W)

    print("\n[1] Membaca informasi WiFi...")
    wifi = wifi_info()

    ssid = wifi.get("ssid", "UNKNOWN")
    bssid = wifi.get("bssid", "UNKNOWN")
    ip = wifi.get("ip", "UNKNOWN")
    frequency = wifi.get("frequency_mhz", "UNKNOWN")
    signal = wifi.get("rssi", "UNKNOWN")
    state = wifi.get("supplicant_state", "UNKNOWN")

    print("[2] Membaca informasi jaringan...")
    gateway = gateway_info(ip)

    print("[3] Memeriksa akses router...")
    admin = admin_check(gateway)

    print("\n" + C + "=== HASIL PEMERIKSAAN ===" + W)
    print("SSID       :", ssid)
    print("BSSID      :", bssid)
    print("IP HP      :", ip)
    print("GATEWAY    :", gateway or "UNKNOWN")
    print("FREQUENCY  :", frequency)
    print("SIGNAL     :", signal)
    print("CONNECTION :", state)
    print("ROUTER     :", admin)

    print("\n" + Y + "=== WPS SECURITY ===" + W)
    print("WPS STATUS : UNKNOWN")
    print("Status WPS belum dapat dibaca.")
    print("Periksa melalui halaman admin router.")

    print("\n=== REKOMENDASI ===")
    print("1. Gunakan WPA2-AES atau WPA3.")
    print("2. Nonaktifkan WPS.")
    print("3. Gunakan password kuat.")
    print("4. Ganti password admin router.")

    data = {
        "DATE": str(datetime.now()),
        "SSID": ssid,
        "BSSID": bssid,
        "IP": ip,
        "GATEWAY": gateway,
        "FREQUENCY": frequency,
        "SIGNAL": signal,
        "CONNECTION": state,
        "ROUTER": admin,
        "WPS": "UNKNOWN"
    }

    with open("wps_report.txt", "w") as f:
        for k, v in data.items():
            f.write(f"{k}: {v}\n")

    print("\nLaporan disimpan: wps_report.txt")
    print(G + "\nPEMERIKSAAN SELESAI!" + W)

if __name__ == "__main__":
    main()
