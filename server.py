import socket
import os

def start_server(host='0.0.0.0', port=65432, output_dir='received_files'):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server started on {host}:{port}, waiting for connections...")

    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    # Receive the file name
    file_name = conn.recv(1024).decode()
    print(f"Receiving file: {file_name}")

    # Open the file for writing
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, 'wb') as f:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            f.write(data)

    print(f"File received and saved to {file_path}")
    conn.close()

if __name__ == "__main__":
    start_server()
