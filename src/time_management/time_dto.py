from dataclasses import dataclass


@dataclass
class TimeDTO:
    total_time_worked: int
    latest_time_worked: int
    seconds_remaining: int
