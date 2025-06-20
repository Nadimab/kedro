from __future__ import annotations

from pathlib import Path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class FileDecryption:
    valid_encrypted_extensions = (".okiv", ".okid")

    class UnexpectedEncryptionFormat(BaseException):
        pass

    @staticmethod
    def decrypt_single_file(
        encrypted_filepath: Path,
        key: bytes | str,
        salt: bytes | str,
        decrypted_filepath: Path,
        override=True,
    ) -> None:
        """Decrypts a single encrypted file, using given key and salt, with AES
        algorithm in CBC mode, and write decrypted data to another given
        location. If the output file already exists, it is overriden only if the
        override parameter is set to True (default).

        Args:
            encrypted_filepath: the encrypted file path
            key: the key used for decryption
            salt: the salt (or iv) used for decryption
            decrypted_filepath: the file path for decrypted data
            override: a boolean indicating whether to override an already
            existing decrypted file.

        Returns: None.

        """
        # Files checks (is not a directory, exists, can be overriden)
        # Can factorise this probably (or put a separate function
        # sanitize_inputs()?)
        if not encrypted_filepath.is_file():
            raise IsADirectoryError(
                f"Expected encrypted file to be a file path, but was given a "
                f"directory! {str(encrypted_filepath)}"
            )
        if not decrypted_filepath.is_file():
            raise IsADirectoryError(
                f"Expected decrypted file to be a file path, but was given a "
                f"directory! {str(decrypted_filepath)}"
            )
        if not (encrypted_filepath.exists()):
            raise FileNotFoundError(
                f"Encrypted file could not be found! {encrypted_filepath}"
            )
        if decrypted_filepath.exists() and not override:
            raise FileExistsError(
                f"Output file already exists. If you wish to "
                f"override it, set override=True. {decrypted_filepath}"
            )

        # Check if encrypted file has an expected format
        if not (
            encrypted_filepath.suffix
            in FileDecryption.valid_encrypted_extensions
        ):
            raise FileDecryption.UnexpectedEncryptionFormat(
                f"The encrypted file cannot be decrypted, it is in the wrong "
                f"format. Got {encrypted_filepath.suffix}, allowed format "
                f"are {FileDecryption.valid_encrypted_extensions}"
            )

        # Change key/salt types to hexadecimal array
        if type(key) is str:
            key = bytearray.fromhex(key)
        if type(salt) is str:
            salt = bytearray.fromhex(salt)

        # Create cipher decryptor
        try:
            decryptor = Cipher(
                algorithms.AES(key), modes.CBC(salt)
            ).decryptor()
        except ValueError:
            raise

        # Open input and output files, read/write bytes
        with open(encrypted_filepath, mode="rb") as encrypted_file:
            with open(decrypted_filepath, mode="wb") as decrypted_file:
                # Decrypt data as a whole
                # Warning: What if the file is too big? Look up cryptography
                # update_into() function with fixed buffer size.
                data: bytes = encrypted_file.read()
                decrypted_data: bytes = (
                    decryptor.update(data) + decryptor.finalize()
                )
                decrypted_file.write(decrypted_data)
