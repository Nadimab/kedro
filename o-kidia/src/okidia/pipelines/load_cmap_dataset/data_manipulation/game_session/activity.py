from __future__ import annotations

from ..exceptions import ChallengesEmptyError, DigitInputsEmptyError
from .challenge import Challenge
from .digit_input import DigitInput
from .enums import ActivityEnum
from .video import Video


class Activity:
    """An activity (test) done by a user during a session with a start time, stop time and a list of challenges

    Attributes:
        game_name (str): The name of the game the user played (e.g. "Dj Crocos", "Crocos Factory", ...)
        start_ts (float): The timestamp of the start of the activity
        end_ts (float): The timestamp of the end of the activity
        digit_inputs (list): A list of all digit-tracking events during the activity
        challenges (list): A list of all challenges of the activity sorted by start_ts
        video (Video): The video of the activity


    Raises:
        TypeError: When either type for game_name, start_ts, end_ts, video, digit_inputs or challenges is not a string, float, dict or list
    """

    __slots__ = (
        "game_name",
        "start_ts",
        "end_ts",
        "digit_inputs",
        "challenges",
        "video",
    )

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        game_name: str,
        start_ts: float,
        end_ts: float,
        video: dict,
        digit_inputs: list,
        challenges: list,
    ):
        if not isinstance(game_name, str):
            raise TypeError(f"Expected a string for 'game_name', got {type(game_name)}")

        if not isinstance(start_ts, float):
            raise TypeError(f"Expected a float for 'start_ts', got {type(start_ts)}")

        if not isinstance(end_ts, float):
            raise TypeError(f"Expected a float for 'end_ts', got {type(end_ts)}")

        if not isinstance(digit_inputs, list):
            raise TypeError(
                f"Expected a list for 'digit_inputs', got {type(digit_inputs)}"
            )

        if not isinstance(challenges, list):
            raise TypeError(f"Expected a list for 'challenges', got {type(challenges)}")

        if not digit_inputs:
            raise DigitInputsEmptyError("No digit inputs provided for this activity")

        if not challenges:
            raise ChallengesEmptyError("No challenges provided for this activity")

        self.game_name = ActivityEnum(game_name)
        self.start_ts = start_ts
        self.end_ts = end_ts

        if not isinstance(digit_inputs[0], DigitInput):
            digit_inputs = list(
                map(lambda digit_input: DigitInput(**digit_input), digit_inputs)
            )
        self.digit_inputs: list[DigitInput] = sorted(
            digit_inputs, key=lambda digit_input: digit_input.ts
        )

        if not isinstance(challenges[0], Challenge):
            # if python 3.9 is used, this can be replaced with map(lambda challenge: Challenge(**challenge | **dict(activity=self)), challenges)
            challenges = list(
                map(
                    lambda challenge_input: Challenge.from_activity(
                        **{**challenge_input, **dict(activity=self)}
                    ),
                    challenges,
                )
            )
        self.challenges: list[Challenge] = sorted(
            challenges, key=lambda challenge: challenge.start_ts
        )

        self.video = Video(**video)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Activity):
            return False
        return (
            self.game_name == other.game_name
            and self.start_ts == other.start_ts
            and self.end_ts == other.end_ts
            and len(self.digit_inputs) == len(other.digit_inputs)
            and len(self.challenges) == len(other.challenges)
            and all(
                digit_input == other_digit_input
                for digit_input, other_digit_input in zip(
                    self.digit_inputs, other.digit_inputs
                )
            )
            and all(
                challenge == other_challenge
                for challenge, other_challenge in zip(self.challenges, other.challenges)
            )
            and self.video == other.video
        )

    def copy(self):
        """Generate a shallow copy of the activity."""
        activity = Activity(
            game_name=self.game_name.value,
            start_ts=self.start_ts,
            end_ts=self.end_ts,
            video=dict(
                start_ts=self.video.start_ts,
                stop_ts=self.video.stop_ts,
                path=self.video.path,
            ),
            digit_inputs=self.digit_inputs,
            challenges=self.challenges,
        )
        return activity

    def asdict(self):
        """Convert the Activity object to a dictionary

        Returns:
            dict: The dictionary representation of the Activity object
        """
        return {
            "game_name": self.game_name.value,
            "start_ts": self.start_ts,
            "end_ts": self.end_ts,
        }

    def get_digit_inputs(self, from_ts: float, to_ts: float) -> list[DigitInput]:
        """Get the digit inputs of the activity between the given timestamps

        Args:
            from_ts (float): The timestamp of the start of the range
            to_ts (float): The timestamp of the end of the range

        Returns:
            list: The digit inputs of the activity between the given timestamps
        """
        return [
            digit_input
            for digit_input in self.digit_inputs
            if from_ts <= digit_input.ts <= to_ts
        ]
