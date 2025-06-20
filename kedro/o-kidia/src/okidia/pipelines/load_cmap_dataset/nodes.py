"""
This is a boilerplate pipeline 'load_cmap_dataset'
generated using Kedro 0.18.0
"""
from __future__ import annotations
import json
import pandas as pd
import json
import csv
from tkinter.messagebox import NO

from typing import Callable

from .data_manipulation.game_session import GameSession


def validate_json(json_dataset: dict[str, Callable]) -> dict[str, Callable]:
    valid_dataset = {}
    for key, data_loading_func in json_dataset.items():
        try:
            # Call explicitly to generate the data from file
            json_data = data_loading_func()
            # Try to create a GameSession object from the data to check if
            # it is valid
            _ = GameSession.from_dict(json_data)
        except BaseException as exc:
            print(
                f"There was a problem while loading the json file {key}. "
                f"Exception raised: {type(exc)}"
            )
            print(exc)
        else:
            # If no error occured with the current file, we save it
            valid_dataset[key] = data_loading_func
    return valid_dataset
