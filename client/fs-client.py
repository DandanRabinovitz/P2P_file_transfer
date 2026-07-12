import socket
import struct
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

path = None
client_socket = None

def prepare_file_packet(file_path):
    path = Path(file_path)
    filename_bytes = path.name.encode('utf-8')
    filename_len = len(filename_bytes)
    file_bytes = path.read_bytes()
    file_size = len(file_bytes)
    header = struct.pack('!II', filename_len, file_size)
    packet = header + filename_bytes + file_bytes
    return packet

def switch_frames():
    start_frame.pack_forget()
    sender_frame.pack(fill="both", expand=True)

def browse_file():
    selected_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("All Files", "*.*")]
    )
    if selected_path:
        global path
        file_slot_var.set(selected_path)
        path = Path(selected_path)

def connect_server(server_host):
    global client_socket
    server_host = server_host.strip()
    if not server_host:
        messagebox.showwarning("Input Error", "Please enter an IP address.")
        return
    server_port = 12345
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5.0)
        client_socket.connect((server_host, server_port))
        client_socket.settimeout(None)
        print(f"Connected to {server_host}:{server_port}")
        switch_frames()
    except socket.error as e:
        print(f"Connection failed: {e}")
        messagebox.showerror(
            "Connection Error",
            f"Could not connect to '{server_host}'.\n\nDetails: {e}"
        )

def send_file():
    global client_socket, path
    if not path:
        messagebox.showwarning("Warning", "Please select a file first!")
        return
    try:
        packet = prepare_file_packet(path)
        client_socket.sendall(packet)
        print("File sent completely!")
        echo_message = client_socket.recv(1024).decode('utf-8')
        print(f"Server's response: {echo_message}")
    except socket.error as e:
        messagebox.showerror("Error", f"Failed to send file: {e}")

root = tk.Tk()
root.title("File Transfer Sender")
root.geometry("550x100")

start_frame = tk.Frame(root, padx=15, pady=20)
start_frame.pack(fill=tk.BOTH, expand=True)

sender_frame = tk.Frame(root, padx=15, pady=20)

ip_label = tk.Label(start_frame, text="Enter File Receiver Ip Address: ")
ip_label.pack(side=tk.LEFT, padx=5)

server_host = tk.StringVar()
ip_slot = tk.Entry(start_frame, textvariable=server_host, width=40)
ip_slot.pack(side=tk.LEFT, padx=5)

connect_btn = tk.Button(start_frame, text="Connect", command=lambda: connect_server(server_host.get()))
connect_btn.pack(side=tk.LEFT, padx=5)

label = tk.Label(sender_frame, text="Selected File:")
label.pack(side=tk.LEFT, padx=5)

file_slot_var = tk.StringVar()
entry_slot = tk.Entry(sender_frame, textvariable=file_slot_var, width=40)
entry_slot.pack(side=tk.LEFT, padx=5)

browse_btn = tk.Button(sender_frame, text="Browse", command=browse_file)
browse_btn.pack(side=tk.LEFT, padx=5)

send_btn = tk.Button(sender_frame, text="Send", command=send_file)
send_btn.pack(side=tk.LEFT, padx=5)

root.mainloop()