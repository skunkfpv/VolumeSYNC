import tkinter as tk
from tkinter import ttk
import serial
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Function to set the Windows volume
def set_volume(value):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(value, None)

# Function to connect to the selected COM port
def connect_serial():
    com_port = com_port_var.get()
    baud_rate = 115200  # You can adjust this if needed

    try:
        # Open the serial port
        serial_port = serial.Serial(com_port, baud_rate)
        print(f"Connected to {com_port} at {baud_rate} baud")
        # Start listening for data
        root.after(1, lambda: read_serial_data(serial_port))  # Reduce the delay to 1 millisecond
    except Exception as e:
        print(f"Failed to connect to {com_port}: {e}")

# Function to read serial data and adjust volume
def read_serial_data(serial_port):
    try:
        if serial_port.in_waiting > 0:
            data = serial_port.readline().decode("utf-8").strip()
            try:
                percentage = int(data)
                # Map the percentage to a volume value between 0.0 and 1.0
                volume_value = percentage / 100.0
                set_volume(volume_value)
                print(f"Setting volume to {percentage}%")
            except ValueError:
                # Ignore non-integer values
                pass
    except Exception as e:
        print(f"Error reading serial data: {e}")

    # Continue listening for data
    root.after(1, lambda: read_serial_data(serial_port))  # Reduce the delay to 1 millisecond

# GUI setup
root = tk.Tk()
root.title("Volume Control")

# COM port selection
com_port_var = tk.StringVar()
com_port_label = ttk.Label(root, text="Select COM Port:")
com_port_label.grid(row=0, column=0, padx=10, pady=5)

com_ports = [f"COM{i+1}" for i in range(10)]  # Add more if needed
com_port_combobox = ttk.Combobox(root, values=com_ports, textvariable=com_port_var)
com_port_combobox.grid(row=0, column=1, padx=10, pady=5)
com_port_combobox.set(com_ports[0])

# Connect button
connect_button = ttk.Button(root, text="Connect", command=connect_serial)
connect_button.grid(row=1, column=0, columnspan=2, pady=10)

# Main loop
root.mainloop()
