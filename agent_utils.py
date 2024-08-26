import json
import pandas as pd
import spotipy

def get_playlist_data(playlist_id, access_token):
    spotify = spotipy.Spotify(auth=access_token)
    
    fields = 'items(track(id,name,artists,album(id,name)))'
    playlist_data = spotify.playlist_tracks(playlist_id, fields=fields)
    #print(json.dumps(playlist_data, sort_keys=True, indent=4))
    
    tracks_list = []
    for item in playlist_data['items']:
        track_details = item['track']
        track_name = track_details['name']
        artist_names = ', '.join(artist['name'] for artist in track_details['artists'])
        album_details = track_details['album']
        album_name = album_details['name']
        album_identifier = album_details['id']
        track_identifier = track_details['id']

        audio_features = spotify.audio_features(track_identifier)[0] if track_identifier else None
        
        album_data = spotify.album(album_identifier) if album_identifier else None
        album_release_date = album_data.get('release_date') if album_data else None

        track_data = spotify.track(track_identifier) if track_identifier else None
        track_popularity = track_data.get('popularity') if track_data else None

        tracks_list.append({
            'Track Name': track_name,
            'Artists': artist_names,
            'Album Name': album_name,
            'Album ID': album_identifier,
            'Track ID': track_identifier,
            'Popularity': track_popularity,
            'Release Date': album_release_date,
            'Duration (ms)': audio_features.get('duration_ms', None) if audio_features else None,
            'Explicit': track_details.get('explicit', None),
            'Spotify URL': track_details.get('external_urls', {}).get('spotify', None),
            'Danceability': audio_features.get('danceability', None) if audio_features else None,
            'Energy': audio_features.get('energy', None) if audio_features else None,
            'Key': audio_features.get('key', None) if audio_features else None,
            'Loudness': audio_features.get('loudness', None) if audio_features else None,
            'Mode': audio_features.get('mode', None) if audio_features else None,
            'Speechiness': audio_features.get('speechiness', None) if audio_features else None,
            'Acousticness': audio_features.get('acousticness', None) if audio_features else None,
            'Instrumentalness': audio_features.get('instrumentalness', None) if audio_features else None,
            'Liveness': audio_features.get('liveness', None) if audio_features else None,
            'Valence': audio_features.get('valence', None) if audio_features else None,
            'Tempo': audio_features.get('tempo', None) if audio_features else None,
        })

    return pd.DataFrame(tracks_list)


def get_artists_similarities(artist_related_id, access_token):
    # Set up Spotipy with the access token
    sp = spotipy.Spotify(auth=access_token)

    #Get the artists similar to the related artists
    sp_artist_similar = sp.artist_related_artists(artist_related_id)
    #print(json.dumps(sp_artist_similar, sort_keys=True, indent=4))
    artist_all = sp_artist_similar['artists']

    sim_artist = []
    for i in artist_all: 
        artists_name = i['name']
        genres = i['genres']
        artist_id  = i['id']
        popularity = i['popularity']

        similar_artist_data = {
            "Artist": artists_name,
            "Genres": genres,
            "Artist ID": artist_id,
            "Popularity": popularity
        }

        sim_artist.append(similar_artist_data)

    #Returns the first 5 artist based on popularity
    df1 = pd.DataFrame(sim_artist)
    df1 = df1.sort_values(by='Popularity', ascending=False)
    df1 = df1.head(5)

    return(df1)
        

