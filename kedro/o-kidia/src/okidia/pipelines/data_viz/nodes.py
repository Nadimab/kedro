"""
This is a boilerplate pipeline 'data_viz'
generated using Kedro 0.18.0
"""
from __future__ import annotations

from typing import Callable

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from ..load_cmap_dataset.data_manipulation.game_session import GameSession


def plot_challenge(game_session: GameSession, challenge: int, ax=None):
    curve = pd.DataFrame.from_records([{"x": point[0], "y": point[1], "t": point[2], "type": "model"} for point in game_session.sorted_activities[0].challenges[challenge].curve_points()])
    curve_user = pd.DataFrame.from_records([{"x": point[0], "y": point[1], "t": point[2], "type": "user"} for point in game_session.sorted_activities[0].challenges[challenge].digit_curve()])
    sns.lineplot(x="x", y="y", data=curve, color="red", ax=ax, sort=False)
    sns.lineplot(x="x", y="y", data=curve_user, ax=ax, sort=False)


def plot_game_session(validated_dataset: dict[str, Callable]) -> dict[str,Callable] :
    png_dataset={}
    for key, data_loading_func in validated_dataset.items():
        game_session = GameSession.from_dict(data_loading_func())
        key=key[:-4]+"png"
        fig, axis = plt.subplots(5, 3)
        fig.set_size_inches(20, 20)
        for challenge in range(len(game_session.sorted_activities[0].challenges)):
         plot_challenge(game_session, challenge, axis[challenge // 3, challenge % 3])
         plt.close("all")
        png_dataset[key]=fig 
    return png_dataset 