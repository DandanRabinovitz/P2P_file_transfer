import socket
import struct
from threading import Thread
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

def receive_file(client_socket):
    header = b""
    while len(header) < 8:
        chunk = client_socket.recv(8 - len(header))
        if not chunk:
            raise ConnectionError("Socket closed prematurely while reading header")
        header += chunk
    filename_len, file_size = struct.unpack('!II', header)
    filename_bytes = b""
    while len(filename_bytes) < filename_len:
        chunk = client_socket.recv(filename_len - len(filename_bytes))
        if not chunk:
            raise ConnectionError("Socket closed prematurely while reading filename")
        filename_bytes += chunk
    filename = filename_bytes.decode('utf-8')
    file_data = b""
    while len(file_data) < file_size:
        remaining_bytes = file_size - len(file_data)
        chunk = client_socket.recv(min(4096, remaining_bytes))
        if not chunk:
            raise ConnectionError("Socket closed prematurely while reading file data")
        file_data += chunk
    print("File fully received!")
    return filename, file_data

def switch_frames():
    start_frame.pack_forget()
    sender_frame.pack(fill="both", expand=True)

def run_server_socket():
    server_port = 12345
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("0.0.0.0", server_port))
        server_socket.listen(1)
        print(f"Server listening on port {server_port}...")
        switch_frames()
        client_socket, client_address = server_socket.accept()
        print(f"Connection accepted from {client_address}")
        try:
            filename, raw_file_bytes = receive_file(client_socket)
            output_path = Path(filename)
            output_path.write_bytes(raw_file_bytes)
            print(f"Success! File successfully written to: {output_path.resolve()}")
            label.config(text=f"Received: {filename} ({len(raw_file_bytes)} bytes)")
            client_socket.sendall(b"File received successfully by server!")
        except Exception as e:
            print(f"Error handling file transfer: {e}")
        finally:
            client_socket.close()
    except socket.error as e:
        print(f"Server failed to start: {e}")
        messagebox.showerror("Server Error", f"Could not start server.\n\nDetails: {e}")

def start_server():
    server_thread = Thread(target=run_server_socket, daemon=True)
    server_thread.start()

root = tk.Tk()
root.title("File Transfer Receiver (Server)")
root.geometry("550x100")

start_frame = tk.Frame(root, padx=15, pady=20)
start_frame.pack(fill=tk.BOTH, expand=True)

sender_frame = tk.Frame(root, padx=15, pady=20)

status_label = tk.Label(start_frame, text="Click to launch the receiver server:")
status_label.pack(side=tk.LEFT, padx=5)

connect_btn = tk.Button(start_frame, text="Start Server", command=start_server)
connect_btn.pack(side=tk.LEFT, padx=5)

label = tk.Label(sender_frame, text="Waiting for incoming files...")
label.pack(side=tk.LEFT, padx=5)

root.mainloop()