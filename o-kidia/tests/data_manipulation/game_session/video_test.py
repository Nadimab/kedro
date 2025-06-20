import pytest


@pytest.mark.parametrize(
    "input_kwargs,exception,exception_message",
    [
        ({}, TypeError, ".*missing 3 required positional argument.*"),
        (
            {"start_ts": 0.00},
            TypeError,
            ".*missing 2 required positional argument.*",
        ),
        (
            {"start_ts": 0.00, "stop_ts": 0.00},
            TypeError,
            ".*missing 1 required positional argument.*",
        ),
        (
            {"start_ts": 0, "stop_ts": 0.00, "path": ""},
            TypeError,
            "Expected a float for 'start_ts', got <class 'int'>",
        ),
        (
            {"start_ts": 0.00, "stop_ts": 0, "path": ""},
            TypeError,
            "Expected a float for 'stop_ts', got <class 'int'>",
        ),
        (
            {"start_ts": 0.00, "stop_ts": 0.00, "path": 0},
            TypeError,
            "Expected a string for 'path', got <class 'int'>",
        ),
        (
            {"start_ts": 10.00, "stop_ts": 0.00, "path": ""},
            ValueError,
            "Stop time must be greater than start time, got 0.0 - 10.0",
        ),
    ],
)
def test_exception_new_video(input_kwargs, exception, exception_message):
    from src.okidia.pipelines.load_cmap_dataset.data_manipulation.game_session.video import (
        Video,
    )

    with pytest.raises(exception, match=exception_message):
        Video(**input_kwargs)


def test_video_eq():
    from src.okidia.pipelines.load_cmap_dataset.data_manipulation.game_session.video import (
        Video,
    )

    video_1 = Video(start_ts=0.00, stop_ts=10.00, path="path")
    video_2 = Video(start_ts=0.00, stop_ts=10.00, path="path")
    video_3 = Video(start_ts=0.00, stop_ts=10.00, path="path2")

    assert video_1 == video_2
    assert video_1 != video_3
