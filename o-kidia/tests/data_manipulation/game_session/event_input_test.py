import pytest


@pytest.mark.parametrize(
    "input_kwargs,exception,exception_message",
    [
        ({}, TypeError, ".*missing 2 required positional argument.*"),
        (
            {"ts": 0.00},
            TypeError,
            ".*missing 1 required positional argument.*",
        ),
        (
            {"ts": 0, "event_type": ""},
            TypeError,
            "Expected a float for 'ts', got <class 'int'>",
        ),
        (
            {"ts": 0.00, "event_type": 0},
            TypeError,
            "Expected a string for 'event_type', got <class 'int'>",
        ),
        (
            {"ts": 0.00, "event_type": "ShouldNotExist"},
            ValueError,
            ".*'ShouldNotExist' is not a valid EventTypeEnum.*",
        ),
        (
            {"ts": 0.00, "event_type": "input"},
            TypeError,
            "Expected an object name of type 'str' for an event_type 'input', got <class 'NoneType'>",
        ),
        (
            {"ts": 0.00, "event_type": "Common"},
            TypeError,
            "Expected a result code of type 'int' for the event_type 'Common', got <class 'NoneType'>",
        ),
    ],
)
def test_exception_new_event_input(input_kwargs, exception, exception_message):
    from src.okidia.pipelines.load_cmap_dataset.data_manipulation.game_session.event_input import (
        EventInput,
    )

    with pytest.raises(exception, match=exception_message):
        EventInput(**input_kwargs)


def test_event_input_eq():
    from src.okidia.pipelines.load_cmap_dataset.data_manipulation.game_session.event_input import (
        EventInput,
    )

    event_input_1 = EventInput(ts=0.00, event_type="input", object_name="play")
    event_input_2 = EventInput(ts=0.00, event_type="input", object_name="play")
    event_input_3 = EventInput(ts=0.00, event_type="Common", result_code=0)
    event_input_4 = EventInput(ts=0.00, event_type="Common", result_code=1)

    assert event_input_1 == event_input_2
    assert event_input_1 != event_input_3
    assert event_input_1 != event_input_4
