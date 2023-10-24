import os

from cryptography.fernet import Fernet

from .coreutils import log, CURRENT_FILE_DIRECTORY


def generate_encryption_key() -> bytes:
    """
    Generate a key for encryption and decryption using Fernet.
    :return: Generated encryption key.
    """
    return Fernet.generate_key()


def encrypt_data(key: bytes, data: str) -> bytes:
    """
    Encrypt the given data using the provided key.
    :param key: Encryption key.
    :param data: Data to be encrypted.
    :return: Encrypted data.
    """
    cipher = Fernet(key)
    return cipher.encrypt(data.encode())


def decrypt_data(key: bytes, encrypted_data: bytes) -> str:
    """
    Decrypt the given encrypted data using the provided key.
    :param key: Encryption key.
    :param encrypted_data: Data to be decrypted.
    :return: Decrypted data as string.
    """
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_data).decode()


def get_api_key(api_key: str) -> str:
    """
    Retrieve or store the Netlas.io API key.
    If the key is not stored, it encrypts and saves it. Otherwise, it retrieves and decrypts it.

    :param api_key: The API key provided as input.
    :return: The final API key, either retrieved from the file or the one provided by the user.
    """
    # Get or Set the encryption key.
    encryption_key = get_encryption_key()

    api_key_path = os.path.join(CURRENT_FILE_DIRECTORY, ".netlas-auth")
    try:
        # If API key exists, decrypt and retrieve it.
        if os.path.exists(api_key_path) and os.path.getsize(api_key_path) > 0:
            with open(api_key_path, "rb") as api_key_file:
                encrypted_api_key = api_key_file.read()
                final_api_key = decrypt_data(encryption_key, encrypted_api_key)
                if api_key:
                    log.info(
                        f"Netlas.io API key is already configured: {api_key_file.name}"
                    )
        else:
            # If API key doesn't exist, encrypt the provided key and store it.
            encrypted_api_key = encrypt_data(encryption_key, api_key)
            with open(api_key_path, "wb") as api_key_file:
                api_key_file.write(encrypted_api_key)

            log.info(f"Netlas.io API key written: {api_key_path}")
            final_api_key = api_key
    except Exception as e:
        log.error(f"An error occurred while handling the API key: {e}")
        raise

    return final_api_key


def get_encryption_key() -> bytes:
    """
    Retrieve the encryption key from file or generate if it doesn't exist.
    :return: Encryption key.
    """
    try:
        # If encryption key exists, retrieve it.
        if os.path.exists(KEY_PATH) and os.path.getsize(KEY_PATH) > 0:
            with open(KEY_PATH, "rb") as encryption_key_file:
                return encryption_key_file.read()
        else:
            # If encryption key doesn't exist, generate a new one and store it.
            new_key = generate_encryption_key()
            with open(KEY_PATH, "wb") as encryption_key_file:
                encryption_key_file.write(new_key)

            log.info(f"Encryption key written: {encryption_key_file.name}")
            return new_key
    except Exception as e:
        log.error(f"An error occurred while handling the encryption key: {e}")
        raise


# Path to where the encryption key will be stored.
KEY_PATH = os.path.join(CURRENT_FILE_DIRECTORY, ".encryption-key")
