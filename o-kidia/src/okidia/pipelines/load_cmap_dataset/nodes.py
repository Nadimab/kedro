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

'''
def extract_informations(validated_dataset: dict[str, Callable]):
    game_data={}
    for key, data_loading_func in validated_dataset.items():
        key_csv = key[:-4]+"xlsx"
        game_session = GameSession.from_dict(data_loading_func())
        #game_session.to_csv("data/03_primary"+str(game_session.student_id)+".csv").sort_values(by=["ts"],ascending=True)
        digit_inputs = game_session.to_dataframe().sort_values(by=["ts"], ascending=True)
        #digit_inputs.to_csv("data/03_primary/logs/"+str(game_session.student_id)+".csv", na_rep='NULL')
        digit_inputs['challenge'] = digit_inputs['challenge'].fillna('Null')
        digit_inputs['phase'] = digit_inputs['phase'].fillna('Null')
        game_data[key_csv] = digit_inputs #("data/03_primary/logs/"+str(i)+".csv", na_rep='NULL')
        #i+=1
    print(game_data)
    return game_data
'''
