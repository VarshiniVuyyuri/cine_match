#  CineMatch - Movie Recommendation System

CineMatch is a web application built with Flask that helps users discover movies, rate them, and get personalized recommendations. Users can browse a movie catalog, manage a personal watchlist, and receive smart suggestions based on their viewing preferences.

##  Features

- **Movie Catalog**: Browse a collection of movies with posters, descriptions, genres, and release years.
- **Search & Filter**: Easily find movies by title or filter the catalog by genre.
- **Star Ratings**: Rate movies on a scale of 1 to 5 stars. Your ratings are saved instantly.
- **Average Ratings**: See the community average rating for each movie.
- **Personal Watchlist**: Add movies you want to watch later and manage your list.
- **Smart Recommendations**: Get personalized movie suggestions based on the genres you rate highly.
- **Top-Rated List**: View a list of the most highly-rated movies by all users.

##  Tech Stack

- **Backend**: Python, Flask, Flask-SQLAlchemy
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Development**: Git & GitHub for version control.

##  Project Structure

The project is organized with a standard Flask application structure:

cinematch/
├── .flaskenv           # Environment variables for Flask
├── app.py              # Main Flask application file (routes, models, logic)
├── requirements.txt    # Python package dependencies
├── static/             # Contains static assets
│   ├── css/
│   │   └── style.css   # Custom stylesheets
│   ├── js/
│   │   └── script.js   # Custom JavaScript for interactivity
│   └── images/         # For storing static images like posters
├── templates/          # Contains HTML templates rendered by Flask
│   ├── base.html       # Base layout with navbar and footer
│   ├── index.html      # Main movie browsing page
│   ├── movie_detail.html # Page for a single movie's details
│   ├── recommendations.html # Page to display recommendations
│   ├── top_rated.html  # Page for the highest-rated movies
│   └── watchlist.html  # User's personal watchlist page
└── README.md           # Project documentation


##  How to Run the Project

### 1. Prerequisites

- Python 3.8+
- `pip` for package management
- A virtual environment tool (`venv`)

### 2. Setup and Installation

```bash
# Clone the repository
git clone [https://github.com/your-username/cinematch.git](https://github.com/your-username/cinematch.git)
cd cinematch

# Create and activate a virtual environment
# On Windows:
python -m venv venv
venv\Scripts\activate
# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Initialize the database (one-time command)
# This creates the database file and seeds it with sample movies.
flask db-init