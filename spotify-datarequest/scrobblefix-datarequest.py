import json
from collections import namedtuple
from datetime import datetime, timezone
from typing import List

from common import format_datetime

# BEGIN: Settings - times in EST/EDT

start = datetime(year=2020, month=4, day=7, hour=12, minute=2).astimezone()
end = datetime(year=2020, month=4, day=8, hour=0, minute=37).astimezone()
play_threshold = 30 * 1000  # 30 seconds

# END: Settings

Track = namedtuple('Track', ('end_time', 'artist_name', 'track_name', 'ms_played'))
count = 0

with open('StreamingHistory4.json', 'r') as f:
    data: List[Track] = json.load(f, object_hook=lambda obj: Track(
        end_time=datetime.fromisoformat(obj['endTime']).replace(tzinfo=timezone.utc).astimezone(),
        artist_name=obj['artistName'],
        track_name=obj['trackName'],
        ms_played=obj['msPlayed']
    ))

    for item in data:
        if item.ms_played >= play_threshold and start <= item.end_time <= end:
            print('{:35s}{:30s}{:s}'.format(format_datetime(item.end_time), item.artist_name, item.track_name))
            count += 1

    print('=' * 100)
    print(count, 'scrobbles')
