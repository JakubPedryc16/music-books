from typing import List
from scripts.spotify_config import sp

def play_song(track_id: str):
    """Odtwórz utwór na aktywnym urządzeniu Spotify"""
    track_uri = f"spotify:track:{track_id}"
    devices = sp.devices()
    if not devices["devices"]:
        print("❌ Brak aktywnego urządzenia. Otwórz Spotify na PC/telefonie.")
        return
    device_id = devices["devices"][0]["id"]
    sp.start_playback(device_id=device_id, uris=[track_uri])
    print(f"▶️ Odtwarzam: {track_uri}")

def play_playlist(track_ids: List[str]):
    devices = sp.devices()
    if not devices["devices"]:
        print("❌ Brak aktywnego urządzenia. Otwórz Spotify na PC/telefonie.")
        return
    device_id = devices["devices"][0]["id"]
    sp.start_playback(device_id=device_id, uris=track_ids)
    print(f"▶️ Odtwarzam playlistę z {len(track_ids)} utworami")