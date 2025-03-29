import socket
import os

def send_file(host, port, file_path):
    if not os.path.exists(file_path):
        print("Error: File does not exist!")
        return

    # Get the file name from the path
    file_name = os.path.basename(file_path)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    # Send the file name
    client_socket.send(file_name.encode())

    # Send the file content
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            client_socket.send(chunk)

    print(f"File {file_name} sent successfully!")
    client_socket.close()

if __name__ == "__main__":
    host = input("Enter server IP: ")
    port = int(input("Enter server port: "))
    file_path = input("Enter the path of the file to send: ")
    send_file(host, port, file_path)
