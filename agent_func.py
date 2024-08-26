import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances
from config import *

""" CAN BE EDITED TO RETURN MORE ARTISTS """
def playlist_recommendations(song_name, amount=5): 
    if song_name not in music_df['Track Name'].values:
        print(f"'{song_name}' is not here, please see if you have the exact spelling of the song.")
        return
    
    scaler = MinMaxScaler()
    music_features = music_df[['Danceability', 'Energy', 'Key', 
                           'Loudness', 'Mode', 'Speechiness', 'Acousticness',
                           'Instrumentalness', 'Liveness', 'Valence', 'Tempo']].values
    music_features_scaled = scaler.fit_transform(music_features)

    # Calculate the similarity scores based on music features using pairwise distances#
    song_index = music_df[music_df['Track Name'] == song_name].index[0]
    similarity_scores = 1 - pairwise_distances([music_features_scaled[song_index]], music_features_scaled, metric='cosine')

    # Get the indices of the most similar songs then,
    # Get the names of the most similar songs based on content-based filtering
    # Get the popularity score of the input song
    similar_song_indices = similarity_scores.argsort()[0][::-1][1:amount + 1] 
    content_based_recommendations = music_df.loc[similar_song_indices][['Track Name', 'Artists', 'Album Name', 'Popularity']]

    # Create a DataFrame for the input song
    input_song_data = {
        'Track Name': [song_name],
        'Artists': [music_df.loc[music_df['Track Name'] == song_name, 'Artists'].values[0]],
        'Album Name': [music_df.loc[music_df['Track Name'] == song_name, 'Album Name'].values[0]],
        'Popularity': music_df.loc[music_df['Track Name'] == song_name, 'Popularity'].values[0]
    }
    input_song_df = pd.DataFrame(input_song_data)

    # Concatenate the input song DataFrame with content-based recommendations#
    # Sort the hybrid recommendations based on weighted popularity score
    playlist_recommendations = pd.concat([content_based_recommendations, input_song_df], ignore_index=True)
    playlist_recommendations = playlist_recommendations.sort_values(by='Popularity', ascending=False)
    playlist_recommendations = playlist_recommendations[playlist_recommendations['Track Name'] != song_name]

    return playlist_recommendations


