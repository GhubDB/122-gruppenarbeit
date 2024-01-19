import re

from src.time_management.helpers import seconds_to_hhmmss


def test_seconds_to_hhmmss_returns_correctly_formatted_string():
    seconds = 3665
    result = seconds_to_hhmmss(seconds)
    pattern = re.compile(r"^\d{2}:\d{2}:\d{2}$")
    assert pattern.match(result), f"Expected format HH:MM:SS, got: {result}"
