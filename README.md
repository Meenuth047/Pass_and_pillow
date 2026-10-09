# Pass the Pillow

Live Website: https://pass-and-pillow.onrender.com

For a quick 1-minute guide to start playing, see [QUICK_START.md](QUICK_START.md).
For detailed deployment and local server instructions, see [Installation.md](Installation.md).

Pass the Pillow is an automated, web-based party game application designed to eliminate bias and keep classic party games fair and unpredictable.

## Origin Story

The project originated during a gathering with friends and family. A group decided to play the classic party game "Pass the Pillow", but the traditional setup required a designated person to manually play and pause music. This created an unavoidable fairness issue: the person controlling the music could anticipate or observe who held the pillow and deliberately choose when to pause, influencing the outcome of the round. 

Searching online for an automated tool revealed plenty of generic countdown timers, but none tailored specifically to this use case--namely, an app that plays real music from a playlist at random and halts abruptly at an unpredictable moment without human intervention. This project was built to solve that problem, giving every player, including the host, an equal opportunity to participate.

## How the Game Works

1. Players sit in a circle and designate a pillow (or ball, toy, or other object) to pass.
2. The game host connects a music source (Spotify playlist, local audio file, or preset samples).
3. The host chooses a randomized duration range (10-20 seconds, 20-30 seconds, 30-40 seconds, or 40-60 seconds).
4. When the host presses "Start Game", an eligible track is selected at random and begins playing.
5. Players pass the pillow in a circle.
6. The timer stops the music automatically at a random instant within the selected range, displaying the prompt: "Music stopped. Who has the pillow?"
7. The player caught holding the pillow is eliminated or receives a round penalty, according to house rules.

## Feature Matrix

### Implemented Features

- Spotify OAuth 2.0 PKCE Authorization: Secure, browser-only public client flow without client secrets. Includes CSRF state validation, callback handling, token storage, automatic token refreshing, and complete session disconnect.
- User Playlists Retrieval: Full playlist loading with API pagination, cover art, and total track counts.
- Playlist Preview: Live inspection of the selected playlist including cover image, title, total tracks, eligible playable tracks count, and scrollable track list with title and artist information.
- Intelligent Random Track Selection:
  - Selects uniformly from eligible, playable, non-local tracks.
  - Guaranteed non-repetition across consecutive rounds when two or more eligible tracks exist.
  - Session history tracking that prioritizes unplayed tracks during the active session.
  - Graceful single-track handling: Permits repetition with explanatory UI notice if a playlist has only one playable track.
  - Graceful zero-track handling: Warns user and prevents game start if a playlist is empty.
  - Bounded retry: Retries up to 3 alternative tracks if a selected track fails playback due to API or network errors.
  - Automatic session history reset when changing playlists or clicking Reset History.
- Spotify Playback Methods:
  - Spotify Web Playback SDK: In-browser streaming player for supported desktop browsers.
  - Spotify Connect Web API: Device discovery and remote playback control for open Spotify apps (desktop, mobile, smart speakers).
- Configurable Randomized Stop Intervals: Four duration ranges (10-20s, 20-30s, 30-40s, 40-60s), with endpoints inclusive.
- Precise Playback Verification: Timers trigger only after audio playback is confirmed active.
- Automated Stop and Emergency Manual Stop: Halts audio and clears all timeouts cleanly.
- Race Condition and Stale Timer Guards: Disables start button during initialization, clears timers on playlist switch, mode change, stop, and session disconnect.
- Truthful State Display: Visual states for disconnected, loading, ready, starting, playing, stopped, and error.
- Offline and Local Audio Fallback: Retains local file upload (MP3, WAV, OGG) and preset sample audio streams for offline play or accounts without Spotify Premium.

### Planned Features

- Multiplayer scorekeeping and player elimination brackets.
- Sound effects for countdowns and buzzer tones.
- Custom stop duration range sliders.
- Collaborative playlist voting and party room sharing via WebRTC.

## Architecture and Technology Choices

The application is structured as a client-side Single-Page Application (SPA) contained within `main.html`:

- Vanilla HTML5, CSS3, and JavaScript: Eliminates complex build tools, external runtime dependencies, bundlers, and backend servers.
- Web Crypto API: Provides cryptographically secure random values and SHA-256 digest calculation for PKCE code verifiers and code challenges (`crypto.getRandomValues`, `crypto.subtle.digest`).
- Spotify Web API: Communicates via HTTP requests (`fetch`) for user profile, playlist retrieval, device enumeration, and playback control (`/v1/me/player/play`, `/v1/me/player/pause`).
- Spotify Web Playback SDK (`https://sdk.scdn.co/spotify-player.js`): Creates a local browser playback device for desktop environments.
- HTML5 Audio API: Powers the offline fallback player via `URL.createObjectURL(file)` and native `<audio>` element controls.

## Spotify Integration and Setup

### Spotify Developer Dashboard Configuration

To connect Spotify, you must register a free application in the Spotify Developer Dashboard:

1. Log in to the Spotify Developer Dashboard at https://developer.spotify.com/dashboard.
2. Click "Create App".
3. Provide an App name (for example, "Pass the Pillow") and App description.
4. Set the Redirect URI to the exact address where the app is hosted.
   - For local development: `http://127.0.0.1:8000/main.html` or `http://localhost:8000/main.html`.
5. Select the "Web API" and "Web Playback SDK" checkboxes under Which APIs are you planning to use.
6. Accept the Developer Terms of Service and save the app.
7. Copy your Client ID from the app overview page.

### Connecting in Pass the Pillow

1. Open `main.html` in your web browser.
2. In the Spotify tab, paste your Client ID into the input field.
3. Click "Connect with Spotify".
4. Authorize the requested permissions on the Spotify login screen.
5. You will be redirected back to the application with an authorization code, which is exchanged for an access token automatically.

### Account and Device Limitations

- Spotify Premium Requirement: Spotify API playback control (`/v1/me/player/play`, `/v1/me/player/pause`) and the Spotify Web Playback SDK strictly require a Spotify Premium subscription. Free Spotify accounts will receive a 403 Forbidden ("Premium required") error from Spotify API. This is an official restriction enforced by Spotify.
- Mobile Web Browser Playback: The Spotify Web Playback SDK relies on Encrypted Media Extensions (EME), which are not supported in mobile web browsers (such as Safari on iOS or Chrome on Android). To play on a mobile device, launch the official Spotify mobile app on your phone, open Pass the Pillow in your mobile browser, and select your phone as the playback device from the device dropdown.
- Public Client Scopes: The application requests minimal required scopes:
  - `streaming`
  - `user-read-email`
  - `user-read-private`
  - `playlist-read-private`
  - `playlist-read-collaborative`
  - `user-modify-playback-state`
  - `user-read-playback-state`

## Security and Privacy

- No Client Secret: In accordance with OAuth 2.0 PKCE standards for public browser clients, no client secret is used, stored, or committed.
- State Validation: An unpredictable cryptographic state parameter is generated per authorization request and verified upon callback to prevent CSRF attacks.
- Client-Side Token Storage: Tokens are saved strictly in your browser local storage. They are never sent to any third-party server.
- One-Click Disconnect: Clicking "Disconnect" purges all access tokens, refresh tokens, and session identifiers from storage and disconnects the player instance.

## Development and Testing Guidance

### Live Deployment on Render (Mobile and Web)

For public access on mobile phones or other devices without running a local server:

1. Log in to the Render Dashboard at https://dashboard.render.com.
2. Click "New +" and select "Static Site".
3. Connect your repository.
4. Set Publish Directory to `.` and leave Build Command blank.
5. Click "Create Static Site".
6. Copy your live Render URL (for example: `https://your-service-name.onrender.com`).
7. In the Spotify Developer Dashboard (https://developer.spotify.com/dashboard), add your live Render URL to your app Redirect URIs:
   - `https://your-service-name.onrender.com/`
   - `https://your-service-name.onrender.com/index.html`

A `render.yaml` configuration file is included in the repository for automated Render Blueprint deployment.

### Local Development (Optional)

To run the application locally using Python standard library:

```bash
# Navigate to the project directory
cd /path/to/Pass_and_pillow

# Start a local HTTP server
python3 -m http.server 8000

# Open in your browser:
# http://127.0.0.1:8000/
```

### Running Test Verification

The repository includes an automated verification test suite:

```bash
python3 test_suite.py
```

This tests HTML structure, UI elements, PKCE generation, track selection algorithms, timer math, consecutive non-repetition guarantees, single-track fallbacks, retry limits, and documentation formatting.

## Official Spotify Documentation References

- Spotify Authorization Code Flow with PKCE:
  https://developer.spotify.com/documentation/web-api/tutorials/code-pkce-flow
- Spotify Web Playback SDK Quick Start:
  https://developer.spotify.com/documentation/web-playback-sdk
- Spotify Web API Reference (Player):
  https://developer.spotify.com/documentation/web-api/reference/play-a-users-playback
- Spotify Web API Reference (Playlists):
  https://developer.spotify.com/documentation/web-api/reference/get-playlist
- Spotify Developer Dashboard:
  https://developer.spotify.com/dashboard
