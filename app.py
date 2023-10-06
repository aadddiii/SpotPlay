import keys
import re
import spotipy
import functions
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
import recommendations as rec
import requests, json, secrets, base64
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
client_id = keys.id
client_secret = keys.secret
scope = "playlist-modify-private playlist-modify-public user-read-private user-read-email"
redirect_uri = 'http://localhost:5000/callback'
app.secret_key = secrets.token_hex(16)

global tracks
tracks = []

df = pd.read_csv("data/preprocessed_dataset.csv", index_col=0)

@app.route("/", methods=["GET"])
def login():
    session["key"] = client_secret
    return redirect('https://accounts.spotify.com/authorize?' +
                    f'response_type=code&client_id={client_id}&' +
                    f'scope={scope}&redirect_uri={redirect_uri}&' + 
                    f'state={client_secret}')
    
@app.route("/callback", methods=["GET", "POST"])
def callback():
    session["codeauth"] = request.args.get('code')
    headers = {
        'Authorization': f'Basic {base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': request.args.get('code'),
        'redirect_uri': redirect_uri
    }
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    tokens = json.loads(response.content)

    session['access_token'] = tokens['access_token']

    # Fetch user information
    sp = spotipy.Spotify(auth=session['access_token'])
    user_info = sp.current_user()
    session['user_name'] = user_info['display_name']
    
    print(user_info)

    return redirect(url_for("index"))

@app.route("/home", methods=["GET", "POST"])
def index():
    user_name = session.get('user_name', 'Guest')
    
    if request.method == "POST":
        link = request.form.get("link")
        if link:
            return redirect(url_for("recommend", link=link))
    return render_template("index.html", user_name=user_name)


@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    sp = spotipy.Spotify(auth=session['access_token'])
    link = request.form.get("link")

    if not link:
        return render_template("index.html", error="Invalid Spotify song link.")

    song_id_match = re.search(r'(?<=track/)[\w]+', link)

    if not song_id_match:
        return render_template("index.html", error="Invalid Spotify song link.")

    song_id = song_id_match.group(0)
    song_info = sp.track(song_id)
    audio_features = sp.audio_features(song_id)

    if song_info and audio_features:
            input_features = [audio_features[0]['danceability'], audio_features[0]['valence'], audio_features[0]['liveness'], audio_features[0]['energy']]
            track_id = link.split('/')[-1]
            input_song_name = song_info['name']
            input_artist = song_info['artists'][0]['name']
            df_without_input = df[(df['track_id'] != track_id) & (df['track_name'] != input_song_name) & (df['artists'] != input_artist)]
            top_songs = rec.content_based_recommendation(input_features, df_without_input, top_n=10) 

            recommended_tracks = []
            for song in top_songs:
                track_info = {
                    'id': song['track_id'],
                    'name': song['track_name'],
                    'artists': song['artists'],
                    'image_url': functions.get_album_art_url(song['track_id']),
                    'external_url': 'http://open.spotify.com/track/%s' % song['track_id'],
                }
                recommended_tracks.append(track_info)
                
            recommend_id = [track['id'] for track in recommended_tracks]

            # Store the recommended tracks in the user's session
            session["recommended_tracks"] = recommend_id
            
            # Render the result.html template with the track information
            return render_template("result.html", tracks=recommended_tracks)

    return render_template("index.html", error="Invalid Spotify song link.")

@app.route("/create_playlist", methods=["POST", "GET"])
def create_playlist():
    sp = spotipy.Spotify(auth=session['access_token'])
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user= user_id,name="playlist_name", public=False, description="playlist_description")

    # Add the recommended tracks to the playlist
    sp.playlist_add_items(playlist_id=playlist['id'], items=session["recommended_tracks"])
    
    playlist_link = playlist['external_urls']['spotify']
    return redirect(location = f'{playlist_link}', code = 302)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
