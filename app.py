import keys
import re
import spotipy
import spotify_cli
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
import recommendations as rec
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
global tracks
tracks = []
# Replace with your Spotify API credentials
client_id = keys.id
client_secret = keys.secret
scope = "playlist-modify-private playlist-modify-public"

# Initialize Spotipy with SpotifyOAuth
auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, scope=scope, redirect_uri="http://localhost")
sp = spotipy.Spotify(auth_manager=auth_manager)

df = pd.read_csv("data/preprocessed_dataset.csv", index_col=0)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        link = request.form.get("link")
        if link:
            return recommend(link)
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    link = request.form.get("link")
    
    song_id = re.search(r'(?<=track/)[\w]+', link)
    if song_id:
        song_id = song_id.group(0)
        song_info = sp.track(song_id)
        audio_features = sp.audio_features(song_id)
        if song_info and audio_features:
            input_features = [audio_features[0]['danceability'], audio_features[0]['valence'], audio_features[0]['liveness'], audio_features[0]['energy']]
            track_id = link.split('/')[-1]
            input_song_name = song_info['name']
            input_artist = song_info['artists'][0]['name']
            df_without_input = df[(df['track_id'] != track_id) & (df['track_name'] != input_song_name) & (df['artists'] != input_artist)]
            top_songs = rec.content_based_recommendation(input_features, df_without_input, top_n=10) 

            # Create a dictionary to store track information

            for index, song in top_songs.iterrows():
                track_info = {
                    'id': song['track_id'],
                    'name': song['track_name'],
                    'artists': song['artists'],
                    'image_url': spotify_cli.get_album_art_url(song['track_id']),
                    'external_url': 'http://open.spotify.com/track/%s' % song['track_id'],
                }
                tracks.append(track_info)
                
            # Render the result.html template with the track information
            return render_template("result.html", tracks=tracks)

    return render_template("index.html", error="Invalid Spotify song link.")

@app.route("/create_playlist", methods=["POST", "GET"])
def create_playlist():
    playlist_name = "Recommended Songs Playlist"
    playlist_description = "Playlist of recommended songs based on the input track."
    playlist = sp.user_playlist_create(user=sp.me()['id'], name=playlist_name, public=False, description=playlist_description)

    # Add the recommended tracks to the playlist
    tracks_to_add = []
    for track in tracks:
        tracks_to_add.append(track['id'])
    sp.playlist_add_items(playlist_id=playlist['id'], items=tracks_to_add)
    
    playlist_link = playlist['external_urls']['spotify']
    return redirect(f'{playlist_link}')


if __name__ == "__main__":
    app.run(debug=True)
