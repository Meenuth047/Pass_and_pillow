# Pass the Pillow

Live Website: https://pass-and-pillow.onrender.com

Pass the Pillow is an automated, web-based party game application designed to eliminate bias and keep classic party games fair and unpredictable.

## Origin Story

The project originated during a gathering with friends and family. A group decided to play the classic party game "Pass the Pillow", but the traditional setup required a designated person to manually play and pause music. This created an unavoidable fairness issue: the person controlling the music could anticipate or observe who held the pillow and deliberately choose when to pause, influencing the outcome of the round. 

Searching online for an automated tool revealed plenty of generic countdown timers, but none tailored specifically to this use case--namely, an app that plays real music from a playlist at random and halts abruptly at an unpredictable moment without human intervention. This project was built to solve that problem, giving every player, including the host, an equal opportunity to participate.

## Step 1: Open the Game

Open https://pass-and-pillow.onrender.com in your mobile browser or desktop browser.

---

## Option 1: Quick Play (Use Author's App)

To start playing immediately without setting up a developer account:

1. On the Spotify tab, paste this Client ID:
   ```
   b9df1dea7f174af197b814956f500fd8
   ```
2. Click "Connect with Spotify" and log in with your Spotify account.
3. Select your playback device:
   - On Desktop: In-browser Web Player.
   - On Mobile: Open the Spotify app on your phone, start playing briefly, and choose your phone from the device dropdown.
4. Select a playlist from your library.
5. Choose a stop duration (10-20s, 20-30s, 30-40s, or 40-60s).
6. Click "Start Game" and pass the pillow!

---

## Option 2: Play with Your Own Spotify App & Personal Songs

If you want to use your own Spotify Developer credentials:

Requirements: A Spotify Premium account is required for third-party playback.

1. Go to the Spotify Developer Dashboard:
   https://developer.spotify.com/dashboard
2. Click "Create App", enter an app name (such as "Pass the Pillow"), and select "Web API" and "Web Playback SDK".
3. Under "Redirect URIs", add these three URIs:
   - `https://pass-and-pillow.onrender.com/`
   - `https://pass-and-pillow.onrender.com`
   - `https://pass-and-pillow.onrender.com/index.html`
4. Click "Add" for each, then scroll down and click "Save".
5. Copy your Client ID from the dashboard overview.
6. Open https://pass-and-pillow.onrender.com, paste your personal Client ID, and click "Connect with Spotify".

---

## Offline Alternative (No Spotify Needed)

Click the "Upload Music" tab to upload any audio file directly from your phone or computer.

## Architecture and Technology Choices

The application is structured as a client-side Single-Page Application (SPA) contained within `main.html`:

- Vanilla HTML5, CSS3, and JavaScript: Eliminates complex build tools, external runtime dependencies, bundlers, and backend servers.
- Web Crypto API: Provides cryptographically secure random values and SHA-256 digest calculation for PKCE code verifiers and code challenges (`crypto.getRandomValues`, `crypto.subtle.digest`).
- Spotify Web API: Communicates via HTTP requests (`fetch`) for user profile, playlist retrieval, device enumeration, and playback control (`/v1/me/player/play`, `/v1/me/player/pause`).
- Spotify Web Playback SDK (`https://sdk.scdn.co/spotify-player.js`): Creates a local browser playback device for desktop environments.
- HTML5 Audio API: Powers the offline fallback player via `URL.createObjectURL(file)` and native `<audio>` element controls.
