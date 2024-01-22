import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports

def scan_ports():
    ports = [port.device for port in serial.tools.list_ports.comports()]
    if ports:
        info = "\n".join([f"{port.device}: {port.description}" for port in serial.tools.list_ports.comports()])
        show_info_dialog("Connected COM Ports", info)
    else:
        show_info_dialog("Connected COM Ports", "No COM ports found.")

def show_info_dialog(title, message):
    info_dialog = tk.Toplevel(root)
    info_dialog.title(title)
    info_label = tk.Label(info_dialog, text=message)
    info_label.pack(padx=20, pady=10)
    ok_button = ttk.Button(info_dialog, text="OK", command=info_dialog.destroy)
    ok_button.pack(pady=10)

# GUI setup
root = tk.Tk()
root.title("SkunkFPV's COM Scanner")
root.geometry("300x200")  # Set window size to 400x400 pixels

title_label = tk.Label(root, text="SkunkFPV's COM Scanner", font=('Helvetica', 14, 'bold'))
title_label.pack(pady=20)

scan_button = ttk.Button(root, text="Scan COM Ports", command=scan_ports)
scan_button.pack(pady=20)

root.mainloop()
