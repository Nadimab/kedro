from pathlib import Path

import pytest

from src.decryption.decryption import FileDecryption

encrypted_filepath_test = Path(
    "./external_resources/encryption" "/encrypted_video.okiv"
).resolve()
decrypted_filepath_test = encrypted_filepath_test.parent.joinpath(
    "decrypted_file.mp4"
)
any_file = encrypted_filepath_test.parent.joinpath("test_encrypted_file.zip")
key_test = "e2db8b9e17d0f102d284caea3e687101c7aaf93a0a30cc39467d6c0b0cb0cfac"
salt_test = "6273eaf3a83e20e64ecd7bb17d8b836e"


@pytest.mark.parametrize(
    "input_kwargs, exception, exception_message",
    [
        # No args
        (
            {},
            TypeError,
            ".*missing 4 required positional arguments.*",
        ),
        # Decrypted file is not a file
        (
            {
                "encrypted_filepath": any_file,
                "decrypted_filepath": Path(""),
                "key": "",
                "salt": "",
            },
            IsADirectoryError,
            "^Expected decrypted file to be a file path.*",
        ),
        # Encrypted file exists, but has wrong format
        (
            {
                "encrypted_filepath": any_file,
                "decrypted_filepath": decrypted_filepath_test,
                "key": key_test,
                "salt": "",
            },
            FileDecryption.UnexpectedEncryptionFormat,
            "^The encrypted file cannot be decrypted.*",
        ),
        # Invalid key
        (
            {
                "encrypted_filepath": encrypted_filepath_test,
                "decrypted_filepath": decrypted_filepath_test,
                "key": "",
                "salt": "",
            },
            ValueError,
            "^Invalid key size.*",
        ),
        # Invalid IV
        (
            {
                "encrypted_filepath": encrypted_filepath_test,
                "decrypted_filepath": decrypted_filepath_test,
                "key": key_test,
                "salt": "",
            },
            ValueError,
            "^Invalid IV size.*",
        ),
    ],
)
def test_decrypt_single_file(input_kwargs, exception, exception_message):
    with pytest.raises(exception, match=exception_message):
        FileDecryption.decrypt_single_file(**input_kwargs)
