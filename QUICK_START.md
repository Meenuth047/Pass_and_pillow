# Quick Start Guide: Pass the Pillow

## Launching the Application

1. Open a terminal in the project directory:
   ```bash
   cd /path/to/Pass_and_pillow
   ```
2. Start a local HTTP server using Python:
   ```bash
   python3 -m http.server 8000
   ```
3. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/main.html
   ```

## Developer Setup in Spotify Dashboard

To use Spotify playlists, register an application in the Spotify Developer Dashboard:

1. Visit the Spotify Developer Dashboard at:
   https://developer.spotify.com/dashboard
2. Log in with your Spotify account and click "Create App".
3. Enter an App Name (for example: "Pass the Pillow") and description.
4. Add the exact Redirect URI where you are running the game:
   - For local use: `http://127.0.0.1:8000/main.html`
   - Alternatively: `http://localhost:8000/main.html`
5. Check the boxes for "Web API" and "Web Playback SDK".
6. Save the settings and copy the Client ID displayed on the app dashboard.

Important: Never commit or share your Spotify Client ID in public code repositories. The application stores it only in your browser local storage.

## Connecting Spotify and Playing

1. Open Pass the Pillow at `http://127.0.0.1:8000/main.html`.
2. On the Spotify tab, paste your Client ID into the input field.
3. Click "Connect with Spotify".
4. Log in to Spotify and approve access. You will be redirected back to the game.
5. Choose your playback device:
   - In-browser Web Player: Plays directly in desktop Chrome, Firefox, Edge, or Safari.
   - External device: If playing on mobile or a smart speaker, open the official Spotify app and select it from the device dropdown.
6. Select a playlist from your library. The game displays the playlist cover, track count, and preview track list.
7. Select a stop duration range (10-20s, 20-30s, 30-40s, or 40-60s).
8. Click "Start Game".
   - The game selects an eligible track at random.
   - When playback starts, the randomized timer begins counting down.
   - The music automatically stops when the timer expires, showing: "Music stopped. Who has the pillow?"
   - To stop immediately at any moment, click "Stop Music Manually".

## Alternative Offline Playback

If you do not have Spotify Premium or are offline:
1. Click the "Upload Music" tab to load any local MP3, WAV, or OGG file from your computer.
2. Or click the "Preset Songs" tab to use built-in sample audio.
3. Select your stop duration and click "Start Game".

## Troubleshooting

- Error: "Spotify playback failed: Premium required"
  Spotify API and Web Playback SDK strictly require a Spotify Premium subscription. Free tier accounts cannot stream through third-party web apps. Use the "Upload Music" tab for local files instead.

- Error: "Device not found or inactive"
  If using an external device or if the in-browser Web Player is not ready, open the official Spotify app on your phone, tablet, or desktop, start playing any song briefly, pause it, and then click "Refresh" next to the device dropdown in Pass the Pillow.

- In-browser Web Player not appearing in device list
  The Spotify Web Playback SDK requires Encrypted Media Extensions (EME) and must be served over `http://127.0.0.1`, `http://localhost`, or HTTPS. Mobile browsers (iOS Safari, Android Chrome) do not support the Web Playback SDK; use the official Spotify mobile app and Spotify Connect instead.

- Error: "State verification mismatch"
  This error indicates the authorization flow was interrupted or tampered with. Simply click "Connect with Spotify" again to initiate a fresh session.

- Stuck or Stale Timers
  Click "Stop Music Manually" or switch tabs to immediately clear all active timers and pause playback.
