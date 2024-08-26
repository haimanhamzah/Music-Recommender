""" THIS FILE IS NOT USED AS IT IS ORIGINALLY AN IDEA I HAD - EXPLAINED IN THE REPORT """

# This is where the recommendation for collaborative filtering will go 
# import pandas as pd
# from sklearn.metrics import pairwise_distances

# class CollaborativeFilter:
#     def __init__(self, data):
#         self.data = data
#         self.user_item_matrix = None
#         self.item_item_matrix = None
#         self.user_item_df = None

#     def create_user_item_matrix(self):
#         """
#         Create a user-item matrix from the interaction data.
#         """
#         self.user_item_df = self.data.pivot_table(index='user_id',
#                                                    columns='track_id',
#                                                    values='play_count',
#                                                    fill_value=0)
#         self.user_item_matrix = self.user_item_df.values

    # def create_item_item_matrix(self):
    #     """
    #     Create an item-item similarity matrix using cosine similarity.
    #     """
    #     self.item_item_matrix = 1 - pairwise_distances(self.user_item_matrix.T, metric="cosine")

    # def recommend_items(self, user_data, num_recommendations=10):
    #     """
    #     Recommend items to a user based on item-item collaborative filtering.
    #     """
    #     # Get the user's item interactions
    #     user_interactions = self.user_item_df.loc[user_data, :]

    #     # Calculate the weighted average of similar items
    #     item_scores = self.item_item_matrix.dot(user_interactions)

    #     # Sort the item scores in descending order
    #     item_scores = item_scores.sort_values(ascending=False)

    #     # Filter out items the user has already interacted with
    #     recommended_items = item_scores[user_interactions == 0].index[:num_recommendations]

    #     return recommended_items

