# In recommendation.py

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def content_based_recommendation(input_features, df, top_n=5):
    # Ensure input_features is a 2D array with shape (1, num_features)
    input_features = np.array(input_features).reshape(1, -1)

    # Extract audio features of all songs from the DataFrame
    all_audio_features = df[['danceability', 'valence', 'liveness', 'energy']].values

    # Calculate similarity scores using cosine similarity
    similarity_scores = cosine_similarity(input_features, all_audio_features)

    # Get indices of songs in descending order of similarity scores
    similar_songs_indices = np.argsort(similarity_scores[0])[::-1]

    # Remove the input song itself from the list of similar songs
    similar_songs_indices = similar_songs_indices[1:]

    # Select top N songs
    top_n_songs = df.iloc[similar_songs_indices[:top_n]]

    return top_n_songs
