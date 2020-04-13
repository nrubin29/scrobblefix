import json
from collections import namedtuple
from datetime import timezone
from typing import List

from dateutil import parser

from common import format_datetime

Track = namedtuple('Track', ('played_at', 'artist_name', 'track_name'))


def hook(obj: dict):
    if 'played_at' in obj:
        # This is a Track object.
        return Track(
            played_at=parser.parse(obj['played_at']).replace(tzinfo=timezone.utc).astimezone(),
            artist_name=obj['track']['artists'][0]['name'],
            track_name=obj['track']['name'],
        )

    else:
        return obj


with open('data.json', 'r') as f:
    data: List[Track] = json.load(f, object_hook=hook)['items']
    data.sort(key=lambda track: track.played_at)

    for item in data:
        print('{:35s}{:30s}{:s}'.format(format_datetime(item.played_at), item.artist_name, item.track_name))

    print('=' * 100)
    print(len(data), 'scrobbles')
