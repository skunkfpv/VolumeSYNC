import serial
import tkinter as tk
from tkinter import ttk

class SerialMonitor:
    def __init__(self):
        self.ser = None

    def open_serial(self, port, baud_rate):
        try:
            self.ser = serial.Serial(port, baud_rate)
            self.ser.timeout = 0  # Non-blocking mode
            print(f"Serial port {port} opened at {baud_rate} bps")
        except Exception as e:
            print(f"Error: {e}")

    def close_serial(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Serial port closed")

    def read_serial(self):
        try:
            data = self.ser.readline().decode('utf-8', errors='ignore').strip()
            if data:
                print(data)
            self.root.after(10, self.read_serial)  # Schedule the next read
        except Exception as e:
            print(f"Error reading serial data: {e}")
            self.root.after(10, self.read_serial)  # Continue reading after an error

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Serial Monitor")

        # Create and pack widgets
        ttk.Label(self.root, text="Select COM Port:").pack(pady=10)

        ports = [f"COM{i+1}" for i in range(256)]
        self.port_combobox = ttk.Combobox(self.root, values=ports)
        self.port_combobox.pack(pady=10)
        self.port_combobox.set(ports[0])

        ttk.Label(self.root, text="Select Baud Rate:").pack(pady=10)

        baud_rates = [9600, 115200, 230400, 460800]  # Add more if needed
        self.baud_rate_combobox = ttk.Combobox(self.root, values=baud_rates)
        self.baud_rate_combobox.pack(pady=10)
        self.baud_rate_combobox.set(baud_rates[0])

        open_button = ttk.Button(self.root, text="Open Serial", command=self.open_serial_callback)
        open_button.pack(pady=10)

        close_button = ttk.Button(self.root, text="Close Serial", command=self.close_serial)
        close_button.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.root.mainloop()

    def open_serial_callback(self):
        selected_port = self.port_combobox.get()
        selected_baud_rate = int(self.baud_rate_combobox.get())

        self.open_serial(selected_port, selected_baud_rate)

        if self.ser and self.ser.is_open:
            # Start reading serial data
            self.root.after(10, self.read_serial)

    def on_close(self):
        self.close_serial()
        self.root.destroy()

# Create an instance of the SerialMonitor class
serial_monitor = SerialMonitor()

# Create the GUI
serial_monitor.create_gui()
