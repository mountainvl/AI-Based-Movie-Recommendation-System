from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load movie dataset
movies = pd.read_csv("movies.csv")  # Dataset with 'title' and 'description'
vectorizer = TfidfVectorizer(stop_words="english")
movie_matrix = vectorizer.fit_transform(movies["description"].fillna(""))

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    user_movie = data["movie"]
    
    if user_movie not in movies["title"].values:
        return jsonify({"error": "Movie not found"})

    idx = movies[movies["title"] == user_movie].index[0]
    sim_scores = list(enumerate(cosine_similarity(movie_matrix[idx], movie_matrix)[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
    
    recommended_movies = [movies.iloc[i[0]]["title"] for i in sim_scores]
    return jsonify({"recommendations": recommended_movies})

if __name__ == "__main__":
    app.run(debug=True)
