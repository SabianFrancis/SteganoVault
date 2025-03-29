import argparse
from encryption import encrypt_file, decrypt_file
from steganography import embed_file, extract_file

def main():
    parser = argparse.ArgumentParser(description="Secure File Sharing Tool")
    subparsers = parser.add_subparsers(dest="command")

    encrypt_parser = subparsers.add_parser("encrypt")
    encrypt_parser.add_argument("--file", required=True, help="File to encrypt")
    encrypt_parser.add_argument("--password", required=True, help="Encryption password")
    encrypt_parser.add_argument("--output", required=True, help="Output encrypted file")

    decrypt_parser = subparsers.add_parser("decrypt")
    decrypt_parser.add_argument("--file", required=True, help="Encrypted file")
    decrypt_parser.add_argument("--password", required=True, help="Decryption password")
    decrypt_parser.add_argument("--output", required=True, help="Output decrypted file")

    embed_parser = subparsers.add_parser("embed")
    embed_parser.add_argument("--image", required=True, help="Cover image file")
    embed_parser.add_argument("--file", required=True, help="File to embed")
    embed_parser.add_argument("--output", required=True, help="Output image with embedded file")

    extract_parser = subparsers.add_parser("extract")
    extract_parser.add_argument("--image", required=True, help="Image with embedded file")
    extract_parser.add_argument("--output", required=True, help="Extracted file")

    args = parser.parse_args()

    try:
        if args.command == "encrypt":
            encrypt_file(args.password, args.file, args.output)
        elif args.command == "decrypt":
            decrypt_file(args.password, args.file, args.output)
        elif args.command == "embed":
            embed_file(args.image, args.file, args.output)
        elif args.command == "extract":
            extract_file(args.image, args.output)
        else:
            print("Error: Invalid command. Use --help for usage instructions.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
