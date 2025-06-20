from __future__ import annotations

from ..exceptions import DigitInputsEmptyError, PointsEmptyError
from .digit_input import DigitInput
from .video import Video


class Calibration:
    """Point touched during a calibration phase

    Attributes:
        name (str): Name of the point touched
        bump_ts (float): Timestamp of the animation start for the target on this point
        hit_ts (float): Timestamp when the target is touched
        display_time (float): Time interval between the start of the animation and the target being touched
        relative_position_x (float): Relative x position of the target
        relative_position_y (float): Relative y position of the target

    Raises:
        TypeError: When either type for name, bump_ts, hit_ts, display_time, relative_position_x or relative_position_y is not a float or string
    """

    __slots__ = (
        "name",
        "bump_ts",
        "hit_ts",
        "display_time",
        "relative_screen_position_x",
        "relative_screen_position_y",
    )

    def __init__(
        self,
        name: str,
        bump_ts: float,
        hit_ts: float,
        displayTime: float,
        relativeScreenPositionX: float,
        relativeScreenPositionY: float,
    ):
        if not isinstance(name, str):
            raise TypeError(f"Expected a string for 'name', got {type(name)}")

        if not isinstance(bump_ts, float):
            raise TypeError(f"Expected a float for 'bump_ts', got {type(bump_ts)}")

        if not isinstance(hit_ts, float):
            raise TypeError(f"Expected a float for 'hit_ts', got {type(hit_ts)}")

        if not isinstance(displayTime, float):
            raise TypeError(
                f"Expected a float for 'displayTime', got {type(displayTime)}"
            )

        if not isinstance(relativeScreenPositionX, float):
            raise TypeError(
                f"Expected a float for 'relativeScreenPositionX', got {type(relativeScreenPositionX)}"
            )

        if not isinstance(relativeScreenPositionY, float):
            raise TypeError(
                f"Expected a float for 'relativeScreenPositionY', got {type(relativeScreenPositionY)}"
            )

        self.name = name
        self.bump_ts = bump_ts
        self.hit_ts = hit_ts
        self.display_time = displayTime
        self.relative_screen_position_x = relativeScreenPositionX
        self.relative_screen_position_y = relativeScreenPositionY

    def __eq__(self, other: object):
        if not isinstance(other, Calibration):
            return False
        return (
            self.name == other.name
            and self.bump_ts == other.bump_ts
            and self.hit_ts == other.hit_ts
            and self.display_time == other.display_time
            and self.relative_screen_position_x == other.relative_screen_position_x
            and self.relative_screen_position_y == other.relative_screen_position_y
        )


class ScreenCalibration:
    """Metadata pertaining to the calibration phase of a session

    Attributes:
        points (list): List of Calibration objects
        digit_inputs (list): List of DigitInput objects
        video (Video): Video metadata

    Raises:
        TypeError: When either type for points, digit_inputs or video is not a list or dict
    """

    __slots__ = ("points", "digit_inputs", "video")

    def __init__(self, calibrations: list):
        self.points: list[Calibration] = []
        self.digit_inputs: list[DigitInput] = []
        self.video = None
        if not isinstance(calibrations, list):
            raise TypeError(
                f"Expected a list for 'calibrations', got {type(calibrations)}"
            )
        for item in calibrations:
            # Sometime comments can be found inside the screen calibration json list
            if isinstance(item, str):
                continue
            if "digit_inputs" in item:
                if not isinstance(item["digit_inputs"], list):
                    raise TypeError(
                        f"Expected a list for 'digit_inputs', got {type(item['digit_inputs'])}"
                    )
                self.digit_inputs.extend(
                    sorted(
                        map(
                            lambda digit_input: DigitInput(**digit_input),
                            item["digit_inputs"],
                        ),
                        key=lambda digit_input: digit_input.ts,
                    )
                )
            elif "video" in item:
                if not isinstance(item["video"], dict):
                    raise TypeError(
                        f"Expected a dict for 'video', got {type(item['video'])}"
                    )
                self.video = Video(**item["video"])
            else:
                self.points.append(Calibration(**item))

        if not self.digit_inputs:
            raise DigitInputsEmptyError(
                "No digit input provided for the calibration in screenCalibration"
            )
        if not self.points:
            raise PointsEmptyError(
                "No points provided for the calibration in screenCalibration"
            )
        if not self.video:
            raise ValueError(
                "No video provided for the calibration in screenCalibration"
            )

    def __eq__(self, other: object):
        if not isinstance(other, ScreenCalibration):
            return False
        return (
            self.points == other.points
            and self.video == other.video
            and len(self.digit_inputs) == len(other.digit_inputs)
            and all(
                [
                    digit_input == other_digit_input
                    for digit_input, other_digit_input in zip(
                        self.digit_inputs, other.digit_inputs
                    )
                ]
            )
        )
