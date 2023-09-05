import keys
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Replace with your Spotify API credentials
client_id = keys.id
client_secret = keys.secret

def get_spotify_client():
    # Replace with your Spotify API credentials
    client_id = keys.id
    client_secret = keys.secret
    client_uri = "http://localhost"

    # Set the required scopes for playlist creation
    scope = "playlist-modify-private playlist-modify-public"

    # Initialize Spotipy with SpotifyOAuth
    auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, scope=scope, redirect_uri=client_uri)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp

sp = get_spotify_client()

def get_info(link):   
    song_id = re.search(r'(?<=track/)[\w]+', link)
    if song_id:
        song_id = song_id.group(0)
        song_info = sp.track(song_id)
        audio_features = sp.audio_features(song_id)
        return song_info, audio_features
    else:
        print("Invalid Spotify song link.")
        return None, None

def get_album_art_url(track_id):
    track_info = sp.track(track_id)
    album_art_url = track_info['album']['images'][0]['url']
    return album_art_url
