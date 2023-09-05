from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def content_based_recommendation(input_features, df, top_n, songs_already_recommended=[]):
    input_features = np.array(input_features).reshape(1, -1)

    all_audio_features = df[['danceability', 'valence', 'liveness', 'energy']].values

    similarity_scores = cosine_similarity(input_features, all_audio_features)

    similar_songs_indices = np.argsort(similarity_scores[0])[::-1]
    similar_songs_indices = similar_songs_indices[1:]

    recommended_songs = []
    for index in similar_songs_indices:
        track_id = df.iloc[index]['track_id']
        track_name = df.iloc[index]['track_name']
        if track_id not in songs_already_recommended and track_name not in [song['track_name'] for song in recommended_songs]:
            recommended_songs.append(df.iloc[index])
            songs_already_recommended.append(track_id)
            if len(recommended_songs) >= top_n:
                break

    return recommended_songs
