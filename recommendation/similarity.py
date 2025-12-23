import pandas as pd
import difflib
import pickle
import os

# Load preprocessed data
preprocessed_path = 'recommendation/static/recommendation/preprocessed_data.pkl'

if not os.path.exists(preprocessed_path):
    print("Preprocessed data not found. Generating it now...")
    try:
        from .preprocess_data import preprocess_data
        preprocess_data()
        print("Preprocessing complete!")
    except Exception as e:
        raise FileNotFoundError(
            f"Preprocessed data not found at {preprocessed_path}. "
            f"Attempted to generate it but failed: {e}. "
            "Please run 'python recommendation/preprocess_data.py' manually."
        )

with open(preprocessed_path, 'rb') as f:
    data = pickle.load(f)
    df = data['df']
    similarity = data['similarity']

def movie_recommendation(movie_name, number=10):
    list_of_titles = [title.lower() for title in df['title'].tolist()]
    find_close_match = difflib.get_close_matches(movie_name, list_of_titles, n=10, cutoff=0.3)

    if not find_close_match:
        return {}
    
    close_match = find_close_match[0]
    movie_index = df[df['title'].str.lower() == close_match].index[0]
    similarity_score = list(enumerate(similarity[movie_index]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    recommendations = []
    for i in range(number):
        index = sorted_similar_movies[i][0]
        movie = df.iloc[index]
        recommendations.append([
            movie['title'],
            movie['genres'],
            movie['overview'],
            movie['release_date'],
            round(movie['vote_average'],2),
            movie['poster_path']
        ])

    return recommendations