import base64
import json
import webbrowser
from collections import namedtuple
from datetime import timezone
from typing import List, Dict
from urllib.parse import urlunsplit, urlencode, urlparse, parse_qs

from dateutil import parser
from requests import post, get

from common import format_datetime
from env import spotify_client_id, spotify_client_secret
from webserver_thread import WebserverThread

Track = namedtuple('Track', ('played_at', 'artist_name', 'track_name'))


def _hook(obj: dict):
    if 'played_at' in obj:
        # This is a Track object.
        return Track(
            played_at=parser.parse(obj['played_at']).replace(tzinfo=timezone.utc).astimezone(),
            artist_name=obj['track']['artists'][0]['name'],
            track_name=obj['track']['name'],
        )

    else:
        return obj


def _build_spotify_uri(host: str, path: str, query_params: Dict[str, object] = None):
    return urlunsplit(
        ('https', host, path, urlencode(query_params or {}), ''))


if __name__ == '__main__':
    thread = WebserverThread()
    thread.start()

    webbrowser.open(_build_spotify_uri('accounts.spotify.com', 'authorize',
                                       {'response_type': 'code', 'client_id': spotify_client_id,
                                        'redirect_uri': 'http://localhost:8080', 'scope': 'user-read-recently-played'}))

    result = thread.join()
    # noinspection PyTypeChecker
    code = parse_qs(urlparse(result).query)['code'][0]

    auth_header = base64.b64encode(bytes(f'{spotify_client_id}:{spotify_client_secret}', 'utf-8')).decode('utf-8')
    response = post(
        _build_spotify_uri('accounts.spotify.com', 'api/token', {'grant_type': 'authorization_code', 'code': code,
                                                                 'redirect_uri': 'http://localhost:8080'}), headers={
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/x-www-form-urlencoded'})
    access_token = json.loads(response.text)['access_token']

    recent_tracks = get(_build_spotify_uri('api.spotify.com', 'v1/me/player/recently-played', {'limit': 50}),
                        headers={'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}).text
    data: List[Track] = json.loads(recent_tracks, object_hook=_hook)['items']
    data.sort(key=lambda track: track.played_at)

    for item in data:
        print('{:35s}{:30s}{:s}'.format(format_datetime(item.played_at), item.artist_name, item.track_name))

    print('=' * 100)
    print(len(data), 'scrobbles')
