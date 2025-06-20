from __future__ import annotations

from .enums import EventTypeEnum


class EventInput:
    """Input event metadata with a timestamp and event_type. An event type
    can be 'input' or 'common', when it is 'input' there is an object name
    but no result code, when it is 'common' there is a result code and no
    object name.

    Attributes:
        event_type (EventTypeEnum): The type of event, can be 'input' or
         'common'
        ts (float): The timestamp of the event
        object_name (str): The name of the object that was interacted with
        result_code (int): The result code of the event
        args (dict): The arguments specific to the event

    Raises:
        TypeError: When either type for ts or event_type is not a float or
         string
        ValueError: When the event_type is not one of the accepted values
        ValueError: When the result_code is not an integer
    """

    __slots__ = ("event_type", "ts", "result_code", "object_name", "args")

    # pylint: disable=too-many-branches, too-few-public-methods
    # EventInput is used as a storage/validation class, hence the
    # few-public-methods pylint warning & the too-many-branches one cause by
    # the following method.
    def __init__(
        self,
        event_type: str,
        ts: float,
        result_code: int | None = None,
        object_name: str | None = None,
        **kwargs,
    ):
        if not isinstance(event_type, str):
            raise TypeError(
                f"Expected a string for 'event_type', got {type(event_type)}"
            )

        if not isinstance(ts, float):
            raise TypeError(f"Expected a float for 'ts', got {type(ts)}")

        self.event_type = EventTypeEnum(event_type)
        self.ts = ts
        self.object_name = None
        self.result_code = None

        if self.event_type is EventTypeEnum.INPUT:
            if result_code is not None and isinstance(result_code, int):
                self.result_code = result_code
            if object_name is not None and isinstance(object_name, str):
                self.object_name = object_name
            else:
                raise TypeError(
                    f"Expected an object name of type 'str' for an event_type "
                    f"'input', got {type(object_name)}"
                )
        elif self.event_type is EventTypeEnum.COMMON:
            if result_code is not None and isinstance(result_code, int):
                self.result_code = result_code
            else:
                raise TypeError(
                    f"Expected a result code of type 'int' for the event_type "
                    f"'{event_type}', got {type(result_code)}"
                )
        self.args = kwargs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EventInput):
            return False
        return (
            self.event_type == other.event_type
            and self.ts == other.ts
            and self.result_code == other.result_code
            and self.object_name == other.object_name
            and self.args == other.args
        )
