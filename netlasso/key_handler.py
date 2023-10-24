from cryptography.fernet import Fernet

def generate_key() -> bytes:
    """
    Generate a key for encryption and decryption.
    """
    return Fernet.generate_key()

def encrypt_data(key: bytes, data: str) -> bytes:
    """
    Encrypt the given data using the provided key.
    """
    cipher = Fernet(key)
    return cipher.encrypt(data.encode())

def decrypt_data(key: bytes, encrypted_data: bytes) -> str:
    """
    Decrypt the given encrypted data using the provided key.
    """
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_data).decode()

def get_api_key(api_key: str) -> str:
    """
    Retrieve or store the Netlas.io API key.

    :param api_key: The API key provided as input.
    :return: The final API key, either retrieved from the file or the one provided by the user.
    """
    api_key_path = os.path.join(CURRENT_FILE_DIRECTORY, ".netlas-auth")

    # NOTE: For simplicity, I'm assuming the key is stored as a global constant or an environment variable.
    # Ideally, you'd want to securely manage this key too.
    KEY = generate_key()  # Or retrieve from a secure location

    try:
        if os.path.exists(api_key_path) and os.path.getsize(api_key_path) > 0:
            with open(api_key_path, "rb") as file:
                encrypted_api_key = file.read()
                final_api_key = decrypt_data(KEY, encrypted_api_key)
        else:
            encrypted_api_key = encrypt_data(KEY, api_key)
            with open(api_key_path, "wb") as file:
                file.write(encrypted_api_key)

            log.info(f"Netlas.io API key written to {api_key_path}")
            final_api_key = api_key
    except Exception as e:
        log.error(f"An error occurred while handling the API key: {e}")

    return final_api_key