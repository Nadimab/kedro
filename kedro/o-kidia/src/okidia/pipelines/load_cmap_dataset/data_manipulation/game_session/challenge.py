from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

import numpy as np
from tslearn.metrics import dtw_path

from ..exceptions import ChallengeIsTrainingError, EventInputsEmptyError
from .enums import ActivityEnum
from .event_input import EventInput

if TYPE_CHECKING:
    from .activity import Activity


class Challenge:
    """A challenge of an activity (can be a level of an activity) with a
    start time, stop time and a list of events

    Attributes:
        start_ts (float): The start time of the level
        end_ts (float): The end time of the level
        current_challenge (int): The index of the current level
        training (bool): Whether the level is a training level or not
        events (list): A list of all events in the challenge (when a child
         touch outside an object, no log is created) sorted by timestamp

    Raises:
        TypeError: When either type for start_ts, stop_ts, current_challenge,
         training or events is not a float, string, int or bool
    """

    __slots__ = (
        "start_ts",
        "end_ts",
        "current_challenge",
        "training",
        "events",
        "activity",
        "state",
    )

    def __init__(
        self,
        start_ts: float,
        end_ts: float,
        current_challenge: int,
        training: bool,
        events: list,
        activity: Activity = None,
        state: list = [],
    ):
        if not isinstance(start_ts, float):
            raise TypeError(f"Expected a float for 'start_ts', got {type(start_ts)}")

        if not isinstance(end_ts, float):
            raise TypeError(f"Expected a float for 'end_ts', got {type(end_ts)}")

        if not isinstance(current_challenge, int):
            raise TypeError(
                f"Expected an int for 'current_challenge', got {type(current_challenge)}"
            )

        if not isinstance(training, bool):
            raise TypeError(f"Expected a bool for 'training', got {type(training)}")

        if not isinstance(events, list):
            raise TypeError(f"Expected a list for 'events', got {type(events)}")

        if start_ts > end_ts:
            raise ValueError(
                f"Expected 'start_ts' to be smaller than 'end_ts', got {start_ts} > {end_ts}"
            )
        # The first challenge is always a training challenge
        if current_challenge > 0 and training:
            raise ChallengeIsTrainingError(
                f"Challenge is training but current_challenge is {current_challenge}"
            )

        if not events:
            raise EventInputsEmptyError(f"This challenge has no event inputs")

        self.start_ts = start_ts
        self.end_ts = end_ts
        self.current_challenge = current_challenge
        self.training = training

        if not isinstance(events[0], EventInput):
            events = list(map(lambda e: EventInput(**e), events))

        # All events have now a timestamp so we can sort them
        self.events: list[EventInput] = sorted(
            events,
            key=lambda e: e.ts,
        )
        self.state: list[dict] = state
        # TODO: Remove this when the activity is not needed anymore
        self.activity = activity

    @staticmethod
    def from_activity(
        start_ts: float,
        end_ts: float,
        current_challenge: int,
        training: bool,
        events: list,
        activity: Activity,
    ):
        if activity.game_name is ActivityEnum.CROCOS_MAZE:
            return CrocosMazeChallenge(
                start_ts, end_ts, current_challenge, training, events, activity
            )
        elif activity.game_name is ActivityEnum.DJ_CROCOS:
            return DJCrocosChallenge(
                start_ts, end_ts, current_challenge, training, events, activity
            )
        elif activity.game_name is ActivityEnum.CROCOS_FACTORY:
            return CrocosFactoryChallenge(
                start_ts, end_ts, current_challenge, training, events, activity
            )
        elif activity.game_name is ActivityEnum.CROCOS_SPOT:
            return CrocosSpotChallenge(
                start_ts, end_ts, current_challenge, training, events, activity
            )
        elif activity.game_name is ActivityEnum.CROCOS_VOCABULO:
            return CrocosVocabuloChallenge(
                start_ts, end_ts, current_challenge, training, events, activity
            )
        return Challenge(
            start_ts,
            end_ts,
            current_challenge,
            training,
            events,
            activity,
        )

    @staticmethod
    def compute_activity_score(scores: list[list[int | float]]) -> float:
        """Compute the score of the activity from the scores of the challenges

        Args:
            scores (list[list[int]]): The scores of the challenges

        Returns:
            float: The score of the activity
        """
        return 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Challenge):
            return False
        return (
            self.start_ts == other.start_ts
            and self.end_ts == other.end_ts
            and self.current_challenge == other.current_challenge
            and self.training == other.training
            and len(self.events) == len(other.events)
            and all(
                event == other_event
                for event, other_event in zip(self.events, other.events)
            )
        )

    @property
    def sorted_events(self) -> list[EventInput]:
        return sorted(self.events, key=lambda e: e.ts)

    def score(self) -> list[int | float]:
        """The score of the challenge, by default counts the completed challenges

        Returns:
            int: The score of the challenge
        """
        events_end = sum(map(lambda e: e.result_code == 303, self.sorted_events))
        timeout_events = sum(map(lambda e: e.result_code == 200, self.sorted_events))
        return [events_end - timeout_events]


class CrocosMazeChallenge(Challenge):
    def __init__(
        self,
        start_ts: float,
        end_ts: float,
        current_challenge: int,
        training: bool,
        events: list,
        activity: Activity,
    ):
        filtered_events: list = []
        state: list = []
        for event in events:
            (filtered_events if "ts" in event else state).append(event)
        events = filtered_events

        super().__init__(
            start_ts,
            end_ts,
            current_challenge,
            training,
            events,
            activity,
            state,
        )

    def constant_elapsed_time(self, point: int) -> float:
        """The expected time elapsed to reach the given point. The time is
        computed arbitrarily from a simple formula sqrt(x) and makes it
        slowly increase the time to reach the point. In fact, the more
        points there are, the more time it takes to reach the point but also
        the shorter is the distance between two points.

        Returns:
            float: The constant speed of the challenge
        """
        return np.sqrt(point)

    def curve_points(self) -> Iterator[tuple[float, float, float]]:
        """The curve points of the challenge

        Returns:
            Iterator[Tuple[float, float, float]]: The curve points of the
            challenge
        """
        yield (
            float(self.state[0].get("relativeScreenPositionX")),
            float(self.state[0].get("relativeScreenPositionY")),
            0.0,
        )
        for i, point in enumerate(self.state):
            point_name: str = point.get("name", "")
            if not point_name.startswith("Start"):
                yield (
                    float(point.get("relativeScreenPositionX")),
                    float(point.get("relativeScreenPositionY")),
                    self.constant_elapsed_time(i + 1),
                )

    def digit_curve(self) -> Iterator[tuple[float, float, float]]:
        """The digit points related to the curve points of the challenge

        Returns:
            Iterator[Tuple[float, float]]: The digit points related to the
             curve points of the challenge
        """
        start_ts: float | None = None
        end_ts: float | None = None
        for event in self.sorted_events:
            if event.object_name == "Cursor":
                start_ts = event.ts
            elif event.result_code == 303:
                end_ts = event.ts
                break
        if start_ts is None or end_ts is None:
            return None

        if self.activity:
            for digit_input in self.activity.get_digit_inputs(start_ts, end_ts):
                yield (
                    digit_input.touches[0].relative_position_x,
                    digit_input.touches[0].relative_position_y,
                    digit_input.ts - start_ts,
                )

    @staticmethod
    def compute_activity_score(scores: list[list[int | float]]) -> float:
        """Compute the score of the activity from the scores of the challenges

        Args:
            scores (list[list[int | float]]): The scores of the challenges

        Returns:
            float: The score of the activity
        """
        return sum(score[0] for score in scores)

    def score(self) -> list[int | float]:
        """The score of the challenge, by default counts the completed
         challenges

        Returns:
            int: The score of the challenge
        """
        _, score = dtw_path(
            np.asarray([(point[0], point[1]) for point in self.digit_curve()]),
            np.asarray([(point[0], point[1]) for point in self.curve_points()]),
        )
        return [score, score]


class DJCrocosChallenge(Challenge):
    # Maximum continuous number of notes that can be played in a challenge
    max_continuous_notes = 3 + 5 + 7 + 9
    # Four tries to complete the challenge
    nb_games = 4

    @staticmethod
    def compute_activity_score(scores: list[list[int | float]]) -> float:
        """Compute the score of the activity from the scores of the challenges

        Args:
            scores (list[list[int]]): The scores of the challenges

        Returns:
            float: The score of the activity
        """
        return sum(map(lambda s: s[0], scores))

    def score(self) -> tuple[float, float, float]:
        """The score of the challenge

        Returns:
            Tuple[int]: The score of the challenge, followed by the score components
        """
        has_failed = False
        # A success is acounted for when the player didn't fail and the player didn't timeout
        success = 0
        current_try = -1
        continuous = [0 for _ in range(self.nb_games)]
        for e in self.sorted_events:
            if e.result_code == 302:
                has_failed = False
                current_try += 1
            elif e.result_code == 101:
                has_failed = True
            elif e.result_code == 303 and not has_failed:
                success += 1
            elif e.result_code in [1, 2, 3]:
                if not has_failed:
                    continuous[current_try] += 1
        max_continuous = sum(continuous)
        score = (success / self.nb_games) + (max_continuous / self.max_continuous_notes)
        return (
            score,
            success / self.nb_games,
            max_continuous / self.max_continuous_notes,
        )


class CrocosFactoryChallenge(Challenge):
    # Number of experiments to complete the challenge
    nb_games = 3

    @staticmethod
    def compute_activity_score(scores: list[list[int | float]]) -> float:
        """Compute the score of the activity from the scores of the challenges

        Args:
            scores (list[list[int]]): The scores of the challenges

        Returns:
            float: The score of the activity
        """
        success = sum(map(lambda s: s[1], scores))
        nb_games = CrocosFactoryChallenge.nb_games * 8
        return success / nb_games

    def score(self) -> tuple[float, int]:
        """The score of the challenge

        Returns:
            Tuple[int]: The score of the challenge, followed by the score components
        """
        success = 0
        for e in self.sorted_events:
            if e.result_code in [1, 2, 3]:
                success += 1

        return success / CrocosFactoryChallenge.nb_games, success


class CrocosSpotChallenge(Challenge):
    # Number of pairs to select per challenge
    nb_games = 12

    @staticmethod
    def compute_activity_score(scores: list[list[int | float]]) -> float:
        """Compute the score of the activity from the scores of the challenges

        Args:
            scores (list[list[int]]): The scores of the challenges

        Returns:
            float: The score of the activity
        """
        return max(0, sum(map(lambda s: s[1], scores))) / (
            CrocosSpotChallenge.nb_games * 3
        )

    def score(self) -> tuple[float, int]:
        """The score of the challenge

        Returns:
            Tuple[int]: The score of the challenge, followed by the score components
        """
        right_answer = set()
        wrong_answer = set()
        for e in self.sorted_events:
            if e.result_code in [1, 2, 3, 102, 103, 104, 105]:
                if e.result_code in [1, 2, 3]:
                    right_answer.add(e.object_name)
                else:
                    wrong_answer.add(e.object_name)
            elif e.result_code in [4, 101]:
                if e.result_code == 4:
                    wrong_answer.remove(e.object_name)
                elif e.result_code == 101:
                    right_answer.remove(e.object_name)
        score = (
            max(0, (len(right_answer) - len(wrong_answer)))
            / CrocosSpotChallenge.nb_games
        )
        return score, len(right_answer) - len(wrong_answer)


class CrocosVocabuloChallenge(Challenge):
    # Number words/images to guess during the game
    nb_games = 28

    @staticmethod
    def compute_activity_score(scores: list[list[int | float]]) -> float:
        """Compute the score of the activity from the scores of the challenges

        Args:
            scores (list[list[int]]): The scores of the challenges

        Returns:
            float: The score of the activity
        """
        return max(0, sum(map(lambda s: s[1], scores))) / (
            CrocosVocabuloChallenge.nb_games
        )

    def score(self) -> tuple[int, int]:
        """The score of the challenge

        Returns:
            Tuple[int]: The score of the challenge, followed by the score components
        """
        right_answer = set()
        wrong_answer = set()
        for e in self.sorted_events:
            if e.result_code in [1, 2, 101, 102]:
                if e.result_code in [1, 101]:
                    right_answer.add(e.object_name)
                else:
                    wrong_answer.add(e.object_name)
            elif e.result_code in [3, 4, 103, 104]:
                if e.result_code in [3, 103]:
                    right_answer.remove(e.object_name)
                else:
                    wrong_answer.remove(e.object_name)
        score = max(0, (len(right_answer) - len(wrong_answer)))
        return score, len(right_answer) - len(wrong_answer)
