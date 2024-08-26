"""
This file is used to do matrix factorization
It consists of pre processing on the dataset such as cleaning and etc.
scaling and normalization of audio features is a must as well
considering we're doing a relationship between different users and other users
as well as the amount of times they've listened. we can use that to create a whole different algorithm for nn
simple train test and push through a collaborative filtering method

"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from fuzzywuzzy import fuzz
from scipy.sparse import csr_matrix
from sklearn.model_selection import train_test_split


def matrix_factorisation():
    #read million song subset based on user interaction
    initial_song = pd.read_csv('10000.txt', sep='\t', header=None)
    initial_song.columns = ['user_id', 'song_id', 'listen_count']

    #song metadata
    metadata_song = pd.read_csv('song_data.csv')
    metadata_song.drop_duplicates(['song_id'], inplace=True)

    #merge together 
    initial_metadata = pd.merge(initial_song, metadata_song, on="song_id", how="left")

    #convert to csv file
    initial_metadata.to_csv('song_dataset.csv', index=False)

    # Load and preprocess data
    data = pd.read_csv('song_dataset.csv')
    print(data.head())
    #train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

    #Drops the columns with missing values in the 4 columns that we want to return to get priority

    if data['user_id'].isnull().sum() > 0:
        data = data.dropna(axis=0, subset=["user_id"])
    elif data['song_id'].isnull().sum() > 0:
        data = data.dropna(axis=0, subset=["song_id"])
    elif data['title'].isnull().sum() > 0:
        data = data.dropna(axis=0, subset=["title"])
    elif data['listen_count'].isnull().sum() > 0:
        data = data.dropna(axis=0, subset=["listen_count"])
    elif data['artist_name'].isnull().sum() > 0:
        data = data.dropna(axis=0, subset=["artist_name"])

    most_famous_song = (data.groupby(by=["title"])["listen_count"].count().reset_index().rename(columns = {"listen_count": "total_listen_count"})[['title', 'total_listen_count']])
    print(most_famous_song.head())

    data_update1 = data.merge(most_famous_song, left_on = "title", right_on="title", how = "left")
    #print(data_update1.head())

    most_famous_artist = (data_update1.groupby(by=["artist_name"])["listen_count"].count().reset_index().rename(columns = {"listen_count": "total_artist_listen_count"})[['artist_name', 'total_artist_listen_count']])
    print(most_famous_artist.head())

    data_update2 = data_update1.merge(most_famous_artist, left_on = "artist_name", right_on="artist_name", how = "left")
    #print(data_update2.head()) 

    #gets the description of the total listen count
    print(data_update2['total_listen_count'].describe())
    #considering average is 247 listens per song
    #this dataset is huge, hence to avoid noise, only take in the top 30% of the dataset

    upper_quartile = 6000
    data_update3 = data_update2.query('total_listen_count >= @upper_quartile')
    print(data_update3.head())

    if not data_update3[data_update3.duplicated(['title', 'user_id'])].empty:
        data_update3 = data_update3.drop_duplicates(['title', 'user_id'])

    recommended_tracks = data_update3.pivot(index="title", columns="user_id", values="listen_count").fillna(0)
    recommended_tracks_binary = recommended_tracks.apply(np.sign)
    matrix_recommended_tracks_binary = csr_matrix(recommended_tracks_binary.values)
    
    def recommend_songs(user_id, num_recommendations=10):
        # Get the user's listened songs
        user_songs = data_update3[data_update3['user_id'] == user_id]['title'].tolist()
        
        # Calculate the cosine similarity between the user's songs and all songs
        user_songs_indices = recommended_tracks.index.isin(user_songs)
        user_songs_matrix = matrix_recommended_tracks_binary[user_songs_indices]
        cosine_sim = 1 - pairwise_distances(user_songs_matrix, matrix_recommended_tracks_binary, metric="cosine")
        
        # Get the top similar songs based on cosine similarity
        similar_songs_indices = cosine_sim.argsort()[0][-num_recommendations:][::-1]
        similar_songs = recommended_tracks.index[similar_songs_indices].tolist()
        
        # Perform fuzzy matching to find the closest matching songs
        matched_songs = []
        for song in similar_songs:
            if song not in user_songs:
                match_ratio = max(fuzz.ratio(song.lower(), user_song.lower()) for user_song in user_songs)
                if match_ratio >= 15:  # Adjust the threshold as needed
                    matched_songs.append(song)
        
        return matched_songs
    
    user_id = 'b80344d063b5ccb3212f76538f3d9e43d87dca9e'
    recommended_songs = recommend_songs(user_id)
    print(f"Recommended songs for user {user_id}:")
    for song in recommended_songs:
        print(song)



# Create utility matrix
# utility_matrix = data.pivot_table(index='user_id', columns='song_id', values='listen_count', fill_value=0)
# utility_matrix = utility_matrix.values
# train_utility, test_utility = train_test_split(utility_matrix, test_size=0.2, random_state=42)

# # Define model architecture
# num_users = len(data['user_id'].unique())
# num_items = len(data['song_id'].unique())
# embedding_size = 50

# user_input = Input(shape=(1,), name='user_input')
# item_input = Input(shape=(1,), name='item_input')

# user_embedding = Embedding(num_users, embedding_size, name='user_embedding')(user_input)
# item_embedding = Embedding(num_items, embedding_size, name='item_embedding')(item_input)

# user_embedded = Flatten()(user_embedding)
# item_embedded = Flatten()(item_embedding)

# concatenated = Concatenate()([user_embedded, item_embedded])

# dense1 = Dense(128, activation='relu')(concatenated)
# dense2 = Dense(64, activation='relu')(dense1)
# output = Dense(1, activation='linear', name='output')(dense2)

# model = Model(inputs=[user_input, item_input], outputs=output)
# model.compile(loss=MeanSquaredError())

# # Train the model
# model.fit([train_data['user_id'], train_data['song_id']], train_utility, epochs=10, batch_size=64, validation_data=([test_data['user_id'], test_data['song_id']], test_utility))

# # Evaluate the model
# test_mse = model.evaluate([test_data['user_id'], test_data['song_id']], test_utility)
# print(f'Test MSE: {test_mse}')

# Generate recommendations
# def recommend_songs(user_id, topn=10):
#     user_ids = np.repeat(user_id, num_items)
#     item_ids = np.arange(num_items)
    
#     user_item_pairs = [user_ids, item_ids]
#     predictions = model.predict(user_item_pairs)
    
#     top_indices = predictions.argsort()[-topn:][::-1]
#     recommended_items = item_ids[top_indices]
    
#     return recommended_items

# # Example usage
# user_id = 42
# recommended_songs = recommend_songs(user_id)
# print(f'Recommended songs for user {user_id}:')
# for song_id in recommended_songs:
#     song_info = data.loc[data['song_id'] == song_id, ['title', 'artist_name']].values[0]
#     print(f"{song_info[0]} by {song_info[1]}")