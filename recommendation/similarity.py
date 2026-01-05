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

def get_movie_suggestions(query, limit=5):
    """
    Get movie suggestions based on user query for autocomplete
    Returns a list of dictionaries with title and poster_path
    """
    if not query or len(query) < 1:
        return []
    
    # Filter movies where title contains the query (case insensitive)
    query_lower = query.lower()
    matching_movies = df[df['title'].str.lower().str.contains(query_lower, na=False, regex=False)]
    
    # If no direct matches, use fuzzy matching
    if len(matching_movies) == 0:
        list_of_titles = [title.lower() for title in df['title'].tolist()]
        find_close_match = difflib.get_close_matches(query_lower, list_of_titles, n=limit*3, cutoff=0.3)
        
        if find_close_match:
            matching_movies = df[df['title'].str.lower().isin(find_close_match)]
    
    # Get unique movies, limit results
    suggestions = []
    seen = set()
    
    for idx, movie in matching_movies.iterrows():
        # Create a unique key based on title and release date
        unique_key = (movie['title'].lower(), str(movie['release_date']))
        
        if unique_key not in seen and len(suggestions) < limit:
            seen.add(unique_key)
            # Extract year from release_date
            year = movie['release_date'].split('-')[0] if movie['release_date'] and '-' in str(movie['release_date']) else ''
            # Create full title with year for internal use
            full_title = f"{movie['title']} ({year})" if year else movie['title']
            
            # Format release_date to dd-mm-yyyy
            formatted_date = ''
            if movie['release_date'] and '-' in str(movie['release_date']):
                parts = movie['release_date'].split('-')
                if len(parts) == 3:
                    formatted_date = f"{parts[2]}-{parts[1]}-{parts[0]}"
                else:
                    formatted_date = movie['release_date']
            else:
                formatted_date = movie['release_date']
            
            suggestions.append({
                'title': movie['title'],  # Display title without year
                'full_title': full_title,  # Full title with year for matching
                'poster_path': movie['poster_path'],
                'release_date': formatted_date,
                'index': int(idx)  # Include dataframe index
            })
    
    return suggestions

def movie_recommendation(movie_name, number=10, movie_index=None):
    # If movie_index is provided, use it directly
    if movie_index is not None:
        try:
            movie_index = int(movie_index)
            # Verify the index exists in the dataframe
            if movie_index not in df.index:
                movie_index = None
        except (ValueError, TypeError):
            movie_index = None
    
    # If no valid index provided, search by movie name
    if movie_index is None:
        # Check if movie_name includes year in format "Title (Year)"
        import re
        match = re.match(r'^(.+?)\s*\((\d{4})\)$', movie_name)
        
        if match:
            # Extract title and year
            title_only = match.group(1).strip()
            year = match.group(2)
            
            # Find movie matching both title and year
            matching_movies = df[
                (df['title'].str.lower() == title_only.lower()) & 
                (df['release_date'].str.startswith(year))
            ]
            
            if len(matching_movies) > 0:
                movie_index = matching_movies.index[0]
            else:
                # Fallback to just title match
                movie_index = df[df['title'].str.lower() == title_only.lower()].index[0]
        else:
            # Original logic for title-only search
            list_of_titles = [title.lower() for title in df['title'].tolist()]
            find_close_match = difflib.get_close_matches(movie_name.lower(), list_of_titles, n=10, cutoff=0.3)

            if not find_close_match:
                return {}
            
            close_match = find_close_match[0]
            movie_index = df[df['title'].str.lower() == close_match].index[0]
    
    # Get precomputed similar movies
    if isinstance(similarity, list):
        # Optimized format: list of (indices, scores) tuples
        top_indices, top_scores = similarity[movie_index]
        similarity_score = list(zip(top_indices, top_scores))
    else:
        # Legacy format: full similarity matrix
        similarity_score = list(enumerate(similarity[movie_index]))
        similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    recommendations = []
    count = 0
    for index, score in similarity_score:
        if count >= number:
            break
        movie = df.iloc[index]
        # Convert imdb_rating to float, handle empty strings
        try:
            rating = round(float(movie['imdb_rating']), 2) if movie['imdb_rating'] else 0.0
        except (ValueError, TypeError):
            rating = 0.0
        
        # Format release_date to dd-mm-yyyy
        formatted_date = ''
        if movie['release_date'] and '-' in str(movie['release_date']):
            parts = str(movie['release_date']).split('-')
            if len(parts) == 3:
                formatted_date = f"{parts[2]}-{parts[1]}-{parts[0]}"
            else:
                formatted_date = movie['release_date']
        else:
            formatted_date = movie['release_date']
        
        recommendations.append([
            movie['title'],
            movie['genres'],
            movie['overview'],
            formatted_date,
            rating,
            movie['poster_path'],
            int(index)  # Add the dataframe index
        ])
        count += 1

    return recommendations