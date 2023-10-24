import subprocess
import tkinter as tk
from tkinter import scrolledtext

def get_active_wifi_ssid():
    try:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode('utf-8').split('\n')
        ssid_line = [line.split(':')[1].strip() for line in results if "SSID" in line]
        return ssid_line[0] if ssid_line else None
    except subprocess.CalledProcessError:
        return None

def get_wifi_password(ssid):
    try:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', f'name={ssid}', 'key=clear']).decode('utf-8').split('\n')
        password_line = [line.split(':')[1].strip() for line in results if "Key Content" in line]
        return password_line[0] if password_line else "Cannot retrieve password."
    except subprocess.CalledProcessError:
        return "Cannot retrieve password."

def show_active_wifi_password():
    active_ssid = get_active_wifi_ssid()

    result_text.delete('1.0', tk.END)  # Clear previous text

    if active_ssid:
        password = get_wifi_password(active_ssid)
        result_text.insert(tk.END, f"Active WiFi Network: {active_ssid}, Password: {password}\n")
    else:
        result_text.insert(tk.END, "No active WiFi network found.")

def show_saved_wifi_passwords():
    saved_profiles = get_saved_wifi_profiles()

    result_text.delete('1.0', tk.END)  # Clear previous text

    if saved_profiles:
        for profile in saved_profiles:
            password = get_wifi_password(profile)
            result_text.insert(tk.END, f"Saved WiFi Network: {profile}, Password: {password}\n")
    else:
        result_text.insert(tk.END, "No saved WiFi networks found.")

def get_saved_wifi_profiles():
    try:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
        profiles = [line.split(':')[1].strip() for line in results if "All User Profile" in line]
        return profiles
    except subprocess.CalledProcessError:
        return []

# Create the main window
root = tk.Tk()
root.title("WiFi Password Retrieval")

# Create and pack widgets
title_label = tk.Label(root, text="WiFi Password Scanner ", font=("Helvetica", 16))

title_label.pack(pady=10)

active_wifi_button = tk.Button(root, text="Scan Active WiFi", command=show_active_wifi_password)
active_wifi_button.pack()

saved_wifi_button = tk.Button(root, text="Scan Saved WiFi", command=show_saved_wifi_passwords)
saved_wifi_button.pack()

result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
result_text.pack(padx=10, pady=10)

root.mainloop()
