# Pass the Pillow: Quick Start

This guide covers the current local-file version. Spotify instructions
apply after Spotify integration has been implemented.

## Play the current version

1.  Open `main.html` in a modern browser.
2.  Choose **Upload Music** and select an audio file, or select a preset
    track if available.
3.  Choose a random stop-time range.
4.  Click **Start Game**.
5.  Pass the pillow while the music plays.
6.  When the music stops, follow the rules your group agreed on.
7.  Start another round when everyone is ready.

For a fair game, let the automatic timer decide when to stop. Use manual
stop only when you need to end a round early.

## Play with Spotify (planned)

Once Spotify support is implemented:

1.  Click **Connect Spotify**.
2.  Sign in and approve the requested permissions.
3.  Wait for playlists to load.
4.  Select a playlist and check its preview.
5.  Choose a stop-time range.
6.  Click **Start Game**.
7.  Pass the pillow until playback stops.
8.  Start another round. The app should choose a different eligible
    track when at least two are available.

## Developer setup for Spotify

1.  Create an app in the [Spotify Developer
    Dashboard](https://developer.spotify.com/dashboard).
2.  Configure the exact redirect URI used by the app.
3.  Add the client ID using the configuration method documented by the
    implementation.
4.  Use OAuth 2.0 Authorization Code with PKCE for a browser-only
    client. Never expose a client secret in frontend code.
5.  Request only the scopes needed by the selected playlist and playback
    features.
6.  Test sign-in, playlist loading, device selection, playback, token
    expiry, and authorization cancellation.

Spotify playback has account, device, API, and policy requirements. The
Web Playback SDK requires Spotify Premium. Check the current official
documentation: -
[Authorization](https://developer.spotify.com/documentation/web-api/concepts/authorization) -
[PKCE
flow](https://developer.spotify.com/documentation/web-api/tutorials/code-pkce-flow) -
[API
scopes](https://developer.spotify.com/documentation/web-api/concepts/scopes) -
[Web Playback
SDK](https://developer.spotify.com/documentation/web-playback-sdk)

## Troubleshooting

-   **No music starts:** verify a source or playlist is selected and the
    playback device can play audio.
-   **Spotify will not connect:** check the client ID, redirect URI,
    network, and permissions.
-   **No playlists appear:** verify playlist permissions and check that
    the account has playlists accessible to the app.
-   **No playback device is available:** open Spotify on a supported
    device and activate it if required by the implementation.
-   **A track cannot play:** the app should try another eligible track
    with a bounded retry count.
-   **A track repeats:** consecutive repetition should be avoided when
    at least two eligible tracks are available. A one-track playlist
    cannot meet that rule.

## Fair-play note

The stop time is selected randomly from the configured range. Agree on
the group's rules before starting so everyone knows what happens when
the music stops.
