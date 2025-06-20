class ScreenCalibrationOrActivitiesEmptyError(Exception):
    """
    Raised when the activities or screen calibrations are not in a game session.
    """


class DigitInputsEmptyError(Exception):
    """
    Raised when the digit inputs are empty.
    """

    pass


class ChallengesEmptyError(Exception):
    """
    Raised when the challenges are empty.
    """

    pass


class PointsEmptyError(Exception):
    """
    Raised when the points in a calibration are empty.
    """


class ChallengeIsTrainingError(Exception):
    """
    Raised when the challenge is training and should not be.
    """

    pass


class EventInputsEmptyError(Exception):
    """
    Raised when the event inputs are empty.
    """

    pass


class TouchInputsEmptyError(Exception):
    """
    Raised when the touch inputs are empty.
    """

    pass
