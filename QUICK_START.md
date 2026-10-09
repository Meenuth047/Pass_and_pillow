# Quick Start Guide: Pass the Pillow

Live Website: https://pass-and-pillow.onrender.com
(You can also click the live link in the README.md)

---

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
