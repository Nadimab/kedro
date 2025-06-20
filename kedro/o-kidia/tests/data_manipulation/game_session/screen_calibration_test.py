import pytest

from src.okidia.pipelines.load_cmap_dataset.data_manipulation.exceptions import (
    DigitInputsEmptyError,
    PointsEmptyError,
)


@pytest.mark.parametrize(
    "input_kwargs,exception,exception_message",
    [
        ({}, TypeError, ".*missing 6 required positional argument.*"),
        (
            {"name": ""},
            TypeError,
            ".*missing 5 required positional argument.*",
        ),
        (
            {"name": "", "bump_ts": 0.00},
            TypeError,
            ".*missing 4 required positional argument.*",
        ),
        (
            {"name": "", "bump_ts": 0.00, "hit_ts": 0.00},
            TypeError,
            ".*missing 3 required positional argument.*",
        ),
        (
            {"name": "", "bump_ts": 0.00, "hit_ts": 0.00, "displayTime": 0.00},
            TypeError,
            ".*missing 2 required positional argument.*",
        ),
        (
            {
                "name": "",
                "bump_ts": 0.00,
                "hit_ts": 0.00,
                "displayTime": 0.00,
                "relativeScreenPositionX": 0.00,
            },
            TypeError,
            ".*missing 1 required positional argument.*",
        ),
        (
            {
                "name": 0,
                "bump_ts": 0.00,
                "hit_ts": 0.00,
                "displayTime": 0.00,
                "relativeScreenPositionX": 0.00,
                "relativeScreenPositionY": 0.00,
            },
            TypeError,
            "Expected a string for 'name', got <class 'int'>",
        ),
        (
            {
                "name": "",
                "bump_ts": 0,
                "hit_ts": 0.00,
                "displayTime": 0.00,
                "relativeScreenPositionX": 0.00,
                "relativeScreenPositionY": 0.00,
            },
            TypeError,
            "Expected a float for 'bump_ts', got <class 'int'>",
        ),
        (
            {
                "name": "",
                "bump_ts": 0.00,
                "hit_ts": 0,
                "displayTime": 0.00,
                "relativeScreenPositionX": 0.00,
                "relativeScreenPositionY": 0.00,
            },
            TypeError,
            "Expected a float for 'hit_ts', got <class 'int'>",
        ),
        (
            {
                "name": "",
                "bump_ts": 0.00,
                "hit_ts": 0.00,
                "displayTime": 0,
                "relativeScreenPositionX": 0.00,
                "relativeScreenPositionY": 0.00,
            },
            TypeError,
            "Expected a float for 'displayTime', got <class 'int'>",
        ),
        (
            {
                "name": "",
                "bump_ts": 0.00,
                "hit_ts": 0.00,
                "displayTime": 0.00,
                "relativeScreenPositionX": 0,
                "relativeScreenPositionY": 0.00,
            },
            TypeError,
            "Expected a float for 'relativeScreenPositionX', got <class 'int'>",
        ),
        (
            {
                "name": "",
                "bump_ts": 0.00,
                "hit_ts": 0.00,
                "displayTime": 0.00,
                "relativeScreenPositionX": 0.00,
                "relativeScreenPositionY": 0,
            },
            TypeError,
            "Expected a float for 'relativeScreenPositionY', got <class 'int'>",
        ),
    ],
)
def test_exception_new_calibration(input_kwargs, exception, exception_message):
    from src.okidia.pipelines.load_cmap_dataset.data_manipulation.game_session.screen_calibration import (
        Calibration,
    )

    with pytest.raises(exception, match=exception_message):
        Calibration(**input_kwargs)


def test_calibration_eq():
    from src.okidia.pipelines.load_cmap_dataset.data_manipulation.game_session.screen_calibration import (
        Calibration,
    )

    calibration_1 = Calibration(
        name="play",
        bump_ts=0.00,
        hit_ts=0.00,
        displayTime=0.00,
        relativeScreenPositionX=0.00,
        relativeScreenPositionY=0.00,
    )
    calibration_2 = Calibration(
        name="play",
        bump_ts=0.00,
        hit_ts=0.00,
        displayTime=0.00,
        relativeScreenPositionX=0.00,
        relativeScreenPositionY=0.00,
    )
    calibration_3 = Calibration(
        name="player",
        bump_ts=0.00,
        hit_ts=0.00,
        displayTime=0.00,
        relativeScreenPositionX=0.00,
        relativeScreenPositionY=0.00,
    )

    assert calibration_1 == calibration_2
    assert calibration_1 != calibration_3


@pytest.mark.parametrize(
    "input_kwargs,exception,exception_message",
    [
        ({}, TypeError, ".*missing 1 required positional argument.*"),
        (
            {"calibrations": ""},
            TypeError,
            "Expected a list for 'calibrations', got <class 'str'>",
        ),
        (
            {"calibrations": [{"digit_inputs": ""}]},
            TypeError,
            "Expected a list for 'digit_inputs', got <class 'str'>",
        ),
        (
            {"calibrations": [{"video": ""}]},
            TypeError,
            "Expected a dict for 'video', got <class 'str'>",
        ),
        (
            {"calibrations": [{"digit_inputs": []}]},
            DigitInputsEmptyError,
            "No digit input provided for the calibration in screenCalibration",
        ),
        (
            {
                "calibrations": [
                    {
                        "digit_inputs": [
                            {
                                "ts": 0.00,
                                "touchCount": 0,
                                "touches": [
                                    {
                                        "fingerId": 0,
                                        "relativePosition_x": 0.00,
                                        "relativePosition_y": 0.00,
                                        "phase": "Began",
                                    }
                                ],
                            }
                        ]
                    }
                ]
            },
            PointsEmptyError,
            "No points provided for the calibration in screenCalibration",
        ),
        (
            {
                "calibrations": [
                    {
                        "digit_inputs": [
                            {
                                "ts": 0.00,
                                "touchCount": 0,
                                "touches": [
                                    {
                                        "fingerId": 0,
                                        "relativePosition_x": 0.00,
                                        "relativePosition_y": 0.00,
                                        "phase": "Began",
                                    }
                                ],
                            }
                        ]
                    },
                    {
                        "name": "",
                        "bump_ts": 0.00,
                        "hit_ts": 0.00,
                        "displayTime": 0.00,
                        "relativeScreenPositionX": 0.00,
                        "relativeScreenPositionY": 0.00,
                    },
                ]
            },
            ValueError,
            "No video provided for the calibration in screenCalibration",
        ),
    ],
)
def test_exception_new_screen_calibration(input_kwargs, exception, exception_message):
    from src.okidia.pipelines.load_cmap_dataset.data_manipulation.game_session.screen_calibration import (
        ScreenCalibration,
    )

    with pytest.raises(exception, match=exception_message):
        ScreenCalibration(**input_kwargs)


def test_screen_calibration_eq():
    from src.okidia.pipelines.load_cmap_dataset.data_manipulation.game_session.screen_calibration import (
        ScreenCalibration,
    )

    # test if the screen calibration is equal to itself
    screen_calibration_1 = ScreenCalibration(
        calibrations=[
            {
                "digit_inputs": [
                    {
                        "ts": 0.00,
                        "touchCount": 0,
                        "touches": [
                            {
                                "fingerId": 0,
                                "relativePosition_x": 0.00,
                                "relativePosition_y": 0.00,
                                "phase": "Began",
                            }
                        ],
                    }
                ]
            },
            {
                "name": "",
                "bump_ts": 0.00,
                "hit_ts": 0.00,
                "displayTime": 0.00,
                "relativeScreenPositionX": 0.00,
                "relativeScreenPositionY": 0.00,
            },
            {"video": {"start_ts": 0.00, "stop_ts": 0.00, "path": ""}},
        ]
    )
    assert screen_calibration_1 == screen_calibration_1

    # test if the screen calibration is equal to a different screen calibration
    screen_calibration_2 = ScreenCalibration(
        calibrations=[
            {
                "digit_inputs": [
                    {
                        "ts": 0.00,
                        "touchCount": 0,
                        "touches": [
                            {
                                "fingerId": 0,
                                "relativePosition_x": 0.00,
                                "relativePosition_y": 0.00,
                                "phase": "Began",
                            }
                        ],
                    }
                ]
            },
            {
                "name": "",
                "bump_ts": 0.00,
                "hit_ts": 0.00,
                "displayTime": 0.00,
                "relativeScreenPositionX": 0.00,
                "relativeScreenPositionY": 0.00,
            },
            {"video": {"start_ts": 0.00, "stop_ts": 0.00, "path": ""}},
        ]
    )
    assert screen_calibration_1 == screen_calibration_2

    # test if the screen calibration is not equal to a different screen calibration
    screen_calibration_3 = ScreenCalibration(
        calibrations=[
            {
                "digit_inputs": [
                    {
                        "ts": 1.00,
                        "touchCount": 0,
                        "touches": [
                            {
                                "fingerId": 0,
                                "relativePosition_x": 0.00,
                                "relativePosition_y": 0.00,
                                "phase": "Began",
                            }
                        ],
                    }
                ]
            },
            {
                "name": "",
                "bump_ts": 0.00,
                "hit_ts": 0.00,
                "displayTime": 0.00,
                "relativeScreenPositionX": 0.00,
                "relativeScreenPositionY": 0.00,
            },
            {"video": {"start_ts": 0.00, "stop_ts": 0.00, "path": ""}},
        ]
    )
    assert screen_calibration_1 != screen_calibration_3
