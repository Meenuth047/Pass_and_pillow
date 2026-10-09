# Installation and Deployment Guide: Pass the Pillow

## Launching the Application

### Live Deployment on Render for Mobile and Web

To allow anyone to play on their mobile phone or laptop without running a local Python server, deploy the app for free as a Render Static Site:

### Step 1: Connect Your GitHub Repository to Render
1. Go to https://dashboard.render.com and sign up or log in.
2. Click the "New +" button in the top navigation bar and select "Static Site".
3. Connect your GitHub account and select your `Pass_and_pillow` repository.

### Step 2: Configure the Static Site Settings
In the Render creation form, configure the fields:
- Name: `pass-and-pillow` (or your preferred name)
- Branch: `main`
- Build Command: leave blank (or enter `echo 'Build complete'`)
- Publish Directory: `src` (the directory containing index.html and main.html)
- Click "Create Static Site".

Render will automatically deploy the site and provide a free, secure live URL (such as `https://pass-and-pillow.onrender.com`).

### Step 3: Add the Live Render URL to Spotify Developer Dashboard
1. Open your Spotify Developer Dashboard at https://developer.spotify.com/dashboard.
2. Open your app settings.
3. Under "Redirect URIs", add your live Render URL:
   - `https://your-service-name.onrender.com/`
   - `https://your-service-name.onrender.com/index.html`
4. Click Save.

Now anyone with a phone can open the Render URL, connect their Spotify account, and play directly!

---

## Local Development (Optional)

If you prefer testing locally on a computer:
1. Open a terminal in the project directory:
   ```bash
   cd /path/to/Pass_and_pillow
   ```
2. Start a local HTTP server pointing to the `src` directory:
   ```bash
   python3 -m http.server 8000 -d src
   # or
   cd src && python3 -m http.server 8000
   ```
3. Open `http://127.0.0.1:8000/` in your browser.

---

## Developer Setup in Spotify Dashboard

To use Spotify playlists, register an application in the Spotify Developer Dashboard:

1. Visit the Spotify Developer Dashboard at:
   https://developer.spotify.com/dashboard
2. Log in with your Spotify account and click "Create App".
3. Enter an App Name (for example: "Pass the Pillow") and description.
4. Add your Redirect URIs:
   - For Render live hosting: `https://your-service-name.onrender.com/`
   - For local development: `http://127.0.0.1:8000/` or `http://localhost:8000/`
5. Check the boxes for "Web API" and "Web Playback SDK".
6. Save the settings and copy the Client ID displayed on the app dashboard.

Important: Never commit or share your Spotify Client ID in public code repositories. The application stores it only in your browser local storage.

---

## Connecting Spotify and Playing

1. Open your live Render URL (or local server address).
2. On the Spotify tab, paste your Client ID into the input field.
3. Click "Connect with Spotify".
4. Log in to Spotify and approve access. You will be redirected back to the game.
5. Choose your playback device:
   - In-browser Web Player: Plays directly in desktop Chrome, Firefox, Edge, or Safari.
   - External device / Mobile Phone: Open the official Spotify app on your phone, start playing briefly, and choose your phone from the device dropdown.
6. Select a playlist from your library. The game displays the playlist cover, track count, and preview track list.
7. Select a stop duration range (10-20s, 20-30s, 30-40s, or 40-60s).
8. Click "Start Game".
   - The game selects an eligible track at random.
   - When playback starts, the randomized timer begins counting down.
   - The music automatically stops when the timer expires, showing: "Music stopped. Who has the pillow?"
   - To stop immediately at any moment, click "Stop Music Manually".

---

## Alternative Offline Playback

If you do not have Spotify Premium or are offline:
1. Click the "Upload Music" tab to load any local MP3, WAV, or OGG file from your device.
2. Or click the "Preset Songs" tab to use built-in sample audio.
3. Select your stop duration and click "Start Game".

---

## Troubleshooting

- Error: "Spotify playback failed: Premium required"
  Spotify API and Web Playback SDK strictly require a Spotify Premium subscription. Free tier accounts cannot stream through third-party web apps. Use the "Upload Music" tab for local files instead.

- Error: "Device not found or inactive"
  If using an external device or if playing on mobile, open the official Spotify app on your device, start playing any track briefly, pause it, and then click "Refresh" next to the device dropdown in Pass the Pillow.

- In-browser Web Player not appearing on mobile
  The Spotify Web Playback SDK requires Encrypted Media Extensions (EME), which mobile browsers (iOS Safari, Android Chrome) do not support. On mobile devices, launch the Spotify mobile app and select it as the active playback device in the dropdown.

- Error: "State verification mismatch"
  This error indicates the authorization flow was interrupted or tampered with. Click "Connect with Spotify" again to initiate a fresh session.

- Stuck or Stale Timers
  Click "Stop Music Manually" or switch tabs to immediately clear all active timers and pause playback.
