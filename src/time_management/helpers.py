from datetime import datetime, timedelta


def seconds_to_hhmmss(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    time_str = "{:02}:{:02}:{:02}".format(int(h), int(m), int(s))
    return time_str


def get_target_hour(seconds_remaining):
    current_time = datetime.now()
    if 0 > seconds_remaining:
        target_time = current_time - timedelta(seconds=seconds_remaining)
    else:
        target_time = current_time + timedelta(seconds=seconds_remaining)
    target_time_str = target_time.strftime("%H:%M")
    return "To: " + target_time_str
