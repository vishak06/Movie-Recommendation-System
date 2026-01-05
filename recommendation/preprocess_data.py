import pandas as pd
import pickle
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_data():
    """Generate preprocessed similarity data from CSV file."""
    
    csv_path = 'recommendation/static/recommendation/final_movies.csv'
    pkl_path = 'recommendation/static/recommendation/preprocessed_data.pkl'
    
    print("Starting preprocessing...")
    print(f"Loading data from {csv_path}...")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at {csv_path}")
    
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} movies")

    print("Filling missing values...")
    for col in ['title', 'release_date', 'original_language', 'overview', 'genres', 'cast', 'director', 'imdb_rating', 'poster_path']:
        if col in df.columns:
            df[col] = df[col].fillna('')

    print("Creating combined features...")
    combined = df['genres'] + ' ' + df['overview'] + ' ' + df['original_language'] + ' ' + df['cast'] + ' ' + df['director']

    print("Vectorizing features (this may take a while)...")
    vectorizer = TfidfVectorizer(max_features=5000)  # Limit features to reduce memory
    feature_vectors = vectorizer.fit_transform(combined)

    print("Computing similarity in batches to save memory...")
    # Compute similarities in batches to avoid memory issues
    top_k = 50
    batch_size = 1000
    n_movies = feature_vectors.shape[0]
    optimized_similarity = []
    
    for start_idx in range(0, n_movies, batch_size):
        end_idx = min(start_idx + batch_size, n_movies)
        print(f"  Processing movies {start_idx} to {end_idx} of {n_movies}...")
        
        # Compute similarity for this batch against all movies
        batch_similarity = cosine_similarity(
            feature_vectors[start_idx:end_idx], 
            feature_vectors
        ).astype('float32')
        
        # For each movie in batch, keep only top K similar movies
        for i in range(batch_similarity.shape[0]):
            sim_scores = batch_similarity[i]
            top_indices = np.argpartition(sim_scores, -top_k)[-top_k:]
            top_indices = top_indices[np.argsort(-sim_scores[top_indices])]
            top_scores = sim_scores[top_indices]
            optimized_similarity.append((top_indices, top_scores))

    # Ensure directory exists
    os.makedirs(os.path.dirname(pkl_path), exist_ok=True)
    
    print(f"Saving preprocessed data to {pkl_path}...")
    with open(pkl_path, 'wb') as f:
        pickle.dump({
            'df': df[['title', 'release_date', 'original_language', 'overview', 'genres', 'cast', 'director', 'imdb_rating', 'poster_path']],
            'similarity': optimized_similarity
        }, f)

    print("✓ Preprocessing complete! Data saved successfully.")
    return True

if __name__ == '__main__':
    try:
        preprocess_data()
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        exit(1)
