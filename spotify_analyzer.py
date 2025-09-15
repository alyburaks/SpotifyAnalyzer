import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter

load_dotenv("client.env")

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", "http://127.0.0.1:8888/callback/")
SCOPE = "playlist-read-private user-library-read user-top-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

def analyze_playlist(playlist_id):
    results = sp.playlist_items(playlist_id, additional_types=['track'])
    tracks = results['items']

    song_lengths = []
    artists = []
    popularity_scores = []

    for item in tracks:
        track = item['track']
        if track:
            song_lengths.append(track['duration_ms'])
            popularity_scores.append(track['popularity'])
            artists.extend([artist['name'] for artist in track['artists']])

    if not song_lengths:
        print("No tracks found in playlist.")
        return

    avg_length = sum(song_lengths) / len(song_lengths)
    avg_popularity = sum(popularity_scores) / len(popularity_scores)
    most_common_artist = Counter(artists).most_common(1)[0]

    print(f"Total Songs: {len(song_lengths)}")
    print(f"Average Song Length: {round(avg_length/60000,2)} minutes")
    print(f"Average Popularity Score: {round(avg_popularity,1)} / 100")
    print(f"Most Common Artist: {most_common_artist[0]} ({most_common_artist[1]} songs)")

if __name__ == "__main__":
    playlist_url = input("Enter a Spotify playlist URL: ")
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    analyze_playlist(playlist_id)
