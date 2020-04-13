from datetime import datetime


def format_datetime(dt: datetime) -> str:
    """
    Formats a datetime to a human-readable format (which is used by simplescrobble and can be copy-pasted).
    """
    return '{}/{}/{}, {}:{:0>2} {}'.format(dt.month, dt.day, dt.year, dt.hour - 12 if dt.hour > 12 else dt.hour, dt.minute, 'AM' if dt.hour // 12 == 0 else 'PM')
