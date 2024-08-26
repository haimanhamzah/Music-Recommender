# This file contains all the different intel agents doing 
# An agent to take the playlist and music listened from a user
# An agent that's going to recommmend music based on collaborative filtering
# 

from recommender import *
import pandas as pd

class UserAgent:
    def __init__(self, user_id):
        self.user_id = user_id
        self.playlists = []
        self.tracks = []
        self.play_counts = {}

    def fetch_user_data(self, spotify_utils):
        """
        Fetch user playlists and tracks from Spotify API.
        """
        self.playlists = spotify_utils.get_user_playlists(self.user_id)
        for playlist in self.playlists:
            tracks = spotify_utils.get_playlist_tracks(playlist)
            self.tracks.extend(tracks)

        # Calculate play counts (example, you can use a different approach)
        for track in self.tracks:
            self.play_counts[track] = self.play_counts.get(track, 0) + 1

    def get_user_data(self):
        """
        Return user's interaction data as a pandas DataFrame.
        """
        user_data = []
        for track, count in self.play_counts.items():
            user_data.append({'user_id': self.user_id, 'track_id': track, 'play_count': count})
        return pd.DataFrame(user_data)

class RecommendationAgent:
    def __init__(self, user_data):
        self.user_data = user_data
        self.collaborativeFilter = CollaborativeFilter(user_data)
        self.collaborativeFilter.create_user_item_matrix()
        self.collaborativeFilter.create_item_item_matrix()

    def recommend_tracks(self, user_id, num_recommendations=10):
        """
        Recommend tracks to a user based on collaborative filtering.
        """
        track_ids = self.collaborativeFilter.recommend_items(user_id, num_recommendations)
        return track_ids

class ExplorationAgent:
    def __init__(self, spotify_utils):
        self.spotify_utils = spotify_utils

    def explore_tracks(self, seed_tracks, num_recommendations=10):
        """
        Suggest diverse and serendipitous recommendations based on seed tracks.
        """
        # Use Spotify API's recommendation engine (example)
        recommendations = self.spotify_utils.sp.recommendations(seed_tracks=seed_tracks,
                                                                limit=num_recommendations)
        recommended_tracks = [track['id'] for track in recommendations['tracks']]
        return recommended_tracks

class ExplanationAgent:
    def __init__(self, spotify_utils):
        self.spotify_utils = spotify_utils

    def explain_recommendation(self, track_id):
        """
        Provide an explanation or justification for a recommended track.
        """
        # Fetch track information from Spotify API
        track = self.spotify_utils.sp.track(track_id)
        artist = track['artists'][0]['name']
        album = track['album']['name']
        features = self.spotify_utils.get_track_features([track_id])[0]

        # Example explanation based on audio features
        explanation = f"The track '{track['name']}' by {artist} from the album '{album}' is recommended because it has a danceability of {features['danceability']}, energy of {features['energy']}, and valence of {features['valence']}, which aligns with your preferences."

        return explanation

class EvaluationAgent:
    def __init__(self):
        self.user_ratings = {}

    def collect_feedback(self, user_id, track_id, rating):
        """
        Collect user feedback and ratings for recommended tracks.
        """
        self.user_ratings.setdefault(user_id, {})[track_id] = rating

    def evaluate_recommendations(self, user_id):
        """
        Evaluate the performance of recommendations for a user.
        """
        # Calculate evaluation metrics (example: precision)
        user_ratings = self.user_ratings[user_id]
        num_recommended = len(user_ratings)
        num_liked = sum(rating > 3 for rating in user_ratings.values())
        precision = num_liked / num_recommended if num_recommended > 0 else 0

        return precision
    
if __name__ == "__main__":
    UserAgent()

