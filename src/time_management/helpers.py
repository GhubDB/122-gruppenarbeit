from PyQt5.QtCore import QTime

from src.widgets.time_edit_row import TimeEditRow


def seconds_to_hhmmss(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    time_str = "{:02}:{:02}:{:02}".format(int(h), int(m), int(s))
    return time_str


def seconds_to_hhmm(seconds: int) -> str:
    seconds_in_a_day = 24 * 60 * 60
    seconds %= seconds_in_a_day
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    time_str = "{:02}:{:02}".format(int(h), int(m))
    return time_str


def convert_and_sort_qtime(rows: [TimeEditRow]) -> tuple[int, int]:
    zero_time = QTime(0, 0)
    row_tuples = (
        (
            zero_time.secsTo(row.from_time_edit.time()),
            zero_time.secsTo(row.to_time_edit.time()),
        )
        for row in rows
    )
    return sorted(row_tuples, key=lambda row: row[0])


def get_total_time_worked(sorted_rows: [[int, int]]) -> int:
    if len(sorted_rows) < 1:
        return 0

    minStart = sorted_rows[0][0]
    maxEnd = sorted_rows[0][0]
    gap = 0

    for i in range(len(sorted_rows)):
        #  If there is a gap, increment total gap length
        if sorted_rows[i][0] > maxEnd:
            gap = gap + sorted_rows[i][0] - maxEnd

        # Update latest end time
        if sorted_rows[i][1] > maxEnd:
            maxEnd = sorted_rows[i][1]

    return maxEnd - minStart - gap
