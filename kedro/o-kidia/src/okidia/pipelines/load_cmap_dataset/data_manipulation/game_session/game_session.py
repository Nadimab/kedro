from __future__ import annotations

from argparse import ArgumentParser
from functools import reduce
from json import load, loads
from pathlib import Path
from typing import Tuple

import pandas as pd

from ..exceptions import ScreenCalibrationOrActivitiesEmptyError
from .activity import Activity
from .enums import ActivityEnum, PhaseEnum
from .event_input import EventInput
from .screen_calibration import ScreenCalibration


class Resolution:
    """Screen resolution for the device in the form of 'width x height @ refresh_rate'

    Attributes:
        width (int): Width of the screen in pixels
        height (int): Height of the screen in pixels
        refresh_rate (int): Refresh rate of the screen in Hz

    Raises:
        TypeError: When the resolution provided is not a string
        ValueError: When the width or the height are not integers
        ValueError: When the refresh rate is not an integer
    """

    __slots__ = ("width", "height", "refresh_rate")

    def __init__(self, resolution: str):
        if not isinstance(resolution, str):
            raise TypeError("Resolution must be a string")

        screen, rate = resolution.split("@")

        if rate is None:
            raise ValueError(
                f"Resolution must be in the form of 'width x height @ refresh_rate', got '{resolution}'"
            )

        refresh_rate: str = rate.strip().replace("Hz", "")

        if refresh_rate.isnumeric():
            self.refresh_rate = int(refresh_rate)
        else:
            raise ValueError(
                f"Cannot convert refresh rate, expected an integer, received {type(refresh_rate)}: '{refresh_rate}'"
            )

        width, height = screen.strip().split("x")
        width, height = width.strip(), height.strip()

        if width.isnumeric():
            self.width = int(width)
        else:
            raise ValueError(
                f"Cannot convert width, expected an integer, received {type(width)}: '{width}'"
            )

        if height.isnumeric():
            self.height = int(height)
        else:
            raise ValueError(
                f"Cannot convert height, expected an integer, received {type(height)}: '{height}'"
            )

    def to_str(self) -> str:
        """Returns the resolution in the form of 'width x height @ refresh_rate'

        Returns:
            str: The resolution in the form of 'width x height @ refresh_rate'
        """
        return f"{self.width} x {self.height} @ {self.refresh_rate}Hz"

    def __str__(self) -> str:
        return self.to_str()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Resolution):
            return False
        return (
            self.width == other.width
            and self.height == other.height
            and self.refresh_rate == other.refresh_rate
        )


class GameSession:
    """An object representation for a whole game session of a user

    Attributes:
        student_id (str): Student ID of the user
        device_name (str): Name of the device used for the session
        device_type (str): Type of the device used for the session
        device_model (str): Model of the device used for the session
        device_uuid (str): UUID of the device used for the session
        soft_version (int): Version of the software used for the session composed of the branch name and the software version number
        soft_configuration_name (str): Name of the configuration used for the session, usually linked to the current POC (e.g. C-Eye, C-Diag, etc.)
        resolution (Resolution): Resolution of the device used for the session
        screen_calibration (ScreenCalibration | None): Screen calibration metadata
        activities (dict[Activity]): List of Activity objects
        copying (bool): True if the user is copying the game, False otherwise. Allows to ignore the validation of the game session

    Raises:
        TypeError: When either type for student_id, device_name, device_type, device_model, soft_configuration_name or resolution is not a string
        TypeError: When either type for soft_version is not an int
        TypeError: When either type for screenCalibration or activities is not a list
    """

    __slots__ = (
        "student_id",
        "device_name",
        "device_type",
        "device_model",
        "device_uid",
        "soft_version",
        "soft_configuration_name",
        "resolution",
        "screen_calibration",
        "activities",
    )

    def __init__(
        self,
        student_id: str,
        device_name: str,
        device_type: str,
        device_model: str,
        device_uid: str,
        soft_version: int,
        soft_configuration_name: str,
        resolution: str,
        screenCalibration: list | None = None,
        activities: list | dict | None = None,
        copying: bool = False,
    ):
        if not copying:
            self.valid_session(
                student_id,
                device_name,
                device_type,
                device_model,
                device_uid,
                soft_version,
                soft_configuration_name,
                resolution,
                screenCalibration,
                activities,
            )

        self.device_name = device_name
        self.device_type = device_type
        self.device_model = device_model
        self.device_uid = device_uid
        self.soft_version = soft_version
        self.soft_configuration_name = soft_configuration_name
        self.student_id = student_id
        # Transform the resolution string into a Resolution object
        self.resolution = Resolution(resolution)

        # When we copy a game session, we don't pass the screen calibration
        # and activities (shallow)
        if not copying and screenCalibration is not None:
            self.screen_calibration = ScreenCalibration(screenCalibration)
        else:
            self.screen_calibration = None

        if not copying and activities is not None:
            # An activity inside a json could be a list of activities or a
            # single activity
            if isinstance(activities, list):
                self.activities = {
                    activity.game_name: activity
                    for activity in map(
                        lambda activity: Activity(**activity), activities
                    )
                }
            else:
                activity = Activity(**activities)
                self.activities = {activity.game_name: activity}
        else:
            self.activities = {}

    @staticmethod
    def valid_session(
        student_id,
        device_name,
        device_type,
        device_model,
        device_uid,
        soft_version,
        soft_configuration_name,
        resolution,
        screenCalibration,
        activities,
    ):
        if not isinstance(student_id, str):
            raise TypeError(
                f"Expected a string for 'student_id', got {type(student_id)}"
            )

        if not isinstance(device_name, str):
            raise TypeError(
                f"Expected a string for 'device_name', got {type(device_name)}"
            )

        if not isinstance(device_type, str):
            raise TypeError(
                f"Expected a string for 'device_type', got {type(device_type)}"
            )

        if not isinstance(device_model, str):
            raise TypeError(
                f"Expected a string for 'device_model', got {type(device_model)}"
            )

        if not isinstance(device_uid, str):
            raise TypeError(
                f"Expected a string for 'device_uid', got {type(device_uid)}"
            )

        if not isinstance(soft_version, int):
            raise TypeError(
                f"Expected a int for 'soft_version', got {type(soft_version)}"
            )

        if not isinstance(soft_configuration_name, str):
            raise TypeError(
                f"Expected a string for 'soft_configuration_name', got {type(soft_configuration_name)}"
            )

        if not isinstance(resolution, str):
            raise TypeError(
                f"Expected a string for 'resolution', got {type(resolution)}"
            )

        if screenCalibration is not None and not isinstance(screenCalibration, list):
            raise TypeError(
                f"Expected a list for 'screenCalibration', got {type(screenCalibration)}"
            )

        if activities is not None and not isinstance(activities, list):
            raise TypeError(f"Expected a list for 'activities', got {type(activities)}")

        if not screenCalibration and not activities:
            raise ScreenCalibrationOrActivitiesEmptyError(
                "No activities and screen calibration in this game session"
            )

    @staticmethod
    def from_json(path: str | Path) -> GameSession:
        with open(path) as f:
            data = load(f)
        return GameSession(**data)

    @staticmethod
    def from_raw(content) -> GameSession:
        data = loads(content)
        return GameSession(**data)

    @staticmethod
    def from_files(paths) -> GameSession:
        return reduce(
            lambda a, b: a | b if a is not None else b,
            map(GameSession.from_json, paths),
        )

    @staticmethod
    def from_dict(content: dict) -> GameSession:
        return GameSession(**content)

    def get_activity(
        self,
        game_name: ActivityEnum,
        digit_inputs: bool = True,
        video: bool = True,
    ) -> Activity:
        """Retrieve an activity by name from the session

        Args:
            game_name (ActivityEnum): The name of the game to retrieve
            digit_inputs (bool, optional): If True returns the activity with the digit tracking data. Defaults to True.
            video (bool, optional): If True returns the activity with the video metadata. Defaults to True.

        Returns:
            Activity: Returns a reference to the activity when digit_inputs and video are both True, else returns a shallow copy.
        """
        activity = self.activities.get(game_name, None)
        if activity is None:
            return None
        if not digit_inputs or not video:
            activity = activity.copy()
            if not digit_inputs:
                activity.digit_inputs = []
            if not video:
                activity.video = None
        return activity

    @property
    def sorted_activities(self) -> list[Activity]:
        """Returns a list of activities sorted by start time

        Returns:
            list: List of activities sorted by start time
        """
        return sorted(self.activities.values(), key=lambda activity: activity.start_ts)

    def copy(self) -> GameSession:
        """Returns a shallow copy of the object"""
        game_session = GameSession(
            self.student_id,
            self.device_name,
            self.device_type,
            self.device_model,
            self.device_uid,
            self.soft_version,
            self.soft_configuration_name,
            self.resolution.to_str(),
            [],
            copying=True,
        )
        game_session.screen_calibration = self.screen_calibration
        game_session.activities = self.activities
        return game_session

    def __or__(self, other: GameSession) -> GameSession:
        """Merges two game sessions together

        Args:
            other (GameSession): The other game session to merge with

        Raises:
            TypeError: When a game session is not passed in
            ValueError: When the student_id of the two game sessions do not match

        Returns:
            GameSession: A new game session with the merged data, activities and screen calibration are a shallow copy of the original
        """
        if not isinstance(other, GameSession):
            raise TypeError(f"Expected a GameSession object, got {type(other)}")
        if self.student_id != other.student_id:
            raise ValueError(
                f"Cannot merge two game session with different student_id, '{self.student_id}' != '{other.student_id}'"
            )
        game_session = self.copy()
        if game_session.screen_calibration is None:
            game_session.screen_calibration = other.screen_calibration
        game_session.activities = {**self.activities, **other.activities}
        return game_session

    def __eq__(self, other: object) -> bool:
        """Checks if two game sessions are equal

        Args:
            other (GameSession): The other game session to compare with

        Returns:
            bool: True if the two game sessions are equal, False otherwise
        """
        if not isinstance(other, GameSession):
            return False
        return (
            self.student_id == other.student_id
            and self.device_name == other.device_name
            and self.device_type == other.device_type
            and self.device_model == other.device_model
            and self.device_uid == other.device_uid
            and self.soft_version == other.soft_version
            and self.soft_configuration_name == other.soft_configuration_name
            and self.resolution == other.resolution
            and self.screen_calibration == other.screen_calibration
            and self.activities == other.activities
        )

    def _activities_dataframe(self):
        """Returns a pandas dataframe of the activities

        Returns:
            pd.DataFrame: A pandas dataframe of the activities
        """
        return pd.DataFrame([activity.asdict() for activity in self.sorted_activities])

    def _digit_inputs_dataframe(self):
        """Returns a pandas dataframe of the digit inputs

        Returns:
            pd.DataFrame: A pandas dataframe of the digit inputs
        """
        digit_inputs = [
            digit_input.asdict() for digit_input in self.screen_calibration.digit_inputs
        ]
        digit_inputs += [
            digit_input.asdict()
            for activity in self.sorted_activities
            for digit_input in activity.digit_inputs
        ]
        return pd.DataFrame(digit_inputs)

    def _phases_dataframe(self):
        """Returns a pandas dataframe of the phases for each activity

        Returns:
            pd.DataFrame: A pandas dataframe of the phases
        """
        # We initialize the phases with screen calibration
        phases = [
            {
                "activity": "ScreenCalib",
                "challenge": None,
                "phase": None,
                # We use the first digit input of the screen calibration as the start_ts of the phase
                "start_ts": self.screen_calibration.digit_inputs[0].ts,
                # We use the first digit input of the first activity as the end_ts of the phase
                "end_ts": self.sorted_activities[0].digit_inputs[0].ts,
            }
        ]
        # the last event emitted during an activity
        last_end_event: EventInput = None
        for activity in self.sorted_activities:
            # Before each activity, there is a main menu phase when the user select an activity to play
            phases.append(
                {
                    "activity": "MainMenu",
                    "challenge": None,
                    "phase": None,
                    # the start of the main menu is either the last event emitted during the last activity
                    # or the start of the first digit input of the activity
                    "start_ts": last_end_event.ts
                    if last_end_event
                    else activity.digit_inputs[0].ts,
                    # the main menu ends when the user select an activity to play (when the activity starts)
                    "end_ts": activity.start_ts,
                }
            )
            # the last event emitted during a challenge
            last_challenge_end_event: EventInput = None
            for challenge in activity.challenges:
                # We need to retrieve the common events starting and ending the challenge
                # Since it's a list of events, we can loop once and search for them
                start_event = None
                last_error_code = None
                for event in challenge.sorted_events:
                    if event.result_code == 302:
                        start_event = event
                        phases.append(
                            {
                                "activity": activity.game_name.value,
                                "challenge": challenge.current_challenge,
                                "phase": PhaseEnum.DEMO
                                if challenge.training
                                else PhaseEnum.READING,
                                # the start of the demo or reading phase is the end of the last event for this challenge or the start of the activity
                                "start_ts": last_challenge_end_event.ts
                                if last_challenge_end_event
                                else activity.start_ts,
                                # the phase ends when the challenge starts (when the start event is emitted)
                                "end_ts": start_event.ts,
                            }
                        )
                    elif event.result_code in [200, 303,] and last_error_code not in [
                        200,
                        303,
                    ]:
                        last_challenge_end_event = event
                        phases.append(
                            {
                                "activity": activity.game_name.value,
                                "challenge": challenge.current_challenge,
                                "phase": PhaseEnum.TRAINING
                                if challenge.training
                                else PhaseEnum.PLAYING,
                                # The start of the training or playing phase is the start of the challenge (when the start event is emitted)
                                "start_ts": start_event.ts,
                                # The phase ends when the challenge ends (when the end event is emitted)
                                "end_ts": last_challenge_end_event.ts,
                            }
                        )
                    if event.result_code in [200, 302, 303]:
                        last_error_code = event.result_code
                # Usually, there should be a start and end event for each challenge, but just in case,  we check if we have found both events
                if start_event is None or last_challenge_end_event is None:
                    raise ValueError(
                        f"Missing start or end event for challenge {challenge.current_challenge} in activity {activity.game_name.value}"
                    )
            # the last event emitted during an activity is the last challenge end event
            last_end_event = last_challenge_end_event
        return pd.DataFrame(phases)

    def to_dataframe(self):
        """Returns a pandas dataframe of the game session"""
        # We retrieve the dataframes for the different phases of the game session and the digit inputs
        df_phases = self._phases_dataframe()
        df_digits = self._digit_inputs_dataframe()
        # We build an interval index between the start and end timestamps of each phase [start_ts, end_ts)
        idx_phases = pd.IntervalIndex.from_arrays(
            df_phases["start_ts"], df_phases["end_ts"], closed="left"
        )
        # We build a dataframe with the activity, challenge and phase for each digit input according to the interval index
        df_acp = (
            df_phases.loc[
                idx_phases.get_indexer(df_digits["ts"]),
                ["activity", "challenge", "phase"],
            ]
            .copy()
            .reset_index(drop=True)
        )
        # We merge the digit inputs with their activity, challenge and phase
        df_digits.rename(columns={"phase": "phase_digit"}, inplace=True)
        return pd.concat([df_digits, df_acp], axis=1)

    def to_csv(self, filename: str):
        """Writes the game session to a CSV file

        Args:
            filename (str): The name of the file to write to
        """
        self.to_dataframe().to_csv(filename, index=False)

    def response_times(self) -> pd.DataFrame:
        """Returns a pandas dataframe of the response times for each activity

        Returns:
            pd.DataFrame: A pandas dataframe of the response times
        """
        df_phases = self._phases_dataframe()
        df_phases = (
            df_phases[df_phases["phase"].isin([PhaseEnum.TRAINING, PhaseEnum.PLAYING])]
            .copy()
            .reset_index(drop=True)
        )
        df_phases["response_time"] = df_phases["end_ts"] - df_phases["start_ts"]
        return df_phases

    def score(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Returns a pandas dataframe of the score for each activity

        Returns:
            Tuple[pd.DataFrame]: Two pandas dataframe, one for the scores for each activity and one for the scores for each challenge.
        """
        challenges_scores = []
        activities_scores = []
        for activity in self.sorted_activities:
            activity_scores = []
            challenge_type = None
            for challenge in activity.challenges:
                if challenge.training:
                    continue
                if challenge_type is None:
                    challenge_type = type(challenge)
                challenge_scores = challenge.score()
                challenges_scores.append(
                    {
                        "activity": activity.game_name.value,
                        "challenge": challenge.current_challenge,
                        "score": challenge_scores[0],
                    }
                )
                activity_scores.append(challenge_scores)
            activities_scores.append(
                {
                    "activity": activity.game_name.value,
                    "score": challenge_type.compute_activity_score(activity_scores),
                }
            )

        return pd.DataFrame.from_records(activities_scores), pd.DataFrame.from_records(
            challenges_scores
        )


def time_csv(game_session_file: (str | list[str]), output_file: str = None, **kwargs):
    """Function that takes a game session file and outputs a CSV file with the time analysis of each phases

    Args:
        game_session_file (str): The name of the file containing the game session
        output_file (str): The name of the file to write the output to
    """
    try:
        if isinstance(game_session_file, str):
            game_session_file = [game_session_file]
        game_session = GameSession.from_files(game_session_file)
    except Exception as e:
        print(f"Error: {e}")
        return
    else:
        print(f"Game session loaded from {game_session_file} successfully !")
        print(f"Number of activities: {len(game_session.activities)}")
        print("No errors found while parsing the game session.")
    if output_file is not None:
        game_session.to_csv(output_file)
        print("Game session saved to " + output_file)


def score_csv(
    game_session_file: (str | list[str]),
    output_file: str = None,
    only_activities: bool = True,
    **kwargs,
):
    """Function that takes a game session file and outputs a CSV file with the score analysis of each Activities and Challenges

    Args:
        game_session_file (str): The name of the file containing the game session
        output_file (str): The name of the file to write the output to
        only_activities (bool): If True, only the score for each activity is computed. If False, the score for each activity and challenge is computed.
    """
    try:
        if isinstance(game_session_file, str):
            game_session_file = [game_session_file]
        game_session = GameSession.from_files(game_session_file)
    except Exception as e:
        print(f"Error: {e}")
        return
    else:
        print(f"Game session loaded from {game_session_file} successfully !")
        print(f"Number of activities: {len(game_session.activities)}")
        print("No errors found while parsing the game session.")
    if output_file is not None:
        activity_scores, challenge_scores = game_session.score()
        if only_activities:
            activity_scores.to_csv(output_file, index=False)
            print("Activity scores saved to " + output_file)
        else:
            activity_scores.to_csv(output_file + "_activities.csv", index=False)
            challenge_scores.to_csv(output_file + "_challenges.csv", index=False)
            print("Activity and challenge scores saved to " + output_file)


def game_session_parser(parser: ArgumentParser) -> ArgumentParser:
    """Adds the game session arguments to the parser

    Args:
        parser (ArgumentParser): The parser to add the arguments to

    Returns:
        ArgumentParser: The parser with the added arguments
    """
    subparsers = parser.add_subparsers(help="Game Session subcommands")
    time_parser = subparsers.add_parser("time", help="Time analysis")
    time_parser.add_argument(
        "--game-session-file",
        "-f",
        help="The file to read the game session from",
        type=str,
        required=True,
        action="extend",
        nargs="+",
    )
    time_parser.add_argument(
        "--output-file",
        "-o",
        help="The outpule csv file to save the game session",
        type=str,
    )
    score_parser = subparsers.add_parser("score", help="Score analysis")
    score_parser.add_argument(
        "--game-session-file",
        "-f",
        help="The file to read the game session from",
        type=str,
        required=True,
        action="extend",
        nargs="+",
    )
    score_parser.add_argument(
        "--only-activities",
        help="Only output the scores for the activities",
        action="store_true",
    )
    score_parser.add_argument(
        "--output-file",
        "-o",
        help="The outpule csv file to save the game session",
        type=str,
    )
    time_parser.set_defaults(func=time_csv)
    score_parser.set_defaults(func=score_csv)
    return parser


if __name__ == "__main__":
    parser = ArgumentParser(description="Game session parser")
    game_session_parser(parser)
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(**vars(args))
    else:
        parser.print_help()
