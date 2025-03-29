import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from steganography import embed_file, extract_file
import os
import socket
import threading

# Main GUI setup
root = tk.Tk()
root.title("Secure File Sharing")
root.geometry("800x600")
root.resizable(True, True)
root.configure(bg="#1a1a2e")  # Dark Sci-Fi theme background

# Create a "received" folder if it doesn't exist
if not os.path.exists("received"):
    os.makedirs("received")

# Heading
title_label = tk.Label(
    root,
    text="Secure File Sharing",
    font=("Helvetica", 24, "bold"),
    fg="#e94560",
    bg="#1a1a2e"
)
title_label.pack(pady=20)

# Buttons with hover effects
def create_button(text, command):
    def on_enter(e):
        btn["background"] = "#e94560"
        btn["foreground"] = "#1a1a2e"

    def on_leave(e):
        btn["background"] = "#1a1a2e"
        btn["foreground"] = "#e94560"

    btn = tk.Button(
        root,
        text=text,
        command=command,
        font=("Helvetica", 14),
        fg="#e94560",
        bg="#1a1a2e",
        activebackground="#e94560",
        activeforeground="#1a1a2e",
        relief="flat",
        bd=0,
        padx=10,
        pady=5
    )
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

# Encrypt Button
def encrypt_action():
    file_path = filedialog.askopenfilename(title="Select File to Encrypt")
    if not file_path:
        return
    password = simpledialog.askstring("Input", "Enter Password", show="*")
    if not password:
        return
    output_file = filedialog.asksaveasfilename(
        title="Save Encrypted File As",
        defaultextension=".enc",
        filetypes=[("Encrypted Files", "*.enc")]
    )
    if not output_file:
        return
    try:
        salt = os.urandom(16)
        key = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        ).derive(password.encode())
        iv = os.urandom(16)

        with open(file_path, "rb") as f:
            data = f.read()

        cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(data) + encryptor.finalize()

        with open(output_file, "wb") as f:
            f.write(salt + iv + encrypted_data)

        messagebox.showinfo("Success", f"File encrypted successfully: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to encrypt file: {e}")

# Decrypt Button
def decrypt_action():
    file_path = filedialog.askopenfilename(title="Select File to Decrypt")
    if not file_path:
        return
    password = simpledialog.askstring("Input", "Enter Password", show="*")
    if not password:
        return
    output_file = filedialog.asksaveasfilename(
        title="Save Decrypted File As",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )
    if not output_file:
        return
    try:
        with open(file_path, "rb") as f:
            salt = f.read(16)
            iv = f.read(16)
            encrypted_data = f.read()

        key = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        ).derive(password.encode())

        cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
        decryptor = cipher.decryptor()
        data = decryptor.update(encrypted_data) + decryptor.finalize()

        with open(output_file, "wb") as f:
            f.write(data)

        messagebox.showinfo("Success", f"File decrypted successfully: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to decrypt file: {e}")

# Embed Button
def embed_action():
    image_path = filedialog.askopenfilename(title="Select Cover Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not image_path:
        return
    file_path = filedialog.askopenfilename(title="Select File to Embed")
    if not file_path:
        return
    output_image = filedialog.asksaveasfilename(
        title="Save Image with Embedded File As",
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png")]
    )
    if not output_image:
        return
    try:
        embed_file(image_path, file_path, output_image)
        messagebox.showinfo("Success", f"File embedded successfully into: {output_image}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to embed file: {e}")

# Extract Button
def extract_action():
    image_path = filedialog.askopenfilename(title="Select Image with Embedded File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not image_path:
        return
    output_file = filedialog.asksaveasfilename(
        title="Save Extracted File As",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )
    if not output_file:
        return
    try:
        extract_file(image_path, output_file)
        messagebox.showinfo("Success", f"File extracted successfully to: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to extract file: {e}")

# Send via IP
def send_via_ip():
    file_path = filedialog.askopenfilename(title="Select File to Send")
    if not file_path:
        return
    ip_address = simpledialog.askstring("Input", "Enter Recipient's IP Address")
    if not ip_address:
        return
    try:
        # Create a socket connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_address, 5000))  # Connect to the recipient's IP and port 5000

        # Send the file
        with open(file_path, "rb") as f:
            file_data = f.read()
        client_socket.sendall(file_data)
        client_socket.close()

        messagebox.showinfo("Success", f"File sent successfully to {ip_address}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send file: {e}")

# Start Server
def start_server():
    def server_thread():
        global received_folder  # Explicitly declare the global variable
        try:
            # Create a server socket
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(("0.0.0.0", 5000))  # Listen on all interfaces, port 5000
            server_socket.listen(1)
            messagebox.showinfo("Server", "Server started. Waiting for incoming files...")

            # Accept a connection
            client_socket, client_address = server_socket.accept()
            messagebox.showinfo("Server", f"Connection established with {client_address}")

            # Receive the file
            file_data = b""
            while True:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                file_data += chunk

            # Save the received file
            received_file_path = os.path.join(received_folder, f"received_file_{client_address[0]}.bin")
            with open(received_file_path, "wb") as f:
                f.write(file_data)

            client_socket.close()
            server_socket.close()
            messagebox.showinfo("Server", f"File received and saved to: {received_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Server error: {e}")

    # Start the server in a separate thread
    threading.Thread(target=server_thread, daemon=True).start()

# Layout
button_frame = ttk.Frame(root)
button_frame.pack(pady=20)

buttons = [
    ("Encrypt File", encrypt_action),
    ("Decrypt File", decrypt_action),
    ("Embed File in Image", embed_action),
    ("Extract File from Image", extract_action),
    ("Send via IP", send_via_ip),
    ("Start Server", start_server),
]

for text, cmd in buttons:
    btn = create_button(text, cmd)
    btn.pack(pady=10, fill="x", padx=50)



# Run the GUI main loop
root.mainloop()