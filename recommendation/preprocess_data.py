import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_data():
    """Generate preprocessed similarity data from CSV file."""
    
    csv_path = 'recommendation/static/recommendation/moviesdb.csv'
    pkl_path = 'recommendation/static/recommendation/preprocessed_data.pkl'
    
    print("Starting preprocessing...")
    print(f"Loading data from {csv_path}...")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at {csv_path}")
    
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} movies")

    print("Filling missing values...")
    for col in ['title', 'genres', 'overview', 'language', 'poster_path', 'release_date', 'vote_average', 'cast', 'director']:
        if col in df.columns:
            df[col] = df[col].fillna('')

    print("Creating combined features...")
    combined = df['genres'] + ' ' + df['overview'] + ' ' + df['language'] + ' ' + df['cast'] + ' ' + df['director']

    print("Vectorizing features (this may take a while)...")
    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined)

    print("Computing similarity matrix...")
    # Use float32 to save memory
    similarity = cosine_similarity(feature_vectors).astype('float32')
    
    # Store only top 100 similar movies per movie to save memory
    print("Optimizing similarity data (keeping top 100 per movie)...")
    top_k = 100
    optimized_similarity = []
    
    for i in range(len(similarity)):
        # Get indices of top similar movies
        sim_scores = similarity[i]
        top_indices = sim_scores.argsort()[-top_k:][::-1]
        top_scores = sim_scores[top_indices]
        optimized_similarity.append((top_indices, top_scores))

    # Ensure directory exists
    os.makedirs(os.path.dirname(pkl_path), exist_ok=True)
    
    print(f"Saving preprocessed data to {pkl_path}...")
    with open(pkl_path, 'wb') as f:
        pickle.dump({
            'df': df[['title', 'genres', 'overview', 'release_date', 'vote_average', 'poster_path']],
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
