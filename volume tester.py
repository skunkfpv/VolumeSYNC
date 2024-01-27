import serial
import tkinter as tk
from tkinter import ttk

class VolumeMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Volume Monitor")

        # Variables
        self.com_port_var = tk.StringVar()
        self.volume_var = tk.StringVar()

        # GUI elements
        self.label_com_port = tk.Label(root, text="Select COM Port:")
        self.com_port_combobox = ttk.Combobox(root, textvariable=self.com_port_var, state="readonly")
        self.label_volume = tk.Label(root, text="Current Volume:")
        self.volume_label = tk.Label(root, textvariable=self.volume_var)

        # Set up GUI
        self.setup_gui()

    def setup_gui(self):
        # Layout
        self.label_com_port.grid(row=0, column=0, pady=5)
        self.com_port_combobox.grid(row=0, column=1, pady=5)
        self.label_volume.grid(row=1, column=0, pady=5)
        self.volume_label.grid(row=1, column=1, pady=5)

        # Populate COM port combobox with available ports
        self.populate_com_ports()

        # Button to start monitoring
        start_button = tk.Button(self.root, text="Start Monitoring", command=self.start_monitoring)
        start_button.grid(row=2, column=0, columnspan=2, pady=10)

    def populate_com_ports(self):
        com_ports = [f"COM{i+1}" for i in range(256)]
        self.com_port_combobox["values"] = com_ports

    def start_monitoring(self):
        com_port = self.com_port_var.get()
        if com_port:
            try:
                with serial.Serial(com_port, 115200, timeout=1) as ser:
                    while True:
                        line = ser.readline().decode('utf-8').strip()
                        if line.isdigit():
                            volume = int(line)
                            self.volume_var.set(f"{volume}%")
                            self.root.update()
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Please select a COM port.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VolumeMonitor(root)
    root.mainloop()
