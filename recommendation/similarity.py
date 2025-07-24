import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('recommendation/static/recommendation/moviesdb.csv')

for col in ['title' ,'genres', 'overview', 'language', 'poster_path', 'release_date', 'vote_average', 'cast', 'director']:
    df[col] = df[col].fillna('')

combined = df['genres'] + ' ' + df['overview'] + ' ' + df['language'] + ' ' + df['cast'] + ' ' + df['director']

vectorizer = TfidfVectorizer()

feature_vectors = vectorizer.fit_transform(combined)

similarity = cosine_similarity(feature_vectors)

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