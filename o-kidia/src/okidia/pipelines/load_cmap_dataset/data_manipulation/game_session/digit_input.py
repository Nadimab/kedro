from __future__ import annotations

from ..exceptions import TouchInputsEmptyError


class TouchInput:
    """Metadata for a touch event during an activity with the finger used,
    x and y coordinates and a phase

    Attributes:
        finger_id (int): The id of the finger used
        relative_position_x (float): The relative x coordinate of the touch
         event
        relative_position_y (float): The relative y coordinate of the touch
         event
        phase (str): The phase of the touch event, can be 'Began', 'Held' or
         'Ended'

    Raises:
        TypeError: When either type for finger, x, y or phase is not a float
         or string
    """

    __slots__ = (
        "finger_id",
        "relative_position_x",
        "relative_position_y",
        "phase",
    )

    def __init__(
        self,
        fingerId: int,
        relativePosition_x: float,
        relativePosition_y: float,
        phase: str,
    ):
        if not isinstance(fingerId, int):
            raise TypeError(f"Expected an int for 'fingerId', got {type(fingerId)}")

        if not isinstance(relativePosition_x, float):
            raise TypeError(
                f"Expected a float for 'relativePosition_x', got {type(relativePosition_x)}"
            )

        if not isinstance(relativePosition_y, float):
            raise TypeError(
                f"Expected a float for 'relativePosition_y', got {type(relativePosition_y)}"
            )

        if not isinstance(phase, str):
            raise TypeError(f"Expected a string for 'phase', got {type(phase)}")

        self.finger_id = fingerId
        self.relative_position_x = relativePosition_x
        self.relative_position_y = relativePosition_y
        self.phase = phase

    def __eq__(self, other: object) -> bool:
        if isinstance(other, TouchInput):
            return (
                self.finger_id == other.finger_id
                and self.relative_position_x == other.relative_position_x
                and self.relative_position_y == other.relative_position_y
                and self.phase == other.phase
            )
        return False


class DigitInput:
    """Metadata pertaining to all Digit-Tracking events during an activity

    Attributes:
        ts (float): The timestamp of the Digit-Tracking event
        touch_count (int): The number of touches detected during the event
        touches (list): A list of all touch inputs data retrieved during the event

    Raises:
        TypeError: When either type for ts, touchCount or touches is not a float, int or list
    """

    __slots__ = ("ts", "touch_count", "touches")

    def __init__(self, ts: float, touchCount: int, touches: list):
        if not isinstance(ts, float):
            raise TypeError(f"Expected a float for 'ts', got {type(ts)}")

        if not isinstance(touchCount, int):
            raise TypeError(f"Expected an int for 'touchCount', got {type(touchCount)}")

        if not isinstance(touches, list):
            raise TypeError(f"Expected a list for 'touches', got {type(touches)}")

        if not touches:
            raise TouchInputsEmptyError("The list of touches cannot be empty")

        self.ts = ts
        self.touch_count = touchCount

        self.touches = touches
        if not isinstance(self.touches[0], TouchInput):
            self.touches = list(map(lambda x: TouchInput(**x), touches))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DigitInput):
            return False
        return (
            self.ts == other.ts
            and self.touch_count == other.touch_count
            and all(
                [
                    touch == other_touch
                    for touch, other_touch in zip(self.touches, other.touches)
                ]
            )
        )

    # Because of the way we only want the first touch, we cannot use
    # dataclasses
    def asdict(self):
        """Convert the DigitInput object to a dictionary

        Returns:
            dict: The dictionary representation of the DigitInput object
        """
        return {
            "ts": self.ts,
            "touch_count": self.touch_count,
            # "x": [touch.relative_position_x for touch in self.touches],
            # "y": [touch.relative_position_y for touch in self.touches],
            "x": self.touches[0].relative_position_x,
            "y": self.touches[0].relative_position_y,
            "finger_id": self.touches[0].finger_id,
            "phase": self.touches[0].phase,
        }
