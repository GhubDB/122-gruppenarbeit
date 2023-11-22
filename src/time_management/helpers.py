from datetime import timedelta


def seconds_to_hhmmss(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    time_str = "{:02}:{:02}:{:02}".format(int(h), int(m), int(s))
    return time_str


def seconds_to_hhmm(seconds):
    seconds_in_a_day = 24 * 60 * 60
    seconds %= seconds_in_a_day
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    time_str = "{:02}:{:02}".format(int(h), int(m))
    return time_str
