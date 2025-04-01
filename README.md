# SteganoVault

SteganoVault is a secure file-sharing tool that combines **Cryptography** and **Steganography** techniques to ensure the confidentiality of your data. It allows users to encrypt text files, embed encrypted data into images, extract data, and share it directly over a network.

## Features
- 🔒 **Encrypt and Decrypt** text files using a password.
- 🖼️ **Embed and Extract** encrypted data into/from images.
- 🌐 **Send and Receive** files over a network via IP address.
- 💻 **Dark Sci-Fi Themed Interface** with red text on a black background.

## How to Use

### Running the Application
1. **Download the .exe file** from the [Releases](https://github.com/SabianFrancis/SteganoVault/releases/tag/v1.0.0) section.
2. Double-click the `.exe` file to launch the application.

### Encrypting a File
1. Click on the `Encrypt` button.
2. Select the text file you want to encrypt.
3. Enter a password and provide a name for the encrypted file.
4. Click `Save` to generate the encrypted file.

### Decrypting a File
1. Click on the `Decrypt` button.
2. Select the `.enc` file you want to decrypt.
3. Enter the password used during encryption.
4. Provide a name for the decrypted file and click `Save`.

### Embedding Data
1. Click on the `Embed` button.
2. Select the encrypted file and an image to hide the data in.
3. Click `Save` to generate the new steganographic image.

### Extracting Data
1. Click on the `Extract` button.
2. Select the steganographic image.
3. Click `Extract` to retrieve the hidden data.

### Sending Data via IP
1. Click on the `Send via IP` button.
2. Provide the recipient's IP address.
3. Click `Send`.

### Receiving Data
1. Click on the `Start Server` button.
2. Wait for the sender to initiate the transfer.

## Installation (For Developers)
1. Clone the repository:
```bash
 git clone https://github.com/SabianFrancis/SteganoVault.git
```
2. Install the dependencies:
```bash
 pip install -r requirements.txt
```
3. Run the application:
```bash
 python Eclipsa.py
```
## NOTE 
Those other files you see...
- Server.py
- Client.py
- Steganography.py
- Encryption.py 
- Tool.py
   
These are for `Terminal/Command line` use only so if you have these in a folder and navigate it through terminal and here are some examples for it all 

1.Encrypt a file:

`Example:`
```bash
python tool.py encrypt --file myfile.txt --password mypassword123 --output encrypted_file.txt
```
2.Decrypt a file:

`Example:`
```bash
python tool.py decrypt --file encrypted_file.txt --password mypassword123 --output decrypted_file.txt
```
3.Embed a file into an image:

`Example:`
```bash
python tool.py embed --image cover_image.png --file secret.txt --output image_with_secret.png
```
4.Extract a file into an image:

`Example:`
```bash
python tool.py extract --image image_with_secret.png --output extracted_file.txt       
```


## License
This project is licensed under the MIT License.

## Credits
Developed by Sabian Francis

---


