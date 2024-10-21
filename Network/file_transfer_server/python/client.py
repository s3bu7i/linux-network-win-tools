import socket
import os
from tkinter import Tk, Button, Label, filedialog, messagebox, simpledialog
from tkinter import filedialog, messagebox, simpledialog

BUFFER_SIZE = 4096
HOST = '127.0.0.1'
PORT = 5001

client_socket = None  # Initialize client socket

def upload_file():
    try:
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        # Send upload request
        client_socket.send(f"upload {filename}".encode())
        client_socket.send(f"{file_size}".encode())

        with open(file_path, 'rb') as f:
            sent_bytes = 0
            while sent_bytes < file_size:
                bytes_read = f.read(BUFFER_SIZE)
                client_socket.sendall(bytes_read)
                sent_bytes += len(bytes_read)
                progress_label.config(text=f"Sent {sent_bytes}/{file_size} bytes.")
        
        messagebox.showinfo("Success", f"File '{filename}' uploaded successfully.")
    
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

def download_file():
    # Send request to get the list of files
    client_socket.send("list".encode())
    file_list = client_socket.recv(BUFFER_SIZE).decode().split(',')
    
    # Show available files in a dialog
    filename = simpledialog.askstring("Select File", "Available files:\n" + "\n".join(file_list) + "\n\nEnter the filename to download:")
    if not filename or filename not in file_list:
        messagebox.showerror("Error", "Invalid filename selected.")
        return

    try:
        client_socket.send(f"download {filename}".encode())
        file_size = client_socket.recv(BUFFER_SIZE).decode()

        if file_size.startswith("ERROR"):
            messagebox.showerror("Error", file_size)
            return
        
        file_size = int(file_size)
        download_path = filedialog.asksaveasfilename(defaultextension=os.path.splitext(filename)[1])
        if not download_path:
            return

        with open(download_path, 'wb') as f:
            received_bytes = 0
            while received_bytes < file_size:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                f.write(bytes_read)
                received_bytes += len(bytes_read)
                progress_label.config(text=f"Received {received_bytes}/{file_size} bytes.")
        
        messagebox.showinfo("Success", f"File '{filename}' downloaded successfully.")
    
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

def connect_server():
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        messagebox.showinfo("Connection", "Connected to the server!")
    except Exception as e:
        messagebox.showerror("Connection Error", f"Could not connect to the server: {e}")

# Initialize the GUI window
root = Tk()
root.title("File Transfer Client")

# Labels and Buttons
connect_btn = Button(root, text="Connect to Server", command=connect_server, width=25, height=2)
upload_btn = Button(root, text="Upload File", command=upload_file, width=25, height=2)
download_btn = Button(root, text="Download File", command=download_file, width=25, height=2)
progress_label = Label(root, text="Progress: ", width=50, height=2)

# Layout
connect_btn.pack(pady=10)
upload_btn.pack(pady=10)
download_btn.pack(pady=10)
progress_label.pack(pady=10)

root.geometry("400x300")
root.mainloop()
