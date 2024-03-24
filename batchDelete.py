import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".batch_del_env")

# Spotify API credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECTURI")

# Define the needed scope
SCOPE = "playlist-read-private,playlist-read-collaborative,playlist-modify-private,playlist-modify-public"

# Pattern to match "Month Year"
pattern = re.compile("^(January|February|March|April|May|June|July|August|September|October|November|December) \d{4}$")

def authenticate_spotify():
    """Authenticate with Spotify and return a Spotipy client instance."""
    auth_manager = SpotifyOAuth(client_id=CLIENT_ID,
                                client_secret=CLIENT_SECRET,
                                redirect_uri=REDIRECT_URI,
                                scope=SCOPE)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp

def delete_month_year_playlists(sp):
    """Delete all playlists that match the 'Month Year' pattern."""
    # Get current user's playlists
    playlists = sp.current_user_playlists()
    while playlists:
        for playlist in playlists['items']:
            # Check if playlist name matches the pattern
            if pattern.match(playlist['name']):
                print(f"Deleting playlist: {playlist['name']}")
                # Delete playlist
                sp.current_user_unfollow_playlist(playlist['id'])
                
        # Fetch next set of playlists if available
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    print("Finished deleting matching playlists.")

if __name__ == "__main__":
    sp_client = authenticate_spotify()
    delete_month_year_playlists(sp_client)
