import pytest

from src.okidia.pipelines.load_cmap_dataset.data_manipulation.exceptions import (
    ChallengeIsTrainingError,
    EventInputsEmptyError,
)


@pytest.mark.parametrize(
    "input_kwargs,exception,exception_message",
    [
        ({}, TypeError, ".*missing 5 required positional argument.*"),
        (
            {"start_ts": 0.00},
            TypeError,
            ".*missing 4 required positional argument.*",
        ),
        (
            {"start_ts": 0.00, "end_ts": 0.00},
            TypeError,
            ".*missing 3 required positional argument.*",
        ),
        (
            {"start_ts": 0.00, "end_ts": 0.00, "current_challenge": 0},
            TypeError,
            ".*missing 2 required positional argument.*",
        ),
        (
            {
                "start_ts": 0.00,
                "end_ts": 0.00,
                "current_challenge": 0,
                "training": True,
            },
            TypeError,
            ".*missing 1 required positional argument.*",
        ),
        (
            {
                "start_ts": 0.00,
                "end_ts": 0.00,
                "current_challenge": 0,
                "training": True,
                "events": [],
            },
            EventInputsEmptyError,
            "This challenge has no event inputs",
        ),
        (
            {
                "start_ts": 0,
                "end_ts": 0.00,
                "current_challenge": 0,
                "training": True,
                "events": [],
            },
            TypeError,
            "Expected a float for 'start_ts', got <class 'int'>",
        ),
        (
            {
                "start_ts": 0.00,
                "end_ts": 0,
                "current_challenge": 0,
                "training": True,
                "events": [],
            },
            TypeError,
            "Expected a float for 'end_ts', got <class 'int'>",
        ),
        (
            {
                "start_ts": 0.00,
                "end_ts": 0.00,
                "current_challenge": "",
                "training": True,
                "events": [],
            },
            TypeError,
            "Expected an int for 'current_challenge', got <class 'str'>",
        ),
        (
            {
                "start_ts": 0.00,
                "end_ts": 0.00,
                "current_challenge": 0,
                "training": 0,
                "events": [],
            },
            TypeError,
            "Expected a bool for 'training', got <class 'int'>",
        ),
        (
            {
                "start_ts": 0.00,
                "end_ts": 0.00,
                "current_challenge": 0,
                "training": True,
                "events": 0,
            },
            TypeError,
            "Expected a list for 'events', got <class 'int'>",
        ),
        (
            {
                "start_ts": 10.00,
                "end_ts": 0.00,
                "current_challenge": 0,
                "training": True,
                "events": [],
            },
            ValueError,
            "Expected 'start_ts' to be smaller than 'end_ts', got 10.0 > 0.0",
        ),
        (
            {
                "start_ts": 0.00,
                "end_ts": 0.00,
                "current_challenge": 2,
                "training": True,
                "events": [],
            },
            ChallengeIsTrainingError,
            "Challenge is training but current_challenge is 2",
        ),
    ],
)
def test_exception_new_challenge(input_kwargs, exception, exception_message):
    from src.okidia.pipelines.load_cmap_dataset.data_manipulation.game_session.challenge import (
        Challenge,
    )

    with pytest.raises(exception, match=exception_message):
        Challenge(**input_kwargs)


def test_challenge_eq():
    from src.okidia.pipelines.load_cmap_dataset.data_manipulation.game_session.challenge import (
        Challenge,
    )
    from src.okidia.pipelines.load_cmap_dataset.data_manipulation.game_session.event_input import (
        EventInput,
    )

    # test if the challenge is equal to itself
    challenge_1 = Challenge(
        start_ts=0.00,
        end_ts=0.00,
        current_challenge=0,
        training=True,
        events=[EventInput(ts=0.00, event_type="input", object_name="play")],
    )
    assert challenge_1 == challenge_1

    # test if the challenge is equal to another challenge with the same values
    challenge_2 = Challenge(
        start_ts=0.00,
        end_ts=0.00,
        current_challenge=0,
        training=True,
        events=[EventInput(ts=0.00, event_type="input", object_name="play")],
    )
    assert challenge_1 == challenge_2

    # test if the challenge is not equal to another challenge with different values
    challenge_3 = Challenge(
        start_ts=0.00,
        end_ts=0.00,
        current_challenge=1,
        training=False,
        events=[EventInput(ts=0.00, event_type="input", object_name="play")],
    )
    assert challenge_1 != challenge_3

    # test if the challenge is not equal to another challenge with different values
    challenge_4 = Challenge(
        start_ts=0.00,
        end_ts=0.00,
        current_challenge=0,
        training=True,
        events=[
            EventInput(ts=0.00, event_type="input", object_name="play"),
            EventInput(ts=0.00, event_type="input", object_name="play"),
        ],
    )
    assert challenge_1 != challenge_4
