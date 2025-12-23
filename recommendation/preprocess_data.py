import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading data...")
df = pd.read_csv('recommendation/static/recommendation/moviesdb.csv')

print("Filling missing values...")
for col in ['title', 'genres', 'overview', 'language', 'poster_path', 'release_date', 'vote_average', 'cast', 'director']:
    df[col] = df[col].fillna('')

print("Creating combined features...")
combined = df['genres'] + ' ' + df['overview'] + ' ' + df['language'] + ' ' + df['cast'] + ' ' + df['director']

print("Vectorizing features...")
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined)

print("Computing similarity matrix...")
similarity = cosine_similarity(feature_vectors)

print("Saving preprocessed data...")
with open('recommendation/static/recommendation/preprocessed_data.pkl', 'wb') as f:
    pickle.dump({
        'df': df,
        'similarity': similarity
    }, f)

print("Preprocessing complete! Data saved to preprocessed_data.pkl")
