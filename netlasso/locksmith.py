import os
from typing import Union

from cryptography.fernet import Fernet

from .coreutils import log, CURRENT_FILE_DIRECTORY


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


def get_encryption_key() -> bytes:
    """
    Retrieve the encryption key from .encryption-key.
    :return: Encryption key.
    """
    encryption_key_path = os.path.join(CURRENT_FILE_DIRECTORY, ".encryption-key")
    with open(encryption_key_path, "rb") as encryption_key_file:
        return encryption_key_file.read()


def set_encryption_key() -> bytes:
    """
    Generates an encryption key and writes it to .encryption-key
    :return: Written encryption key.
    """
    encryption_key_path = os.path.join(CURRENT_FILE_DIRECTORY, ".encryption-key")
    new_key = Fernet.generate_key()
    with open(encryption_key_path, "wb") as encryption_key_file:
        encryption_key_file.write(new_key)

    log.info(f"Encryption key written: {encryption_key_file.name}")

    return new_key


def set_api_key(api_key: str) -> Union[str, None]:
    """
    Retrieve or store the Netlas.io API key.
    If the key is not stored, it encrypts and saves it. Otherwise, it retrieves and decrypts it.

    :param api_key: The API key provided as input.
    :return: The final API key, either retrieved from the file or the one provided by the user.
    """
    api_key_path = os.path.join(CURRENT_FILE_DIRECTORY, ".netlas-auth")
    final_api_key = None
    try:
        # If API key exists, decrypt and retrieve it.
        if (
            os.path.exists(api_key_path) and os.path.getsize(api_key_path) == 140
        ):  # Encrypted API key size is 140 bytes
            # Get or Set the encryption key.

            get_key = get_encryption_key()
            with open(api_key_path, "rb") as api_key_file:
                encrypted_api_key = api_key_file.read()
                final_api_key = decrypt_data(get_key, encrypted_api_key)
                if api_key:
                    log.info(
                        f"To re-authenticate with a new API Key, "
                        f"remove the current [italic]Netlas.io API key[/] and its "
                        f"[italic]encryption key[/] located in "
                        f"{CURRENT_FILE_DIRECTORY}."
                    )
        else:
            if api_key and len(api_key) == 32:
                set_key = set_encryption_key()
                encrypted_api_key = encrypt_data(set_key, api_key)
                with open(api_key_path, "wb") as api_key_file:
                    api_key_file.write(encrypted_api_key)

                log.info(f"Netlas.io API key written: {api_key_path}")
                final_api_key = api_key
            else:
                log.warning(
                    f"{api_key} does not appear to be a valid Netlas.io API key."
                )

        return final_api_key

    except Exception as e:
        log.error(f"An error occurred while handling the API key: {e}")
        raise
