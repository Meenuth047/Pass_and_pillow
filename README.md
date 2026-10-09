# Pass the Pillow

Pass the Pillow is a lightweight browser-based party game inspired by
pass-the-pillow and hot potato. Music plays while players pass an object
around. When the music stops, the person holding it is out, receives a
challenge, or takes the next turn according to the group's rules.

## Why I built it

The idea came from a gathering with friends. One day, some friends
visited and suggested playing pass the pillow. The usual approach was to
choose songs and manually start and pause them. That meant one person
controlled the timing, which could make the game unfair. I searched
online for a tool matching this use case but did not find one that
suited what I wanted, so I built a small app that stops music
automatically.

The first version was deliberately quick to build: users could upload a
local audio file or choose a preset track, select a random stop
interval, and start a round. The next improvement is to connect Spotify
so users can choose a playlist instead of preparing audio files
manually.

## Current version

-   Single-page interface using HTML, CSS, and vanilla JavaScript.
-   Local audio upload through the browser.
-   Preset tracks.
-   Random stop ranges: 10--20, 20--30, 30--40, and 40--60 seconds.
-   Automatic stopping and a manual stop control.
-   No backend or build system required for the local-file version.

## Planned Spotify improvements

-   Spotify authorization and playlist access.
-   Playlist dropdown and a preview of the selected playlist.
-   Random selection of an eligible track for each round.
-   Avoid the same track in consecutive rounds whenever at least two
    eligible tracks are available.
-   Automatic stopping after a randomly chosen interval.
-   Clear loading, authorization, empty-playlist, unavailable-track,
    device, and playback-error states.
-   Retain local-file playback as an optional fallback if useful.

Spotify playback is subject to account eligibility, API availability,
supported playback methods, and device requirements. The Spotify Web
Playback SDK requires Spotify Premium. The app must communicate
limitations clearly and must not claim playback succeeded when it did
not.

## How a round works

1.  Connect Spotify (planned).
2.  Load playlists the user is authorized to access.
3.  Select a playlist and a stop-time range.
4.  Start a round.
5.  Select a playable track, avoiding the immediately previous track
    when possible.
6.  Start playback and independently choose a random stop time.
7.  Stop playback when the timer expires and show a clear status
    message.
8.  Choose a different track for the next round whenever possible.

Timers must be cancelled when a round is stopped or restarted, when the
playlist changes, and when the relevant UI is torn down.

## Suggested architecture

-   **Interface:** connection status, playlist dropdown, playlist
    preview, duration selector, start/stop controls, and round status.
-   **Authorization:** OAuth 2.0 Authorization Code with PKCE for a
    browser-only public client. Never embed a client secret in browser
    code.
-   **Playlist service:** retrieves playlist and track metadata using
    only necessary permissions.
-   **Track selection:** filters unavailable entries and chooses a track
    without immediate repetition when possible.
-   **Playback service:** starts and stops playback through a supported
    Spotify mechanism and reports errors.
-   **Round controller:** owns timer state, selected duration, current
    track, and round lifecycle.

Keep the app lightweight. Do not add a framework, database, backend, or
build tool unless the selected Spotify flow or deployment requirements
genuinely need one.

## Requirements and limitations

-   Modern browser with JavaScript enabled.
-   Spotify account and authorization for the requested access.
-   Spotify developer application with the exact redirect URI
    configured.
-   Compatible Spotify playback method and device.
-   Internet access for Spotify features. Local-file playback can work
    offline if retained.
-   Check official Spotify documentation for current API rules and
    requirements.

Official references: - [Spotify
Authorization](https://developer.spotify.com/documentation/web-api/concepts/authorization) -
[Authorization Code with
PKCE](https://developer.spotify.com/documentation/web-api/tutorials/code-pkce-flow) -
[Spotify API
scopes](https://developer.spotify.com/documentation/web-api/concepts/scopes) -
[Spotify Web Playback
SDK](https://developer.spotify.com/documentation/web-playback-sdk)

## Security and privacy

-   Request only the scopes needed for playlist access and playback.
-   Never commit credentials or tokens to version control.
-   Never put a Spotify client secret in frontend JavaScript.
-   Validate OAuth `state` and implement PKCE correctly.
-   Handle token expiry and authorization cancellation without exposing
    credentials in logs.
-   Do not modify playlists or the user's library.

## Development principles

-   Keep the interface responsive and accessible.
-   Make playback state visible and unambiguous.
-   Generate a fresh random timer for every round.
-   Avoid immediate track repetition when possible, and handle playlists
    with one playable track.
-   Test authorization failures, empty playlists, unavailable tracks,
    playback errors, repeated start/stop actions, and timer cleanup.

## Project files

-   `main.html` --- original single-page interface and game logic.
-   `README.md` --- project background, architecture, and development
    notes.
-   `QUICK_START.md` --- concise setup and usage instructions.

## Project status

The local-file game is the starting point. Spotify connection, playlist
selection, and non-repeating track selection are planned improvements
and must not be described as implemented until built and tested.
