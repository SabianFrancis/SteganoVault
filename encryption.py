from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def encrypt_file(password, input_file, output_file):
    salt = os.urandom(16)  # Generate a random salt
    key = PBKDF2HMAC(algorithm=SHA256(), length=32, salt=salt, iterations=100000).derive(password.encode())
    iv = os.urandom(16)  # Generate a random initialization vector

    with open(input_file, "rb") as f:
        data = f.read()

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()

    with open(output_file, "wb") as f:
        f.write(salt + iv + encrypted_data)  # Save salt, IV, and encrypted data

from cryptography.exceptions import InvalidTag

def decrypt_file(password, input_file, output_file):
    try:
        with open(input_file, "rb") as f:
            salt = f.read(16)  # Read the salt
            iv = f.read(16)  # Read the IV
            encrypted_data = f.read()  # Read the encrypted content

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

        print(f"Decryption successful! Output saved to {output_file}")

    except InvalidTag:
        print("Error: Incorrect password. Decryption failed.")
    except FileNotFoundError:
        print("Error: Input file not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

