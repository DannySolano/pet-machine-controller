
from utils.gcode_controller import GcodeController
from tkinter import filedialog
import subprocess
import tkinter as tk


gcontroller = GcodeController()

is_connection_on = gcontroller.is_connected

available_ports = gcontroller.available_ports()

def increment(currentNumber):
    value = int(currentNumber["text"])
    currentNumber.config(text=f"{value + 1}")
    gcontroller.set_extruder_velocity(value + 1)  # Update extruder velocity

def decrement(currentNumber):
    value = int(currentNumber["text"])
    currentNumber.config(text=f"{value - 1}")
    gcontroller.set_extruder_velocity(value - 1)  # Update extruder velocity

def start(status):
    status.config(text="Starting...")
    gcontroller.start_extruder()  # Start the extruder

def stop(status):
    status.config(text="Stopped")
    gcontroller.pause_extruder()  # Pause the extruder

def upload_file(status):
    file = filedialog.askopenfilename(filetypes=[("Gcode Files", "*.gcode")])
    if file:
        status.config(text=f"File uploaded: {file.split('/')[-1]}")
        gcontroller.read_gcode(open(file, 'r'))  # Read and send G-code file

def connect_to_port(port_selector, status):
    selected_port = port_selector.get()
    if selected_port:
        gcontroller.set_selected_port(selected_port)
        gcontroller.start_connection() 
        status.config(text=f"Connected to {selected_port}")
    else:
        status.config(text="No port selected!")


def execute_command(text_area, entry):
    command = entry.get()
    entry.delete(0, tk.END)

    if command.strip():
        text_area.insert(tk.END, f"> {command}\n")
        print(command)
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            text_area.insert(tk.END, output)
        except subprocess.CalledProcessError as e:
            text_area.insert(tk.END, e.output)
        text_area.insert(tk.END, "\n")