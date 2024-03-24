#!/usr/bin/env python3
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect, jsonify
import datetime
import time
from collections import defaultdict

# Initialise Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv(".monthly_env")

# Set the session cookie and secret key from environment variables
app.config["SESSION_COOKIE_NAME"] = "Spotify Cookie"
app.secret_key = os.getenv("APPSECRET")

# Spotify API credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECTURI")

print("CLIENT_ID:", CLIENT_ID)
print("CLIENT_SECRET:", CLIENT_SECRET)
print("REDIRECT_URI:", REDIRECT_URI)

# Token information key in the session
TOKEN_INFO = "token_info"

# Last run file to keep track of the last run timestamp
LAST_RUN_FILE = "last_run.txt"

# Spotify OAuth scope
SCOPE = "user-library-read playlist-modify-public playlist-modify-private"

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('add_liked_songs_to_monthly_playlist'))

@app.route('/addLikedSongs')
def add_liked_songs_to_monthly_playlist():
    token_info = get_token()
    if isinstance(token_info, str):
    
        sp = spotipy.Spotify(auth=token_info)
        user_id = sp.current_user()["id"]

        # Determine the last time this script was run
        last_run = get_last_run_time()

        # Fetch liked songs since last run
        liked_songs = fetch_liked_songs_since(sp, last_run)

        # Group songs by the month they were added
        monthly_songs = group_songs_by_month(liked_songs)

        # Add songs to the appropriate monthly playlists
        for month, tracks in monthly_songs.items():
            playlist_id = find_or_create_playlist(sp, user_id, month)
            unique_tracks = filter_existing_tracks(sp, playlist_id, tracks)
            if unique_tracks:
                sp.playlist_add_items(playlist_id, unique_tracks)

        # Update the last run time
        update_last_run_time()

        # Returning a valid JSON response indicating success
        return jsonify({"message": "Liked songs added to their respective monthly playlists."}), 200
    elif token_info:
        # If get_token did not return a string (thus returned a redirect), execute it to redirect the client
        return token_info
    else:
        # Fallback in case something unexpected happens, returning a valid error response
        return jsonify({"error": "An unexpected error occurred"}), 500

def filter_existing_tracks(sp, playlist_id, track_ids):
    """Filter out track IDs that already exist in the specified playlist."""
    existing_tracks = sp.playlist_tracks(playlist_id)
    existing_track_ids = [item["track"]["id"] for item in existing_tracks["items"]]
    
    return [track_id for track_id in track_ids if track_id not in existing_track_ids]



def add_liked_songs_to_monthly_playlist_route():
    return add_liked_songs_to_monthly_playlist()


# def fetch_liked_songs_since(sp, since_time):
#     """Fetch liked songs added since a given time."""
#     try:
#         results = sp.current_user_saved_tracks(limit=50)
#         songs = []

#         if not results['items']:
#             print("No items found in results")
#             return songs

#         for item in results["items"]:
#             print("Inspecting item structure:", item)  # Debugging line to inspect item structure
#             try:
#                 added_at = datetime.datetime.strptime(item["added_at"], "%Y-%m-%dT%H:%M:%SZ")
#                 if added_at > since_time:
#                     songs.append(item["track"]["id"])
#                 else:
#                     break  # Exiting early as items are sorted by added_at in descending order
#             except TypeError as e:
#                 print(f"TypeError encountered: {e}. Item structure may be incorrect.")
#                 break

#             if results["next"]:
#                 results = sp.next(results)
#             else:
#                 break

#         return songs
#     except spotipy.SpotifyException as e:
#         print(f"SpotifyException: {e.http_status} - {e.code}: {e.msg}\n{e.reason}")
#         return []

def fetch_liked_songs_since(sp, since_time):
    """Fetch liked songs added since a given time, including their added_at timestamps."""
    results = sp.current_user_saved_tracks(limit=50)
    songs = []

    while results:
        for item in results["items"]:
            added_at_str = item["added_at"]
            added_at = datetime.datetime.strptime(added_at_str, "%Y-%m-%dT%H:%M:%SZ")
            if added_at > since_time:
                songs.append({'id': item["track"]["id"], 'added_at': added_at_str})
            else:
                # Since the results are in descending order, we can break early
                return songs

        if results["next"]:
            results = sp.next(results)
        else:
            break

    return songs

def group_songs_by_month(songs):
    """Group song IDs by the month they were added."""
    # This example assumes you've fetched the songs' added_at timestamps
    # and have a way to group them by month. You may need a separate function
    # to fetch these details based on song IDs.
    monthly_songs = defaultdict(list)  # Example structure: {"January 2021": ["song_id1", "song_id2"]}
    # Implement the grouping logic here
    for song in songs:
        added_at = datetime.datetime.strptime(song['added_at'], "%Y-%m-%dT%H:%M:%SZ")
        month_year = added_at.strftime("%B %Y")
        monthly_songs[month_year].append(song['id'])
    return dict(monthly_songs)

def find_or_create_playlist(sp, user_id, month):
    """
    Find a playlist by its name (month) or create it if it doesn't exist.
    
    Parameters:
    - sp: The Spotipy client instance.
    - user_id: The Spotify user ID.
    - month: The name of the playlist (e.g., "March 2021").
    
    Returns:
    - The Spotify ID of the existing or newly created playlist.
    """
    # First, try to find the playlist by name among the user's playlists
    playlists = sp.current_user_playlists(limit=50)
    for playlist in playlists['items']:
        if playlist['name'] == month:
            return playlist['id']

    # If the playlist was not found, create a new one with the given name
    new_playlist = sp.user_playlist_create(user_id, month, public=True)
    return new_playlist['id']
    # target_month = month.strip().lower()
    # playlists = sp.current_user_playlists(limit=50)
    # while playlists:
    #     for playlist in playlists['items']:
    #         playlist_name = playlist['name'].strip().lower()
    #         print(f"Comparing: '{playlist_name}' with '{target_month}'")
    #         if playlist_name == target_month:
    #             print(f"Match found for {month}, not creating a new playlist.")
    #             return playlist['id']
    #     if playlists['next']:
    #         playlists = sp.next(playlists)
    #     else:
    #         playlists = None

    # print(f"No match found for {month}, creating a new playlist.")
    # new_playlist = sp.user_playlist_create(user_id, month.title(), public=True)
    # return new_playlist['id']

def add_tracks_to_playlist(sp, user_id, playlist_id, tracks):
    """
    Add tracks to a specified playlist.
    
    :param sp: Spotipy client instance
    :param user_id: Spotify user ID
    :param playlist_id: The Spotify ID of the playlist to add tracks to
    :param tracks: A list of Spotify track URIs to add to the playlist
    """
    # Spotipy handles adding tracks in batches if the list is long
    sp.user_playlist_add_tracks(user_id, playlist_id, tracks)

def get_token():
    token_info = session.get(TOKEN_INFO)
    if not token_info:
        # If the token info is not found, redirect the user to the login
        return redirect(url_for('login'))

    # Check if the token is expired and refresh it if needed
    now = int(time.time())

    is_expired = token_info.get('expires_at',0) - now < 60
    if(is_expired):
        spotify_oauth = create_spotify_oauth()
        try:
            token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
            session[TOKEN_INFO] = token_info  # Save the refreshed token back to the session

        except Exception as e:
            print(f"Error refreshing token: {e}")
            return redirect(url_for('login'))

    return token_info.get('access_token')


def create_spotify_oauth():
    return SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope=SCOPE)

def get_last_run_time():
    """Get the last time the script was run from a file."""
    try:
        with open(LAST_RUN_FILE, "r") as f:
            return datetime.datetime.strptime(f.read(), "%Y-%m-%dT%H:%M:%SZ")
    except FileNotFoundError:
        return datetime.datetime.min

def update_last_run_time():
    """Update the last run time in a file."""
    with open(LAST_RUN_FILE, "w") as f:
        f.write(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))

if __name__ == '__main__':
    app.run(debug=True)
