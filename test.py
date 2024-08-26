"""This was a test development beforehand on an idea i originally had - Explained in report"""


# import pandas as pd
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.model_selection import train_test_split
# from sklearn.decomposition import TruncatedSVD
# import tkinter as tk
# from tkinter import simpledialog

# # Load the dataset
# data = pd.read_csv('dataset.csv', chunksize=5000)

# # Preprocessing
# # Assume the data has columns 'track_id', 'track_name', 'artist', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'valence', 'tempo', 'user_id', 'rating'

# # Feature Engineering for content-based filtering
# content_features = data[['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'valence', 'tempo']]
# content_features = content_features.astype(float)

# # Compute cosine similarity matrix for content-based recommendation
# cosine_sim = cosine_similarity(content_features, content_features)

# # Collaborative Filtering using Matrix Factorization
# ratings_matrix = data.pivot_table(index='user_id', columns='track_id', values='rating').fillna(0)
# X = ratings_matrix.values
# SVD = TruncatedSVD(n_components=50, random_state=17)
# matrix_transformed = SVD.fit_transform(X)
# corr = np.corrcoef(matrix_transformed)

# track_id_list = ratings_matrix.columns
# track_id_index = {track_id: i for i, track_id in enumerate(track_id_list)}

# # Function to get content-based recommendations
# def content_based_recommendations(track_name, data, cosine_sim):
#     try:
#         target_index = data[data['track_name'] == track_name].index[0]
#         sim_scores = list(enumerate(cosine_sim[target_index]))
#         sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#         sim_scores = sim_scores[1:11]
#         track_indices = [i[0] for i in sim_scores]
#         return data['track_name'].iloc[track_indices]
#     except:
#         return "Track not found."

# # Function to get collaborative recommendations
# def collaborative_recommendations(track_id):
#     try:
#         index = track_id_index[track_id]
#         corr_scores = list(enumerate(corr[index]))
#         corr_scores = sorted(corr_scores, key=lambda x: x[1], reverse=True)
#         corr_scores = corr_scores[1:11]
#         track_indices = [i[0] for i in corr_scores]
#         recommended_track_ids = track_id_list[track_indices]
#         return data[data['track_id'].isin(recommended_track_ids)]['track_name'].unique()
#     except:
#         return "Track not found."

# # GUI
# def main_app_window():
#     window = tk.Tk()
#     window.title("Music Recommender System")
    
#     def get_recommendations():
#         track_name = simpledialog.askstring("Input", "Enter a track name for recommendations:")
#         recommendations = content_based_recommendations(track_name, data, cosine_sim)
#         result_label.config(text="Recommendations: \n" + "\n".join(recommendations))
    
#     tk.Label(window, text="Welcome to the Music Recommender!").pack()
#     tk.Button(window, text="Get Recommendations", command=get_recommendations).pack()
#     result_label = tk.Label(window, text="")
#     result_label.pack()
    
#     window.mainloop()

# if __name__ == "__main__":
#     main_app_window()
