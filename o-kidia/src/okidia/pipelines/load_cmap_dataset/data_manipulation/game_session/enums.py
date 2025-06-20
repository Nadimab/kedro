from enum import Enum, IntEnum, auto


class ActivityEnum(Enum):
    """
    Enum for the different activities.
    """

    CROCOS_MAZE = "CrocosMaze"
    DJ_CROCOS = "DJCrocos"
    CROCOS_VOCABULO = "CrocosVocabulo"
    # Inconsistent naming: some activities are named "Crocos" and others are
    # named "Croco"
    CROCOS_FACTORY = "CrocoFactory"
    CROCOS_SPOT = "CrocoSpot"
    SCREEN_CALIBRATION = "ScreenCalib"
    MAIN_MENU = "MainMenu"


class PhaseEnum(IntEnum):
    """Enum for phase of the game
    @TODO: Need to add more phases and specify what they do
    Demo phase contains the instructions and the demo of the game
    because it's not possible to infer when the instructions ends.
    """

    DEMO = auto()
    TRAINING = auto()
    READING = auto()
    PLAYING = auto()


class EventTypeEnum(Enum):
    INPUT = "input"
    # Inconsistency: the first letter of the event type is capitalized
    COMMON = "Common"
