import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import json
import random

# --- App & Database Configuration ---

app = Flask(__name__)
# Get the absolute path of the directory where the script is located
basedir = os.path.abspath(os.path.dirname(__file__))
# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'cinematch.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_super_secret_key'  # Needed for flash messages

db = SQLAlchemy(app)

# --- Database Models ---

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(200), nullable=False)
    watchlist_count = db.Column(db.Integer, default=0) # Track how many watchlists it's on
    
    # Relationship to ratings
    ratings = db.relationship('UserRating', backref='movie', lazy=True, cascade="all, delete-orphan")

    def average_rating(self):
        avg = db.session.query(func.avg(UserRating.rating)).filter(UserRating.movie_id == self.id).scalar()
        return round(avg, 1) if avg else 0.0

class UserRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False) # Rating from 1 to 5
    # In a real app, you'd have a user_id here. We'll simulate a single user.

class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    # In a real app, you'd have a user_id here.
    
    movie = db.relationship('Movie')

# --- Command to Initialize and Seed Database ---

@app.cli.command('db-init')
def db_init():
    """Initializes the database and seeds it with sample movie data."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Load movie data from a file or define here
        movies_data = [
            {"title": "Inception", "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.", "genre": "Sci-Fi", "release_year": 2010, "poster_url": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg"},
            {"title": "The Dark Knight", "description": "When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.", "genre": "Action", "release_year": 2008, "poster_url": "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg"},
            {"title": "Forrest Gump", "description": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75, whose only desire is to be reunited with his childhood sweetheart.", "genre": "Drama", "release_year": 1994, "poster_url": "https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg"},
            {"title": "Pulp Fiction", "description": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.", "genre": "Crime", "release_year": 1994, "poster_url": "https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg"},
            {"title": "The Matrix", "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.", "genre": "Sci-Fi", "release_year": 1999, "poster_url": "https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg"},
            {"title": "Interstellar", "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.", "genre": "Sci-Fi", "release_year": 2014, "poster_url": "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg"},
            {"title": "Spirited Away", "description": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.", "genre": "Animation", "release_year": 2001, "poster_url": "https://m.media-amazon.com/images/M/MV5BMjlmZmI5MDctNDE2YS00YWE0LWE5ZWItZWRhMWQ0NTcxNWRhXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg"},
            {"title": "Parasite", "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.", "genre": "Thriller", "release_year": 2019, "poster_url": "https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_SX300.jpg"},
            {"title": "The Lion King", "description": "Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself.", "genre": "Animation", "release_year": 1994, "poster_url": "https://m.media-amazon.com/images/M/MV5BYTYxNGMyZTYtMjE3MS00MzNjLWFjNmYtMDk3N2FmM2Q0OWROYw@@._V1_SX300.jpg"},
            {"title": "Gladiator", "description": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.", "genre": "Action", "release_year": 2000, "poster_url": "https://m.media-amazon.com/images/M/MV5BMDliMmNhNDEtODUyOS00MjNlLTgxODEtN2U3NzIxMGVkZTA1L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg"}
        ]

        for movie_data in movies_data:
            movie = Movie(**movie_data)
            db.session.add(movie)
        
        db.session.commit()
        print('Database initialized and seeded with sample movies.')


# --- Helper Functions ---

def get_genres():
    """Returns a list of unique genres from the movies in the database."""
    genres = db.session.query(Movie.genre).distinct().order_by(Movie.genre).all()
    return [genre[0] for genre in genres]


# --- Main Routes ---

@app.route('/')
def index():
    """Main page to browse movies. Supports search and filtering."""
    query = request.args.get('search', '')
    genre_filter = request.args.get('genre', 'all')
    
    movies_query = Movie.query
    
    if query:
        movies_query = movies_query.filter(Movie.title.ilike(f'%{query}%'))
    
    if genre_filter != 'all':
        movies_query = movies_query.filter(Movie.genre == genre_filter)
        
    all_movies = movies_query.order_by(Movie.title).all()
    genres = get_genres()
    
    return render_template('index.html', movies=all_movies, genres=genres, current_genre=genre_filter, search_query=query)

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    """Displays details for a single movie."""
    movie = Movie.query.get_or_404(movie_id)
    # For now, we simulate a single user's rating
    user_rating = UserRating.query.filter_by(movie_id=movie.id).first()
    return render_template('movie_detail.html', movie=movie, user_rating=user_rating)

@app.route('/top-rated')
def top_rated():
    """Displays movies sorted by their average rating."""
    top_movies = db.session.query(
        Movie,
        func.avg(UserRating.rating).label('average_rating')
    ).join(UserRating).group_by(Movie.id).order_by(func.avg(UserRating.rating).desc()).limit(10).all()
    
    # The query returns tuples of (Movie, avg_rating), so we unpack them
    movies = [movie for movie, avg_rating in top_movies]
    
    return render_template('top_rated.html', movies=movies)

# --- Rating and Watchlist API Routes ---

@app.route('/rate/<int:movie_id>', methods=['POST'])
def rate_movie(movie_id):
    """Handles rating a movie."""
    rating_value = int(request.form.get('rating'))
    
    # Find existing rating or create a new one
    user_rating = UserRating.query.filter_by(movie_id=movie_id).first()
    if user_rating:
        user_rating.rating = rating_value
    else:
        user_rating = UserRating(movie_id=movie_id, rating=rating_value)
        db.session.add(user_rating)
        
    db.session.commit()
    
    # Recalculate average rating
    movie = Movie.query.get(movie_id)
    avg_rating = movie.average_rating()
    
    return jsonify({'status': 'success', 'message': f'You rated {movie.title} {rating_value} stars.', 'new_avg_rating': avg_rating})

@app.route('/watchlist')
def view_watchlist():
    """Displays the user's watchlist."""
    watchlist_items = Watchlist.query.order_by(Watchlist.id.desc()).all()
    return render_template('watchlist.html', watchlist_items=watchlist_items)

@app.route('/watchlist/add/<int:movie_id>', methods=['POST'])
def add_to_watchlist(movie_id):
    """Adds a movie to the watchlist."""
    # Check if movie exists
    movie = Movie.query.get_or_404(movie_id)
    # Check if it's already in the watchlist
    if not Watchlist.query.filter_by(movie_id=movie_id).first():
        watchlist_item = Watchlist(movie_id=movie_id)
        movie.watchlist_count += 1
        db.session.add(watchlist_item)
        db.session.commit()
        return jsonify({'status': 'success', 'action': 'added', 'message': f"'{movie.title}' added to your watchlist."})
    else:
        return jsonify({'status': 'info', 'action': 'exists', 'message': f"'{movie.title}' is already in your watchlist."})

@app.route('/watchlist/remove/<int:watchlist_id>', methods=['POST'])
def remove_from_watchlist(watchlist_id):
    """Removes a movie from the watchlist."""
    item = Watchlist.query.get_or_404(watchlist_id)
    item.movie.watchlist_count = max(0, item.movie.watchlist_count - 1) # Prevent negative count
    db.session.delete(item)
    db.session.commit()
    flash(f"'{item.movie.title}' was removed from your watchlist.", 'success')
    return redirect(url_for('view_watchlist'))

# --- Recommendation Logic ---

@app.route('/recommendations')
def recommendations():
    """Generates personalized movie recommendations."""
    # Simple recommendation logic:
    # 1. Find the top-rated genres by the user (rating >= 4).
    # 2. Find movies in those genres that the user hasn't rated yet.
    # 3. Randomly select a few to recommend.
    
    # Find genres of movies rated 4 or 5 stars
    highly_rated = UserRating.query.filter(UserRating.rating >= 4).all()
    if not highly_rated:
        # If no high ratings, recommend popular movies instead (most watchlisted)
        recommended_movies = Movie.query.order_by(Movie.watchlist_count.desc(), Movie.title).limit(5).all()
        return render_template('recommendations.html', movies=recommended_movies, logic="popular")

    favorite_genres = {rating.movie.genre for rating in highly_rated}
    
    # Get IDs of movies already rated by the user
    rated_movie_ids = [r.movie_id for r in UserRating.query.all()]
    
    # Find unrated movies in those favorite genres
    recommendations_query = Movie.query.filter(
        Movie.genre.in_(favorite_genres),
        ~Movie.id.in_(rated_movie_ids)
    )
    
    recommended_movies = recommendations_query.all()
    random.shuffle(recommended_movies) # Shuffle to provide variety
    
    return render_template('recommendations.html', movies=recommended_movies[:5], logic="personalized")


if __name__ == '__main__':
    app.run(debug=True)