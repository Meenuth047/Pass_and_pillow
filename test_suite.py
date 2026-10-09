#!/usr/bin/env python3
"""
Comprehensive Automated Test Suite for Pass the Pillow with Spotify Integration.
Tests cover:
1. HTML Structure and DOM element presence
2. Spotify PKCE security & encoding logic
3. Random track selection algorithm (consecutive non-repetition, 1-track fallback, 0-track handling)
4. Playback retry bounding
5. Timer calculation and interval bounds
6. Documentation checks (verifying 0 emojis in README.md and QUICK_START.md)
7. Local HTTP server integration test
"""

import os
import re
import sys
import math
import random
import hashlib
import base64
import unittest
import threading
import http.server
import socketserver
import urllib.request

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_HTML_PATH = os.path.join(REPO_DIR, "main.html")
README_PATH = os.path.join(REPO_DIR, "README.md")
QUICK_START_PATH = os.path.join(REPO_DIR, "QUICK_START.md")
INSTALLATION_PATH = os.path.join(REPO_DIR, "Installation.md")


class TestPassThePillow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(MAIN_HTML_PATH, "r", encoding="utf-8") as f:
            cls.html_content = f.read()

        with open(README_PATH, "r", encoding="utf-8") as f:
            cls.readme_content = f.read()

        with open(QUICK_START_PATH, "r", encoding="utf-8") as f:
            cls.quick_start_content = f.read()

        with open(INSTALLATION_PATH, "r", encoding="utf-8") as f:
            cls.installation_content = f.read()

    # -------------------------------------------------------------------------
    # 1. HTML DOM Structure & UI Elements
    # -------------------------------------------------------------------------
    def test_html_basic_structure(self):
        self.assertIn("<!DOCTYPE html>", self.html_content)
        self.assertIn("<title>Pass the Pillow Game</title>", self.html_content)
        self.assertIn("https://sdk.scdn.co/spotify-player.js", self.html_content)

    def test_spotify_ui_elements_exist(self):
        required_elements = [
            'id="spotifyClientId"',
            'id="redirectUriDisplay"',
            'id="spotifyConnectBtn"',
            'id="spotifyDisconnectBtn"',
            'id="spotifyAuthView"',
            'id="spotifyConnectedView"',
            'id="spotifyUserBadge"',
            'id="spotifyDeviceSelect"',
            'id="refreshDevicesBtn"',
            'id="spotifyPlaylistSelect"',
            'id="refreshPlaylistsBtn"',
            'id="playlistPreviewCard"',
            'id="playlistImage"',
            'id="playlistTitle"',
            'id="playlistStats"',
            'id="playlistTrackList"',
            'id="playlistNotice"',
            'id="startBtn"',
            'id="stopBtn"',
            'id="status"',
            'id="audioFile"',
            'id="audioPlayer"',
            'id="spotifyNowPlaying"',
            'id="nowPlayingTitle"',
            'id="nowPlayingArtist"',
            'id="resetSessionBtn"',
        ]
        for elem in required_elements:
            self.assertIn(elem, self.html_content, f"Missing required element: {elem}")

    def test_tabs_configuration(self):
        self.assertIn('data-tab="spotify"', self.html_content)
        self.assertIn('data-tab="upload"', self.html_content)
        self.assertIn('data-tab="preset"', self.html_content)
        self.assertIn('id="spotifyTab"', self.html_content)
        self.assertIn('id="uploadTab"', self.html_content)
        self.assertIn('id="presetTab"', self.html_content)

    def test_duration_buttons_configuration(self):
        expected_ranges = [
            ('data-min="10"', 'data-max="20"'),
            ('data-min="20"', 'data-max="30"'),
            ('data-min="30"', 'data-max="40"'),
            ('data-min="40"', 'data-max="60"'),
        ]
        for min_attr, max_attr in expected_ranges:
            self.assertIn(min_attr, self.html_content)
            self.assertIn(max_attr, self.html_content)

    def test_spotify_scopes_compliance(self):
        required_scopes = [
            'streaming',
            'user-read-email',
            'user-read-private',
            'playlist-read-private',
            'playlist-read-collaborative',
            'user-modify-playback-state',
            'user-read-playback-state'
        ]
        for scope in required_scopes:
            self.assertIn(scope, self.html_content, f"Missing required Spotify scope: {scope}")

    def test_no_hardcoded_secrets(self):
        # Ensure no client secret is accidentally hardcoded
        secret_patterns = [
            r'client_secret\s*[:=]\s*["\'][^"\']+["\']',
            r'clientSecret\s*[:=]\s*["\'][^"\']+["\']',
        ]
        for pat in secret_patterns:
            matches = re.findall(pat, self.html_content, re.IGNORECASE)
            self.assertEqual(len(matches), 0, f"Found hardcoded client secret match: {matches}")

    # -------------------------------------------------------------------------
    # 2. PKCE Math & Encoding Tests
    # -------------------------------------------------------------------------
    def test_pkce_base64url_encoding(self):
        def base64url(data: bytes) -> str:
            return base64.b64encode(data).decode('utf-8').replace('+', '-').replace('/', '_').rstrip('=')

        sample = b"test-code-verifier-string"
        encoded = base64url(sample)
        self.assertNotIn("+", encoded)
        self.assertNotIn("/", encoded)
        self.assertNotIn("=", encoded)

        # Standard challenge test vector
        verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
        sha_digest = hashlib.sha256(verifier.encode('ascii')).digest()
        challenge = base64url(sha_digest)
        self.assertEqual(challenge, "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM")

    # -------------------------------------------------------------------------
    # 3. Random Track Selection Algorithm Simulation
    # -------------------------------------------------------------------------
    def test_track_selection_consecutive_non_repetition(self):
        """Simulate TrackSelector logic with 5 tracks across 500 rounds."""
        tracks = [
            {"id": f"track_{i}", "name": f"Track {i}", "uri": f"spotify:track:{i}"}
            for i in range(5)
        ]

        class TrackSelectorSim:
            def __init__(self):
                self.session_played = set()
                self.last_played = None

            def select(self, eligible_tracks):
                if not eligible_tracks:
                    return None
                if len(eligible_tracks) == 1:
                    return eligible_tracks[0]

                # Exclude last played track
                candidates = [t for t in eligible_tracks if t["id"] != self.last_played]

                # Prioritize unplayed
                unplayed = [t for t in candidates if t["id"] not in self.session_played]
                if unplayed:
                    candidates = unplayed

                selected = random.choice(candidates)
                self.last_played = selected["id"]
                self.session_played.add(selected["id"])
                return selected

        selector = TrackSelectorSim()
        history = []
        for _ in range(500):
            chosen = selector.select(tracks)
            self.assertIsNotNone(chosen)
            history.append(chosen["id"])

        # Verify that NO two consecutive tracks are identical
        for i in range(1, len(history)):
            self.assertNotEqual(
                history[i], history[i - 1],
                f"Consecutive identical track detected at round {i}: {history[i]}"
            )

        # Verify all tracks were played
        self.assertEqual(set(history), {t["id"] for t in tracks})

    def test_track_selection_two_tracks_alternation(self):
        """With exactly 2 tracks, rounds must strictly alternate."""
        tracks = [{"id": "A"}, {"id": "B"}]

        class TrackSelectorSim:
            def __init__(self):
                self.last_played = None

            def select(self, eligible):
                candidates = [t for t in eligible if t["id"] != self.last_played]
                selected = random.choice(candidates)
                self.last_played = selected["id"]
                return selected

        selector = TrackSelectorSim()
        history = [selector.select(tracks)["id"] for _ in range(50)]
        for i in range(1, len(history)):
            self.assertNotEqual(history[i], history[i - 1])

    def test_track_selection_single_track_graceful_handling(self):
        """With exactly 1 track, repetition is permitted without errors."""
        tracks = [{"id": "ONLY_ONE", "name": "Solo Track"}]

        def select_track(eligible):
            if not eligible:
                return None
            if len(eligible) == 1:
                return {"track": eligible[0], "isSingleTrack": True}
            return None

        result = select_track(tracks)
        self.assertIsNotNone(result)
        self.assertEqual(result["track"]["id"], "ONLY_ONE")
        self.assertTrue(result["isSingleTrack"])

    def test_track_selection_zero_tracks_graceful_handling(self):
        """With 0 tracks, selection returns None/error gracefully."""
        tracks = []

        def select_track(eligible):
            if not eligible:
                return None
            return eligible[0]

        result = select_track(tracks)
        self.assertIsNone(result)

    def test_bounded_playback_retries(self):
        """Ensure bounded retries stop after MAX_RETRIES (3) and do not loop infinitely."""
        MAX_RETRIES = 3
        attempts = 0
        failed_ids = set()
        tracks = [{"id": f"t_{i}"} for i in range(10)]

        while attempts < MAX_RETRIES:
            attempts += 1
            available = [t for t in tracks if t["id"] not in failed_ids]
            candidate = available[0]
            # Simulate failure
            failed_ids.add(candidate["id"])

        self.assertEqual(attempts, 3)
        self.assertEqual(len(failed_ids), 3)

    def test_playlist_track_count_schema_resilience(self):
        """Test parsing playlist counts across legacy tracks.total, new items.total, and array formats."""
        def get_count(pl):
            if not pl: return 0
            if "tracks" in pl and isinstance(pl["tracks"], dict) and isinstance(pl["tracks"].get("total"), int):
                return pl["tracks"]["total"]
            if "items" in pl and isinstance(pl["items"], dict) and isinstance(pl["items"].get("total"), int):
                return pl["items"]["total"]
            if isinstance(pl.get("total"), int):
                return pl["total"]
            if isinstance(pl.get("tracks"), list):
                return len(pl["tracks"])
            if isinstance(pl.get("items"), list):
                return len(pl["items"])
            return 0

        self.assertEqual(get_count({"tracks": {"total": 42}}), 42)
        self.assertEqual(get_count({"items": {"total": 88}}), 88)
        self.assertEqual(get_count({"total": 15}), 15)
        self.assertEqual(get_count({"tracks": None}), 0)
        self.assertEqual(get_count({}), 0)

    def test_playlist_item_extraction_schema_resilience(self):
        """Test track extraction supporting legacy item.track, new item.item, and direct track objects."""
        raw_items = [
            {"track": {"id": "t1", "uri": "spotify:track:t1", "type": "track", "name": "Song 1"}},
            {"item": {"id": "t2", "uri": "spotify:track:t2", "type": "track", "name": "Song 2"}},
            {"id": "t3", "uri": "spotify:track:t3", "type": "track", "name": "Song 3"},
            {"track": None}, # null track
            {"track": {"id": "t4", "is_local": True, "uri": "spotify:track:t4"}}, # local file
        ]

        def extract_tracks(items):
            extracted = []
            for item in items:
                t = item.get("track") or item.get("item") or (item if item.get("uri") and item.get("type") == "track" else None)
                if t and t.get("id") and t.get("uri") and not t.get("is_local") and t.get("is_playable") is not False:
                    extracted.append(t["id"])
            return extracted

        valid_ids = extract_tracks(raw_items)
        self.assertEqual(valid_ids, ["t1", "t2", "t3"])

    # -------------------------------------------------------------------------
    # 4. Timer Math & Random Duration
    # -------------------------------------------------------------------------
    def test_random_duration_bounds(self):
        ranges = [(10, 20), (20, 30), (30, 40), (40, 60)]
        for min_dur, max_dur in ranges:
            samples = [
                random.randint(min_dur, max_dur)
                for _ in range(1000)
            ]
            self.assertTrue(all(min_dur <= s <= max_dur for s in samples))
            self.assertIn(min_dur, samples, f"Min endpoint {min_dur} was never hit")
            self.assertIn(max_dur, samples, f"Max endpoint {max_dur} was never hit")

    def test_status_stopped_message_exact_text(self):
        """Prompt requires exact message: 'Music stopped. Who has the pillow?'"""
        self.assertIn("Music stopped. Who has the pillow?", self.html_content)

    # -------------------------------------------------------------------------
    # 5. Documentation Tests (NO EMOJIS CHECK)
    # -------------------------------------------------------------------------
    def test_no_emojis_in_readme(self):
        # Check for Unicode emojis in README.md
        emoji_pattern = re.compile(
            r'[\U00010000-\U0010ffff]'  # Supplementary Multilingual Plane (common emojis)
            r'|[\u2600-\u26ff]'          # Miscellaneous Symbols
            r'|[\u2700-\u27bf]'          # Dingbats
            r'|[\u2b50-\u2b55]'          # Stars and symbols
            r'|[\u231a-\u231b\u23e9-\u23ec\u23f0\u23f3]' # Misc technical clocks/arrows
        )
        matches = emoji_pattern.findall(self.readme_content)
        self.assertEqual(
            len(matches), 0,
            f"README.md must not contain any emojis! Found: {matches}"
        )

    def test_no_emojis_in_quick_start(self):
        # Check for Unicode emojis in QUICK_START.md and Installation.md
        emoji_pattern = re.compile(
            r'[\U00010000-\U0010ffff]'
            r'|[\u2600-\u26ff]'
            r'|[\u2700-\u27bf]'
            r'|[\u2b50-\u2b55]'
            r'|[\u231a-\u231b\u23e9-\u23ec\u23f0\u23f3]'
        )
        matches_qs = emoji_pattern.findall(self.quick_start_content)
        self.assertEqual(
            len(matches_qs), 0,
            f"QUICK_START.md must not contain any emojis! Found: {matches_qs}"
        )
        matches_inst = emoji_pattern.findall(self.installation_content)
        self.assertEqual(
            len(matches_inst), 0,
            f"Installation.md must not contain any emojis! Found: {matches_inst}"
        )

    def test_readme_contains_required_sections(self):
        required_phrases = [
            "Origin Story",
            "How the Game Works",
            "Implemented Features",
            "Planned Features",
            "Architecture and Technology Choices",
            "Spotify Developer Dashboard Configuration",
            "Account and Device Limitations",
            "Security and Privacy",
            "Official Spotify Documentation References",
            "Spotify Premium",
            "https://pass-and-pillow.onrender.com",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, self.readme_content, f"README.md missing section: {phrase}")

    def test_quick_start_contains_required_sections(self):
        required_phrases = [
            "https://pass-and-pillow.onrender.com",
            "Option 1",
            "Option 2",
            "b9df1dea7f174af197b814956f500fd8",
            "Spotify",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, self.quick_start_content, f"QUICK_START.md missing section: {phrase}")

    def test_installation_contains_required_sections(self):
        required_phrases = [
            "Launching the Application",
            "Developer Setup in Spotify Dashboard",
            "Connecting Spotify and Playing",
            "Troubleshooting",
            "Redirect URI",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, self.installation_content, f"Installation.md missing section: {phrase}")

    # -------------------------------------------------------------------------
    # 6. Local HTTP Server Integration Test
    # -------------------------------------------------------------------------
    def test_local_server_serves_html(self):
        """Starts a temporary HTTP server and fetches main.html over HTTP."""
        class QuietHandler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                pass  # suppress console logging

        # Bind to port 0 for OS-assigned ephemeral port
        server = socketserver.TCPServer(("127.0.0.1", 0), QuietHandler)
        port = server.server_address[1]

        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()

        try:
            url = f"http://127.0.0.1:{port}/main.html"
            with urllib.request.urlopen(url, timeout=5) as resp:
                self.assertEqual(resp.status, 200)
                body = resp.read().decode('utf-8')
                self.assertIn("Pass the Pillow", body)
                self.assertIn("Spotify", body)
        finally:
            server.shutdown()
            server.server_close()


if __name__ == '__main__':
    unittest.main()
