import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from functions import start, stop, connect_to_port, decrement, increment, execute_command, upload_file, available_ports, is_connection_on

root = tk.Tk()

state = "active" if is_connection_on else "disabled"

label_status = tk.Label(root,
                        text="Status",
                        bg="lightgray",
                        width=40,
                        height=3)
label_number = tk.Label(root, text="50", font=("Arial", 48))
label_unity = tk.Label(root, text="mm/s", font=("Arial", 48))

label_number.pack()
label_unity.pack()
label_status.pack(pady=10)

# Control buttons (start/stop and increment/decrement)
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_start = tk.Button(frame_buttons,
                      text="▶",
                      width=5,
                      command=lambda: start(status=label_status),
                      state=state,
                      bg="white",
                      activebackground="lightyellow"
                      )
btn_start.grid(row=0, column=0, padx=5)

btn_stop = tk.Button(frame_buttons,
                     text="■",
                     width=5,
                     command=lambda: stop(status=label_status),
                     state=state,
                     bg="white",
                     activebackground="lightyellow")
btn_stop.grid(row=0, column=1, padx=5)

btn_decrement = tk.Button(frame_buttons,
                          text="- 1",
                          width=5,
                          command=lambda: decrement(
                              currentNumber=label_number),
                          state=state,
                          bg="white",
                          activebackground="lightyellow")
btn_decrement.grid(row=1, column=0, padx=5, pady=5)

btn_increment = tk.Button(frame_buttons,
                          text="+ 1",
                          width=5,
                          command=lambda: increment(
                              currentNumber=label_number),
                          state=state,
                          bg="white",
                          activebackground="lightyellow"
                          )
btn_increment.grid(row=1, column=1, padx=5, pady=5)

# Port selector and connect button
frame_ports = tk.Frame(root)
frame_ports.pack(pady=10)

port_selector_label = tk.Label(frame_ports, text="Select Port:")
port_selector_label.grid(row=0, column=0, padx=5)

# Ports
port_selector = ttk.Combobox(
    frame_ports, values=available_ports, state="readonly", width=10)
port_selector.grid(row=0, column=1, padx=5)

btn_connect = tk.Button(frame_ports, text="Connect", command=lambda: connect_to_port(
    port_selector=port_selector, status=label_status), bg="white", activebackground="lightyellow")
btn_connect.grid(row=0, column=2, padx=5)


# Upload file button
btn_upload = tk.Button(root, text="Upload File", command=lambda: upload_file(
    status=label_status), width=20, bg="white", state=state, activebackground="lightyellow")
btn_upload.pack(pady=10)

# Command execution area
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=80)
text_area.pack(padx=10, pady=10)
entry = tk.Entry(root, width=80)
entry.pack(padx=10, pady=5)
entry.bind("<Return>", execute_command)


# Run the application
root.title("PET RECICLE CONTROLLER")
root.geometry("400x650")

root.mainloop()
