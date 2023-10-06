import spotipy
from spotipy import SpotifyOAuth, Spotify

# Set up the SpotifyOAuth object
auth_manager = SpotifyOAuth(
client_id='32c03a1df6824e509aa71e92283e8973',
client_secret='a995d73fb79841728d8326a2663afc46',
redirect_uri="http://localhost",
scope="user-read-private user-read-email"
)

# Get the authorization URL and have the user authorize your app
auth_url = auth_manager.get_authorize_url()
print(f'Please visit this URL to authorize the application: {auth_url}')

# After the user authorizes your app, get the authorization code from the redirect URL
# and use it to get an access token
code = input('Please enter the authorization code: ')
auth_manager.get_access_token(code)

# Now you can use Spotipy to make authenticated API requests
sp = spotipy.Spotify(auth_manager=auth_manager)
results = sp.current_user_saved_tracks(limit=10, offset=5, market='JP')
print(results)