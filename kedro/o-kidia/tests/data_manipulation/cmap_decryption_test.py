"""Tests associated with cmap_decryption.py
"""
from pathlib import Path

import pytest

from src.data_manip.cmap_decryption import load_cmap_video_keys
from src.utils.definitions import TEST_RESOURCES_ROOT_LOC
from src.utils.exceptions import UnexpectedFormatError


def test_load_cmap_video_keys():
    """Tests checking the loading of the C-MAP dataset information file.

    Returns: nothing

    """
    # File does not exist
    with pytest.raises(FileNotFoundError):
        load_cmap_video_keys(Path("/a.txt"))

    # Given path is a folder
    with pytest.raises(FileExistsError):
        load_cmap_video_keys(Path("/"))

    with pytest.raises(UnexpectedFormatError):
        load_cmap_video_keys(
            TEST_RESOURCES_ROOT_LOC.joinpath(
                "tests", "data_manip", "incorrect_csv.csv"
            )
        )


def decrypt_videos_from_df_row_test():
    """

    Returns:

    """


def find_encrypted_file_test():
    """

    Returns:

    """


def decrypt_encrypted_file_test():
    """

    Returns:

    """


def find_decrypted_file_test():
    """

    Returns:

    """


def load_cmap_video_keys_test():
    """

    Returns:

    """
