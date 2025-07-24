# Movie Recommendation System

This is a **Movie Recommendation Web Application** built using **Django** for the backend and **HTML, CSS, Bootstrap** for the frontend. The project uses a preprocessed Kaggle dataset to recommend similar movies based on a user’s input title.

## Overview

The goal of this project is to create a system where users can input a movie name, and the application will return a list of similar movies. The recommendations are generated using content-based filtering methods such as cosine similarity and TF-IDF vectorization. These techniques compare the textual features (like genres, keywords, overview, etc.) of the input movie with others in the dataset to find the most similar ones.

The application begins by processing a Kaggle movie dataset, where each movie's features are combined into a single string and converted into numerical vectors using TF-IDF. Then, cosine similarity is calculated between all movie vectors to identify and rank the most similar movies. This ensures that the recommendations are not random, but actually relevant to the content of the selected movie.

Once a user enters a movie title on the site, the app retrieves the top similar movies based on the similarity scores and displays them in an organized format. Each recommended movie title is also linked to a Google search page, allowing users to explore more details, trailers, or streaming platforms directly from the app.

This system is especially useful for users who are looking to discover new movies similar to the ones they already love. It can be easily expanded or enhanced in the future to include ratings, genres, or even collaborative filtering techniques to improve the recommendations.

## Features

- Input any movie name and get a list of similar movies.
- Each recommended movie is clickable and links directly to a Google search for more details.
- Responsive design for mobile and desktop.
- Bootstrap-based UI for a modern and clean look.

## Tech Stack

- **Backend:** Django
- **Frontend:** HTML, CSS, Bootstrap
- **Data Processing:** Python (Pandas, Scikit-learn)
- **Dataset:** Kaggle Movies Dataset (cleaned and preprocessed)


## Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/movie-recommender.git
   cd movie-recommender
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate 
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**
   ```bash
   python manage.py runserver
   ```

5. **Visit** `http://127.0.0.1:8000/` in your browser


## How it Works

- The system uses **cosine similarity** between movie features like genres and keywords.
- When a user enters a movie title, the model finds the most similar movies from the dataset.
- The similarity matrix is precomputed for performance.


## Acknowledgements

- [Kaggle: The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)
