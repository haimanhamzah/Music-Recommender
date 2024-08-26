from sklearn.preprocessing import MinMaxScaler
import requests
import base64
from agent_utils import *

"""THIS IS WHERE I SET UP MY ENVIRONMENT, THE TOP PART OF THE CODE IS TAKEN FROM SPOTIPY DOCUMENTATION HENCE IT IS NOT MY OWN WORK"""
"""THIS SECTION JUST UTILIZES THE SPOTIFY WEB API CONNECTION, WHERE MY AGENTS ARE BUILT ON."""
"""I WILL LINK THE OFFICIAL DOCUMENTATION AND OFFICIAL SPOTIPY VIDEO THAT COINCIDES WITH THIS CONNECTION"""

# Replace with your own Client ID and Client Secret
CLIENT_ID = 'cefb820f69584936affacbc094f83dbe'
CLIENT_SECRET = '967d1466ea6440859ffd14393468e0a5'

# Base64 encode the client ID and client secret
client_credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
client_credentials_base64 = base64.b64encode(client_credentials.encode())

# Request the access token
token_url = 'https://accounts.spotify.com/api/token'
headers = {
    'Authorization': f'Basic {client_credentials_base64.decode()}'
}
data = {
    'grant_type': 'client_credentials'
}
response = requests.post(token_url, data=data, headers=headers)

if response.status_code == 200:
    access_token = response.json()['access_token']
    print("Access token obtained successfully.")
else:
    print("Error obtaining access token.")
    exit()

""" THIS IS WHERE YOU INPUT THE PLAYLIST ID AND ARTIST RELATED ID """

""" TO GET PLAYLIST ID -> GO ON TO SPOTIFY -> CLICK ON A PLAYLIST -> CLICK ON THE '...' ICON -> CLICK ON SHARE -> EMBED PLAYLIST -> SHOW CODE"""

""" TAKE THE FINAL STRING IN SRC - e.g. src="https://open.spotify.com/embed/playlist/37i9dQZF1EQoqCH7BwIYb7? -> 37i9dQZF1EQoqCH7BwIYb7 """

""" SAME GOES FOR ARTIST_ID -> GO TO ARTIST INSTEAD OF PLAYLIST """

playlist_id = '1Lev74dTiJ9FJHiPapPl7y' 
artist_related_id = '25jJ6vyXwTRa0e6XCcdR6U'

# Call the function to get the music data from the playlist and store it in a DataFrame
music_df = get_playlist_data(playlist_id, access_token)
music_df1 = get_artists_similarities(artist_related_id, access_token)

# data = music_df
# data1 = music_df1

