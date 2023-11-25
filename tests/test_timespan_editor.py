from src.time_management.helpers import get_total_time_worked


def test_get_total_time_worked_worked_empty_input():
    assert get_total_time_worked([]) == 0


def test_get_total_time_worked_worked_single_timespan():
    input_data = [[800, 900]]
    assert get_total_time_worked(input_data) == 100


def test_get_total_time_worked_worked_non_overlapping_timespans():
    input_data = [
        [800, 900],
        [1000, 1100],
        [1300, 1400],
    ]
    assert get_total_time_worked(input_data) == 300


def test_get_total_time_worked_worked_overlapping_timespans():
    input_data = [
        [800, 900],
        [830, 1000],
        [930, 1100],
    ]
    assert get_total_time_worked(input_data) == 300


def test_get_total_time_worked_worked_multiple_gaps():
    input_data = [
        [800, 900],
        [1000, 1100],
        [1300, 1400],
        [1500, 1600],
    ]
    assert get_total_time_worked(input_data) == 400
