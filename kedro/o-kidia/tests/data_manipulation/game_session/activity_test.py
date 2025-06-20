import pytest

dummy_digit_inputs = {
    "ts": 0.0,
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
video_dummy = {"start_ts": 0.0, "stop_ts": 0.0, "path": ""}
challenges_dummy = [
    {
        "start_ts": 0.0,
        "end_ts": 0.0,
        "current_challenge": 0,
        "training": False,
        "events": [{"ts": 0.0, "event_type": "Common", "result_code": 1}],
    }
]


@pytest.mark.parametrize(
    "activity_kwargs,exception,exception_message",
    [
        ({}, TypeError, ".*missing 6 required positional arguments.*"),
        (
            {"game_name": "CrocosMaze"},
            TypeError,
            ".*missing 5 required positional arguments.*",
        ),
        (
            {
                "game_name": "CrocosMaze",
                "start_ts": 0.0,
                "end_ts": 0.0,
                "digit_inputs": "",
                "video": video_dummy,
                "challenges": challenges_dummy,
            },
            TypeError,
            "Expected a list for 'digit_inputs', got <class 'str'>",
        ),
        (
            {
                "game_name": "CrocosMaze",
                "start_ts": 0,
                "end_ts": 0.0,
                "digit_inputs": [dummy_digit_inputs],
                "video": video_dummy,
                "challenges": challenges_dummy,
            },
            TypeError,
            "Expected a float for 'start_ts', got <class 'int'>",
        ),
        (
            {
                "game_name": "ShouldNotExist",
                "start_ts": 0.0,
                "end_ts": 0.0,
                "digit_inputs": [dummy_digit_inputs],
                "video": video_dummy,
                "challenges": challenges_dummy,
            },
            ValueError,
            ".*'ShouldNotExist' is not a valid ActivityEnum.*",
        ),
        (
            {
                "game_name": "",
                "start_ts": 0.0,
                "end_ts": 0.0,
                "digit_inputs": [dummy_digit_inputs],
                "video": video_dummy,
                "challenges": challenges_dummy,
            },
            ValueError,
            ".*'' is not a valid ActivityEnum.*",
        ),
    ],
)
def test_exception_new_activity(
    activity_kwargs: dict, exception: Exception, exception_message: str
):
    from src.okidia.pipelines.load_cmap_dataset.data_manipulation.game_session.activity import (
        Activity,
    )

    with pytest.raises(exception, match=exception_message):
        Activity(**activity_kwargs)


def test_activity_shallow_copy():
    from src.okidia.pipelines.load_cmap_dataset.data_manipulation.game_session.activity import (
        Activity,
    )

    game_name = "CrocosMaze"
    start_ts = 0.0
    end_ts = 0.0
    activity = Activity(
        game_name=game_name,
        start_ts=start_ts,
        end_ts=end_ts,
        digit_inputs=[dummy_digit_inputs],
        challenges=challenges_dummy,
        video=video_dummy,
    )
    activity_copy = activity.copy()
    assert activity == activity_copy
