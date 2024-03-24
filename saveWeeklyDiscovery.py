from flask import Flask, request, url_for, session, redirect, jsonify
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import os
from dotenv import load_dotenv
import time

app = Flask(__name__)
load_dotenv(".weekly_env")

app.config["SESSION_COOKIE_NAME"] = "Spotify Cookie"
app.secret_key = os.getenv("APPSECRET")
TOKEN_INFO = "token_info"

# Initialize SpotifyOAuth once and reuse
spotify_oauth = SpotifyOAuth(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    redirect_uri=os.getenv("REDIRECTURI"),
    scope=os.getenv("SCOPE")
)

@app.route('/')
def login():
    auth_url = spotify_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = spotify_oauth.get_access_token(code) # Ensure the token is received as a dictionary
    session[TOKEN_INFO] = token_info
    return redirect(url_for('save_discover_weekly'))

@app.route('/saveDiscoverWeekly')
def save_discover_weekly():
    access_token = get_token()
    if not access_token:
        return redirect(url_for('login'))
    sp = spotipy.Spotify(auth=access_token)
    user_id = sp.current_user()['id']

    discover_weekly_playlist_id, saved_weekly_playlist_id = find_playlists(sp, user_id)
    if not discover_weekly_playlist_id:
        return jsonify({"error": "Discover Weekly playlist not found"}), 404

    if not saved_weekly_playlist_id:
        #saved_weekly_playlist_id = sp.user_playlist_create(user_id, "Saved Weekly", public=True)['id']
        saved_weekly_playlist_id = sp.user_playlist_create(user_id, "Discover Weekly Archive", public=True)['id']
    
    copy_tracks(sp, discover_weekly_playlist_id, saved_weekly_playlist_id)
    return jsonify({"message": "Discover Weekly songs added successfully"}), 200

def find_playlists(sp, user_id):
    """Find 'Discover Weekly' and 'Saved Weekly' playlists, return their IDs."""
    discover_weekly_id = saved_weekly_id = None
    for playlist in sp.current_user_playlists(limit=50)['items']:
        if playlist['name'] == "Discover Weekly":
            discover_weekly_id = playlist['id']
        #elif playlist['name'] == "Saved Weekly":
        elif playlist['name'] == "Discover Weekly Archive":
            saved_weekly_id = playlist['id']
    return discover_weekly_id, saved_weekly_id

def fetch_all_tracks(sp, playlist_id):
    """Fetch all tracks of a playlist handling pagination."""
    tracks = []
    results = sp.playlist_tracks(playlist_id, fields="items.track.uri,next")
    while results:
        tracks.extend([item['track']['uri'] for item in results['items']])
        if results['next']:
            results = sp.next(results)
        else:
            break
    return tracks

def copy_tracks(sp, source_playlist_id, target_playlist_id):
    """Copy tracks from source playlist to target playlist without duplicating, considering pagination."""
    user_id = sp.current_user()['id']
    # Fetch existing tracks in the target playlist
    existing_track_uris = fetch_all_tracks(sp, target_playlist_id)
    
    # Fetch tracks from the source playlist
    source_track_uris = fetch_all_tracks(sp, source_playlist_id)

    # Filter out tracks that already exist in the target playlist
    tracks_to_add = [uri for uri in source_track_uris if uri not in existing_track_uris]

    # Add only the unique tracks to the target playlist in batches to respect API limits
    batch_size = 100
    for i in range(0, len(tracks_to_add), batch_size):
        sp.user_playlist_add_tracks(user_id, target_playlist_id, tracks_to_add[i:i+batch_size])


def get_token():
    token_info = session.get(TOKEN_INFO)
    if not token_info or token_info.get('expires_at', 0) - int(time.time()) < 60:
        return None
    return token_info['access_token']

if __name__ == '__main__':
    app.run(debug=True)
