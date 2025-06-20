"""Module that assert the integrity of the C-MAP dataset and decrypts its
video files.
"""
import argparse
from pathlib import Path

import pandas as pd
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

from src.utils.definitions import (
    CMAP_DATASET_COLUMNS,
    CMAP_ROOT_LOC,
    CMAP_TARGET_DIR,
)
from src.utils.exceptions import UnexpectedFormatError


def load_cmap_video_keys(file_path: Path) -> pd.DataFrame:
    """
    Load the .csv file that contains the keys to decrypt the videos recorded in
    the C-MAP project.

    Args:
        file_path: a Path pointing to the .csv file of the C-MAP dataset

    Returns: a pandas dataframe with all the information needed to decrypt the
    C-MAP video dataset
    """
    # Assert that file_path exists...
    if not file_path.exists():
        raise FileNotFoundError(f"Couldn't find file at: {file_path}")
    # and it is a file
    if not file_path.is_file():
        raise FileExistsError(
            f"The path given leads to a folder and not a " f"file: {file_path}"
        )

    # Load the file: it should have a header that contains 5 fields
    try:
        dataframe = pd.read_csv(file_path, sep=",", header=0)
        assert dataframe.columns == CMAP_DATASET_COLUMNS
    except Exception as ex:
        print(ex)
        raise UnexpectedFormatError(
            f"Problem opening the file loc" f"ated at {file_path}"
        ) from ex
    return dataframe


def find_decrypted_file(
    encrypted_filepath: Path,
    output_dir_path: Path,
    session_id: str,
    video_tag: str,
    replace_files: bool,
) -> Path:
    """Creates a path where the decrypted file should be located,
    and eventually creates the folder tree leading to it.

    Args:
        encrypted_filepath (Path): the path pointing to the encrypted file
        output_dir_path (Path): the decrypted data root location
        session_id (str): the id session of the encrypted file
        video_tag (str): the associated video tag (e.g. ScreenCalibration)
        replace_files (bool): a boolean set to True if we want to replace
        the existing decrypted file, False otherwise.

    Returns: a path pointing to the decrypted file location

    Raises: FileExistsError

    """
    decrypted_filepath = output_dir_path.joinpath(
        "decrypted_videos",
        session_id,
        video_tag + "_" + encrypted_filepath.stem,
    ).resolve()
    # If the decrypted file already exists, and we don't want to replace it,
    # raise exception
    if decrypted_filepath.exists() and not replace_files:
        raise FileExistsError(
            f"The decrypted file already exists! ({decrypted_filepath})"
        )
    # Create the parent directory path (eventually). Does nothing if it exists
    decrypted_filepath.parent.mkdir(parents=True, exist_ok=True)
    return decrypted_filepath


def decrypt_encrypted_file(
    encrypted_filepath: Path,
    iv_filepath: Path,
    decrypted_file_path: Path,
    encryption_key: str,
) -> None:
    """Decrypts a video file and create a new (decrypted) file.

    Args:
        encrypted_filepath (Path): a path pointing to the encrypted file
        iv_filepath (Path): a path pointing to the associated iv file
        decrypted_file_path (Path): a path pointing to the output root location
        encryption_key (str): a string representing the encryption key
         associated with the file

    Returns: nothing

    """
    # Retrieve iv from file
    iv_b: bytes = bytearray.fromhex(
        # We want the 32 first characters only (no escape characters!)
        iv_filepath.read_text(encoding="utf-8")[:32]
    )
    iv_b = iv_b.decode("unicode-escape").encode("raw_unicode_escape")

    # Transform the encryption key to bytes
    key: bytes = bytes.fromhex(encryption_key)

    # Derive the key from the encryption key and iv
    pbkdf = PBKDF2(password=key, salt=iv_b, dkLen=48, count=1042)

    # Retrieve key and iv
    key = pbkdf[:32]
    iv_b = pbkdf[32:]

    # Create the cipher
    cipher = AES.new(key, AES.MODE_CBC, iv_b)

    # Open the new file for decrypted data
    with open(decrypted_file_path, mode="wb") as decrypted_file:
        # Bytes buffer
        buffer = b""
        with open(encrypted_filepath, "rb") as encrypted_file:
            # Read the encrypted file, by lines
            lines: list[bytes] = encrypted_file.readlines()

            # Process each line...
            line: bytes
            for line in lines:
                if buffer != b"":
                    data = buffer + line
                else:
                    data = line
                buffer = data[16 * (len(data) // 16):]  # fmt: skip
                data = data[: 16 * (len(data) // 16)]
                # Then decrypt this data and write it to the file
                decrypted = cipher.decrypt(data)
                decrypted_file.write(decrypted)


def find_encrypted_file(
    root_dir: Path, session_id: str, filename: str
) -> Tuple[Path, Path]:
    """Retrieves the encrypted file location.

    Args:
        root_dir: the C-MAP dataset root location
        session_id: the session ID of the video
        filename: the video name (xxx.mp4.enc)

    Returns: A tuple that contains the encrypted video path and the
    associated iv file path

    """
    # Create the file path pointing to ...
    return (
        # the encrypted video and...
        root_dir.joinpath(
            "S3 files", "videos", session_id, filename
        ).resolve(),
        # the iv file
        root_dir.joinpath(
            "S3 files", "videos", session_id, filename.split(".")[0] + ".iv"
        ).resolve(),
    )


def decrypt_videos_from_df_row(
    row_df: pd.Series,
    input_dir: Path,
    output_dir: Path,
    replace_files: bool,
    check_integrity: bool,
) -> None:
    """
    The decryption process of a single line from the dataframe that contains
    all the information about the C-MAP dataset.

    Args:
        input_dir: a Path pointing at the C-MAP data root folder
        row_df: a pandas Series with information about one
        encrypted video
        output_dir: the target folder, where to store the decrypted video
        replace_files: a boolean that is True when we want to replace the
        decrypted file if they already exist, False otherwise
        check_integrity: a boolean that is True for the function to check if
        the input and output files are already existing

    Returns: nothing

    """
    # Unpacking the line of the dataframe
    (session_id, filename, key, tag, filesize) = row_df.values
    # Find the video file path to decrypt
    encrypted_file_path, iv_file_path = find_encrypted_file(
        input_dir, session_id, filename
    )
    try:
        # Check if there is a file there...
        if not encrypted_file_path.exists() and check_integrity:
            raise FileNotFoundError(
                f"No file found at this location: " f"{encrypted_file_path}"
            )
        if not iv_file_path.exists() and check_integrity:
            raise FileNotFoundError(
                f"No file found at this location: " f"{iv_file_path}"
            )
        # and if the file size is correct
        if (
            not encrypted_file_path.stat().st_size == filesize
            and check_integrity
        ):
            raise AssertionError(
                f"File size does not match (found "
                f"{encrypted_file_path.stat().st_size} instead of "
                f"{filesize})"
            )
        # Create the decrypted filepath from the given arguments
        decrypted_filepath: Path = find_decrypted_file(
            encrypted_file_path,
            output_dir,
            session_id,
            tag,
            replace_files,
        )
        # We decrypt the video, and store it in the location defined by
        # decrypted_filepath
        decrypt_encrypted_file(
            encrypted_file_path,
            iv_file_path,
            decrypted_filepath,
            key,
        )
    except (
        FileNotFoundError,
        AssertionError,
        FileExistsError,
        UnicodeDecodeError,
    ) as ex:
        print(ex)


def args_parser() -> argparse.Namespace:
    """This function defines and runs the arguments' parser for the function
    main().

    Returns: a Namespace

    """
    # Parser creation
    parser = argparse.ArgumentParser(
        description="Utility function that check the integrity of the C-MAP "
        "dataset and decrypts the videos if needed."
    )
    parser.add_argument(
        "--overwrite",
        help="a flag that allows overwriting existant files",
        action="store_false",
    )
    parser.add_argument(
        "--check-integrity",
        help="a flag that indicates if the program "
        "should check the integrity of the dataset",
        action="store_false",
    )
    parser.add_argument(
        "--cmap-root",
        type=Path,
        default=CMAP_ROOT_LOC,
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=CMAP_TARGET_DIR,
    )
    return parser.parse_args()


def main(parsed_args: argparse.Namespace) -> None:
    """Main function that runs the program, with the given parsed arguments.

    Args:
        parsed_args: the inputs arguments

    Returns: nothing

    """

    cmap_videos_keys_file_path = parsed_args.cmap_root.resolve().joinpath(
        Path("Videos keys/video_keys.csv")
    )

    # Load the .csv file with the wrap function
    keys_df: pd.DataFrame = load_cmap_video_keys(cmap_videos_keys_file_path)

    # Vectorize, for each line we decrypt the video and store it to the
    # target_dir
    keys_df.apply(
        lambda x: decrypt_videos_from_df_row(
            x,
            parsed_args.cmap_root.resolve(),
            parsed_args.output_dir.resolve(),
            parsed_args.overwrite,
            parsed_args.check_integrity,
        ),
        axis=1,
    )


if __name__ == "__main__":
    main(args_parser())
