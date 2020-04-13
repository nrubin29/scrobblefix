# scrobblefix

Utilities to help you fill in the gaps when Last.fm's Spotify scrobbler fails.
Note that these utilities don't actually scrobble the tracks for you (yet).
You should use a service like my [simplescrobble](https://github.com/nrubin29/simplescrobble) to handle this.

## scrobblefix-api

Reads a JSON object returned by Spotify's [Recently Played Tracks endpoint](https://developer.spotify.com/console/get-recently-played).
Note that the endpoint only returns up to 50 tracks.
As per Spotify, "a track must be played for more than 30 seconds to be included in play history," so this works well with Last.fm's rules.

## spotifyfix-privacy

Reads a `StreamingHistory.json` file (from Spotify's [data request feature](https://www.spotify.com/is/account/privacy/)).
There are some variables that need to be configured before the script can work.
