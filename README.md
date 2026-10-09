# Pass the Pillow

Live Website: https://pass-and-pillow.onrender.com

For a quick 1-minute guide to start playing, see [QUICK_START.md](QUICK_START.md).
For detailed deployment and local server instructions, see [Installation.md](Installation.md).

Pass the Pillow is an automated, web-based party game application designed to eliminate bias and keep classic party games fair and unpredictable.

## Origin Story

The project originated during a gathering with friends and family. A group decided to play the classic party game "Pass the Pillow", but the traditional setup required a designated person to manually play and pause music. This created an unavoidable fairness issue: the person controlling the music could anticipate or observe who held the pillow and deliberately choose when to pause, influencing the outcome of the round. 

Searching online for an automated tool revealed plenty of generic countdown timers, but none tailored specifically to this use case--namely, an app that plays real music from a playlist at random and halts abruptly at an unpredictable moment without human intervention. This project was built to solve that problem, giving every player, including the host, an equal opportunity to participate.

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
