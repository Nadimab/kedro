import pytest

from src.okidia.pipelines.load_cmap_dataset.data_manipulation.exceptions import (
    TouchInputsEmptyError,
)


@pytest.mark.parametrize(
    "input_kwargs,exception,exception_message",
    [
        ({}, TypeError, ".*missing 3 required positional argument.*"),
        (
            {"ts": 0.00},
            TypeError,
            ".*missing 2 required positional argument.*",
        ),
        (
            {"ts": 0.00, "touchCount": 0},
            TypeError,
            ".*missing 1 required positional argument.*",
        ),
        (
            {"ts": 0.00, "touchCount": 0, "touches": []},
            TouchInputsEmptyError,
            "The list of touches cannot be empty",
        ),
        (
            {"ts": 0, "touchCount": 0, "touches": []},
            TypeError,
            "Expected a float for 'ts', got <class 'int'>",
        ),
        (
            {"ts": 0.00, "touchCount": "", "touches": []},
            TypeError,
            "Expected an int for 'touchCount', got <class 'str'>",
        ),
        (
            {"ts": 0.00, "touchCount": 0, "touches": ""},
            TypeError,
            "Expected a list for 'touches', got <class 'str'>",
        ),
    ],
)
def test_exception_new_digit_input(input_kwargs, exception, exception_message):
    from src.okidia.pipelines.load_cmap_dataset.data_manipulation.game_session.digit_input import (
        DigitInput,
    )

    with pytest.raises(exception, match=exception_message):
        DigitInput(**input_kwargs)


def test_digit_input_eq():
    from src.okidia.pipelines.load_cmap_dataset.data_manipulation.game_session.digit_input import (
        DigitInput,
        TouchInput,
    )

    touch_1 = TouchInput(
        fingerId=0,
        relativePosition_x=0.00,
        relativePosition_y=0.00,
        phase="Began",
    )
    touch_2 = TouchInput(
        fingerId=0,
        relativePosition_x=0.00,
        relativePosition_y=0.00,
        phase="Began",
    )
    touch_3 = TouchInput(
        fingerId=0,
        relativePosition_x=0.00,
        relativePosition_y=0.00,
        phase="Moved",
    )
    touch_4 = TouchInput(
        fingerId=0,
        relativePosition_x=0.00,
        relativePosition_y=0.00,
        phase="Ended",
    )
    touch_5 = TouchInput(
        fingerId=0,
        relativePosition_x=0.00,
        relativePosition_y=0.00,
        phase="Cancelled",
    )

    input_1 = DigitInput(ts=0.0, touchCount=0, touches=[touch_1])
    input_2 = DigitInput(ts=0.0, touchCount=0, touches=[touch_2])
    input_3 = DigitInput(ts=0.0, touchCount=0, touches=[touch_3])
    input_4 = DigitInput(ts=0.0, touchCount=0, touches=[touch_4])
    input_5 = DigitInput(ts=0.0, touchCount=0, touches=[touch_5])

    assert input_1 == input_2
    assert input_1 != input_3
    assert input_1 != input_4
    assert input_1 != input_5
