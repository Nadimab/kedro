from __future__ import annotations

import json
import os

import numpy as np
import pandas as pd
import pytest

from src.okidia.pipelines.load_cmap_dataset.data_manipulation.exceptions import (
    DigitInputsEmptyError,
    PointsEmptyError,
    ScreenCalibrationOrActivitiesEmptyError,
)
from src.okidia.pipelines.load_cmap_dataset.data_manipulation.game_session import (
    GameSession,
)


def test_valid_json_parsing():
    GameSession.from_json(
        os.path.join(os.path.dirname(__file__), "dummy_data", "test.json")
    )


def test_valid_dataframe_creation():
    game_session = GameSession.from_json(
        os.path.join(os.path.dirname(__file__), "dummy_data", "test.json")
    )
    df = game_session.to_dataframe()
    cols = [
        "ts",
        "touch_count",
        "x",
        "y",
        "finger_id",
        "phase_digit",
        "activity",
        "challenge",
        "phase",
    ]
    assert isinstance(df, pd.DataFrame) == True
    print(df.columns)
    assert df.shape == (len(game_session._digit_inputs_dataframe()), len(cols))
    assert df.columns.tolist() == cols


def test_response_time():
    game_session = GameSession.from_json(
        os.path.join(os.path.dirname(__file__), "dummy_data", "test.json")
    )
    resp_data = game_session.response_times()
    assert resp_data["response_time"].isna().sum() == 0
    assert (resp_data["response_time"] < 0).sum() == 0


def test_game_session_score():
    game_session = GameSession.from_json(
        os.path.join(os.path.dirname(__file__), "dummy_data", "test.json")
    )
    activity_df, _ = game_session.score()
    assert len(activity_df) == 5
    assert activity_df["activity"].tolist() == [
        "CrocosMaze",
        "DJCrocos",
        "CrocosVocabulo",
        "CrocoFactory",
        "CrocoSpot",
    ]
    assert (
        activity_df["score"].round(4).tolist()
        == np.round([0, 11 / 12, 14 / 28, 19 / 24, 1 / 2], 4).tolist()
    )


def test_response_time():
    game_session = GameSession.from_json(
        os.path.join(os.path.dirname(__file__), "dummy_data", "test.json")
    )
    resp_data = game_session.response_times()
    assert resp_data["response_time"].isna().sum() == 0
    assert (resp_data["response_time"] < 0).sum() == 0


def test_game_session_score():
    game_session = GameSession.from_json(
        os.path.join(os.path.dirname(__file__), "dummy_data", "test.json")
    )
    activity_df, _ = game_session.score()
    assert len(activity_df) == 5
    assert activity_df["activity"].tolist() == [
        "CrocosMaze",
        "DJCrocos",
        "CrocosVocabulo",
        "CrocoFactory",
        "CrocoSpot",
    ]
    assert (
        activity_df["score"].round(4).tolist()
        == np.round([8.6002, 11 / 12, 14 / 28, 19 / 24, 0.0833], 4).tolist()
    )


@pytest.mark.parametrize(
    "content,exception",
    [
        # Test empty json file
        ("", json.decoder.JSONDecodeError),
        # Test empty json file with simple object
        ("{}", TypeError),
        # Test completely wrong json file
        ('{"game_id": "test"}', TypeError),
        # Test corrupted json file with missing calibration
        (
            '{"device_name":"Lenovo Yoga Tab 11", "device_model":"LENOVO Lenovo YT-J706F", "resolution":"2000 x 1200 @ 60Hz", "soft_version":1677, "device_type":"Handheld", "student_id":"2021_10_20_09_22_12_447", "device_uid": "", "soft_configuration_name": "", "screenCalibration": []}',
            ScreenCalibrationOrActivitiesEmptyError,
        ),
        # Test corrupted json file with missing activities
        (
            '{"device_name":"Lenovo Yoga Tab 11", "device_model":"LENOVO Lenovo YT-J706F", "resolution":"2000 x 1200 @ 60Hz", "soft_version":1677, "device_type":"Handheld", "student_id":"2021_10_20_09_22_12_447", "device_uid": "", "soft_configuration_name": ""}',
            ScreenCalibrationOrActivitiesEmptyError,
        ),
        # Test corrupted json file with empty activities
        (
            '{"device_name":"Lenovo Yoga Tab 11", "device_model":"LENOVO Lenovo YT-J706F", "resolution":"2000 x 1200 @ 60Hz", "soft_version":1677, "device_type":"Handheld", "student_id":"2021_10_20_09_22_12_447", "device_uid": "", "soft_configuration_name": "", "activities": []}',
            ScreenCalibrationOrActivitiesEmptyError,
        ),
        # Test corrupted json file with a wrong refresh_rate
        (
            '{"device_name":"Lenovo Yoga Tab 11", "device_model":"LENOVO Lenovo YT-J706F", "resolution":"2000 x 1200 @ 6mHz", "soft_version":1677, "device_type":"Handheld", "student_id":"2021_10_20_09_22_12_447", "device_uid": "", "soft_configuration_name": "", "screenCalibration": [""], "activities": [{"start_ts":1634718284.65007,"end_ts":1634718600.10342,"game_name":"CrocosMaze","video":{"stop_ts":1634718599.93298,"path":"/storage/emulated/0/Android/data/com.exkee.crocos/files/.local/share/Sessions/2021_10_20_09_22_12_447/recording_2021_10_20_11_24_44_652.mp4","start_ts":1634718284.64996}}]}',
            ValueError,
        ),
        # Test corrupted json file with a wrong format for the resolution
        (
            '{"device_name":"Lenovo Yoga Tab 11", "device_model":"LENOVO Lenovo YT-J706F", "resolution":"no-format", "soft_version":1677, "device_type":"Handheld", "student_id":"2021_10_20_09_22_12_447", "device_uid": "", "soft_configuration_name": "", "screenCalibration": [""], "activities": [{"start_ts":1634718284.65007,"end_ts":1634718600.10342,"game_name":"CrocosMaze","video":{"stop_ts":1634718599.93298,"path":"/storage/emulated/0/Android/data/com.exkee.crocos/files/.local/share/Sessions/2021_10_20_09_22_12_447/recording_2021_10_20_11_24_44_652.mp4","start_ts":1634718284.64996}}]}',
            ValueError,
        ),
        # Test corrupted json file with no digit inputs inside a calibration
        (
            '{"device_name":"Lenovo Yoga Tab 11", "device_model":"LENOVO Lenovo YT-J706F", "resolution":"2000 x 1200 @ 60Hz", "soft_version":1677, "device_type":"Handheld", "student_id":"2021_10_20_09_22_12_447", "device_uid": "", "soft_configuration_name": "", "screenCalibration": [""], "activities": [{"start_ts":1634718284.65007,"end_ts":1634718600.10342,"game_name":"CrocosMaze","video":{"stop_ts":1634718599.93298,"path":"/storage/emulated/0/Android/data/com.exkee.crocos/files/.local/share/Sessions/2021_10_20_09_22_12_447/recording_2021_10_20_11_24_44_652.mp4","start_ts":1634718284.64996}}]}',
            DigitInputsEmptyError,
        ),
        # Test corrupted json file with no points inside a calibration
        (
            '{"device_name":"Lenovo Yoga Tab 11", "device_model":"LENOVO Lenovo YT-J706F", "resolution":"2000 x 1200 @ 60Hz", "soft_version":1677, "device_type":"Handheld", "student_id":"2021_10_20_09_22_12_447", "device_uid": "", "soft_configuration_name": "", "screenCalibration": ["", { "digit_inputs": [{"ts":1634718163.40101, "touchCount":1, "touches":[{"fingerId":0, "relativePosition_x":0.617191433906555, "relativePosition_y":0.222314760088921, "phase":"Ended"\r\n}]\r\n}]}], "activities": [{"start_ts":1634718284.65007,"end_ts":1634718600.10342,"game_name":"CrocosMaze","video":{"stop_ts":1634718599.93298,"path":"/storage/emulated/0/Android/data/com.exkee.crocos/files/.local/share/Sessions/2021_10_20_09_22_12_447/recording_2021_10_20_11_24_44_652.mp4","start_ts":1634718284.64996}}]}',
            PointsEmptyError,
        ),
    ],
)
def test_invalid_json_parsing(content: str, exception: Exception):
    pytest.raises(exception, GameSession.from_raw, content)


def test_valid_merge_game_session():
    session1 = GameSession.from_json(
        os.path.join(os.path.dirname(__file__), "dummy_data", "game_session_1.json")
    )
    session2 = GameSession.from_json(
        os.path.join(os.path.dirname(__file__), "dummy_data", "game_session_2.json")
    )
    session3 = GameSession.from_json(
        os.path.join(os.path.dirname(__file__), "dummy_data", "game_session_3.json")
    )
    session4 = GameSession.from_json(
        os.path.join(os.path.dirname(__file__), "dummy_data", "game_session_4.json")
    )
    session5 = GameSession.from_json(
        os.path.join(os.path.dirname(__file__), "dummy_data", "game_session_5.json")
    )
    session6 = GameSession.from_json(
        os.path.join(os.path.dirname(__file__), "dummy_data", "game_session_6.json")
    )
    game_session = GameSession.from_json(
        os.path.join(os.path.dirname(__file__), "dummy_data", "test.json")
    )
    assert (
        game_session == session1 | session2 | session3 | session4 | session5 | session6
    )


def test_game_session_from_files():
    game_session = GameSession.from_files(
        [
            os.path.join(
                os.path.dirname(__file__), "dummy_data", "game_session_1.json"
            ),
            os.path.join(
                os.path.dirname(__file__), "dummy_data", "game_session_2.json"
            ),
            os.path.join(
                os.path.dirname(__file__), "dummy_data", "game_session_3.json"
            ),
            os.path.join(
                os.path.dirname(__file__), "dummy_data", "game_session_4.json"
            ),
            os.path.join(
                os.path.dirname(__file__), "dummy_data", "game_session_5.json"
            ),
            os.path.join(
                os.path.dirname(__file__), "dummy_data", "game_session_6.json"
            ),
        ]
    )

    game_session_other = GameSession.from_json(
        os.path.join(os.path.dirname(__file__), "dummy_data", "test.json")
    )

    assert game_session == game_session_other
