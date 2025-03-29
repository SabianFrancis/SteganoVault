from PIL import Image
import os
def embed_file(image_path, input_file, output_image):
    try:
        from PIL import Image
        import os

        img = Image.open(image_path)
        pixels = img.load()

        max_capacity = img.width * img.height * 3 // 8
        file_size = os.path.getsize(input_file)

        if file_size > max_capacity:
            raise ValueError(f"File too large to embed in this image. Max capacity: {max_capacity} bytes")

        file_size_binary = format(file_size, '032b')
        with open(input_file, "rb") as f:
            data = f.read()
        binary_data = file_size_binary + ''.join(format(byte, '08b') for byte in data)

        idx = 0
        for y in range(img.height):
            for x in range(img.width):
                if idx < len(binary_data):
                    r, g, b = pixels[x, y]
                    r = (r & ~1) | int(binary_data[idx])
                    pixels[x, y] = (r, g, b)
                    idx += 1

        img.save(output_image)
        print(f"File successfully embedded into image: {output_image}")

    except FileNotFoundError:
        print("Error: Input file or image not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



def extract_file(image_path, output_file):
    try:
        from PIL import Image

        img = Image.open(image_path)
        pixels = img.load()

        binary_data = ""
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pixels[x, y]
                binary_data += str(r & 1)

        file_size_binary = binary_data[:32]
        file_size = int(file_size_binary, 2)

        file_data_binary = binary_data[32:32 + (file_size * 8)]
        byte_data = [file_data_binary[i:i+8] for i in range(0, len(file_data_binary), 8)]
        byte_data = bytearray([int(byte, 2) for byte in byte_data])

        with open(output_file, "wb") as f:
            f.write(byte_data)

        print(f"File successfully extracted to: {output_file}")

    except FileNotFoundError:
        print("Error: Input image not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


