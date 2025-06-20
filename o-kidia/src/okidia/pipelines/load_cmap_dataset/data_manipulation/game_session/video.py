from __future__ import annotations


class Video:
    """Video metadata for an activity or a whole session with a start time,
    stop time and path to the video file

    Attributes:
        start_ts (float): Start time of the video in seconds
        stop_ts (float): Stop time of the video in seconds
        path (str): Path to the video file

    Raises:
        TypeError: When either type for start_ts, stop_ts or path is not a
         float, string or int
        ValueError: When the start_ts is greater than the stop_ts
    """

    __slots__ = ("start_ts", "stop_ts", "path")

    def __init__(self, start_ts: float, stop_ts: float, path: str):
        if not isinstance(start_ts, float):
            raise TypeError(f"Expected a float for 'start_ts', got {type(start_ts)}")

        if not isinstance(stop_ts, float):
            raise TypeError(f"Expected a float for 'stop_ts', got {type(stop_ts)}")

        if not isinstance(path, str):
            raise TypeError(f"Expected a string for 'path', got {type(path)}")

        if (stop_ts - start_ts) < 0:
            raise ValueError(
                f"Stop time must be greater than start time, got {stop_ts} - "
                f"{start_ts}"
            )

        self.start_ts = start_ts
        self.stop_ts = stop_ts
        self.path = path

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Video):
            return False
        return (
            self.start_ts == other.start_ts
            and self.stop_ts == other.stop_ts
            and self.path == other.path
        )
