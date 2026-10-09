# Pass the Pillow

Live Website: https://pass-and-pillow.onrender.com

Pass the Pillow is an automated, web-based party game application designed to eliminate bias and keep classic party games fair and unpredictable.

## Step 1: Open the Game

Open https://pass-and-pillow.onrender.com in your mobile browser or desktop browser.

---

## Play with Your Own Spotify App & Personal Songs

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

## 100% Free YouTube Mode (No Spotify Premium or Login Needed)

If you do not have Spotify Premium or do not wish to log in:

1. Click the "YouTube (Free)" tab (active by default).
2. Choose one of the curated party collections:
   - Bollywood Party Hits (Kala Chashma, Badtameez Dil, Gallan Goodiyaan, etc.)
   - Global Pop Hits (Levitating, Blinding Lights, Uptown Funk, etc.)
   - 2000s and Retro Hits (Rasputin, Dancing Queen, Don't Stop Me Now, etc.)
   - Or select "Custom YouTube Playlist or Video Link" and paste any public YouTube link.
3. Choose your stop duration and click "Start Game".
4. The game automatically skips instrumental intros, starting directly at high-energy choruses.
5. When you play using YouTube, if you see "Video unavailable", tap on "Start Game" again.

---

## Offline Alternative (No Internet or Spotify Needed)

Click the "Upload Music" tab to upload any audio file directly from your phone or computer.

## Architecture and Technology Choices

The application is structured as a client-side Single-Page Application (SPA) located in `src/`:

- Vanilla HTML5, CSS3, and JavaScript: Eliminates complex build tools, external runtime dependencies, bundlers, and backend servers.
- YouTube IFrame Player API (`https://www.youtube.com/iframe_api`): Provides 100% free, responsive music playback with zero login or subscription requirements.
- Web Crypto API: Provides cryptographically secure random values and SHA-256 digest calculation for PKCE code verifiers and code challenges (`crypto.getRandomValues`, `crypto.subtle.digest`).
- Spotify Web API: Communicates via HTTP requests (`fetch`) for user profile, playlist retrieval, device enumeration, and playback control (`/v1/me/player/play`, `/v1/me/player/pause`).
- Spotify Web Playback SDK (`https://sdk.scdn.co/spotify-player.js`): Creates a local browser playback device for desktop environments.
- HTML5 Audio API: Powers the offline fallback player via `URL.createObjectURL(file)` and native `<audio>` element controls.
- Automatic Smart Hook & Vocal Start Engine: Analyzes synced lyric timestamps and musical structure heuristics to automatically start tracks directly on the iconic chorus hook or vocal line, skipping empty instrumental intros without manual trimming.

## Repository Structure

- `src/`: Contains source code and configuration files (`index.html`, `main.html`, `render.yaml`, `test_suite.py`).
- `doc/`: Contains detailed guides (`Installation.md`).
- `README.md`: Project overview and quick start guide.

## Documentation

For full step-by-step setup, Render deployment instructions, and troubleshooting:
- [Installation and Deployment Guide](doc/Installation.md)
