#!/usr/bin/env python3
"""
Film Curator - Expert Film Recommendation System
Web interface for personalized film recommendations
"""

from flask import Flask, render_template, request, jsonify
import json
import os
import subprocess
from datetime import datetime

app = Flask(__name__)

class FilmCurator:
    def __init__(self):
        self.load_database()
        self.analyze_taste()

    def load_database(self):
        """Load films database"""
        with open('films_db.json', 'r') as f:
            self.db = json.load(f)

    def save_database(self):
        """Save films database"""
        with open('films_db.json', 'w') as f:
            json.dump(self.db, f, indent=2, ensure_ascii=False)

    def analyze_taste(self):
        """Analyze user's taste from ratings"""
        self.taste_profile = {
            '10/10': [],
            '9-9.5/10': [],
            '8-8.5/10': [],
            'low_rated': []
        }

        for film in self.db['watched']:
            rating = film['rating']
            title = film['title']

            if rating == 10:
                self.taste_profile['10/10'].append(title)
            elif rating >= 9:
                self.taste_profile['9-9.5/10'].append(title)
            elif rating >= 8:
                self.taste_profile['8-8.5/10'].append(title)
            elif rating <= 6:
                self.taste_profile['low_rated'].append(title)

    def get_taste_summary(self):
        """Return taste profile summary"""
        return {
            'perfection': self.taste_profile['10/10'],
            'excellence': self.taste_profile['9-9.5/10'],
            'solid': self.taste_profile['8-8.5/10'],
            'avoid_patterns': self.taste_profile['low_rated']
        }

    def is_already_seen(self, title):
        """Check if film is in watched or to-watch list"""
        title_lower = title.lower()

        # Check watched
        for film in self.db['watched']:
            if film['title'].lower() == title_lower:
                return True, 'watched', film.get('rating')

        # Check to-watch
        for film in self.db['to_watch']:
            if film['title'].lower() == title_lower:
                return True, 'to_watch', None

        return False, None, None

    def rate_film(self, title, rating):
        """Rate a watched film"""
        # Check if already exists
        for film in self.db['watched']:
            if film['title'].lower() == title.lower():
                film['rating'] = rating
                self.save_database()
                self.analyze_taste()
                return True, f"Updated {title} to {rating}/10"

        # Add new film
        self.db['watched'].append({
            'title': title,
            'rating': rating
        })

        # Remove from to-watch if present
        self.db['to_watch'] = [f for f in self.db['to_watch']
                               if f['title'].lower() != title.lower()]

        self.save_database()
        self.analyze_taste()
        return True, f"Added {title}: {rating}/10"

    def add_to_watchlist(self, title):
        """Add film to watchlist"""
        # Check if already watched
        for film in self.db['watched']:
            if film['title'].lower() == title.lower():
                return False, f"{title} already watched ({film['rating']}/10)"

        # Check if already in watchlist
        for film in self.db['to_watch']:
            if film['title'].lower() == title.lower():
                return False, f"{title} already in watchlist"

        self.db['to_watch'].append({'title': title})
        self.save_database()
        return True, f"Added {title} to watchlist"

curator = FilmCurator()

@app.route('/')
def index():
    """Main interface"""
    return render_template('index.html',
                         watched_count=len(curator.db['watched']),
                         watchlist_count=len(curator.db['to_watch']))

@app.route('/taste')
def taste():
    """Show taste profile"""
    profile = curator.get_taste_summary()
    return jsonify(profile)

@app.route('/rate', methods=['POST'])
def rate():
    """Rate a film"""
    data = request.json
    title = data.get('title')
    rating = float(data.get('rating'))

    success, message = curator.rate_film(title, rating)
    return jsonify({'success': success, 'message': message})

@app.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
    """Add to watchlist"""
    data = request.json
    title = data.get('title')

    success, message = curator.add_to_watchlist(title)
    return jsonify({'success': success, 'message': message})

@app.route('/check', methods=['POST'])
def check():
    """Check if film is already seen"""
    data = request.json
    title = data.get('title')

    seen, status, rating = curator.is_already_seen(title)

    if seen:
        if status == 'watched':
            return jsonify({
                'seen': True,
                'status': 'watched',
                'rating': rating,
                'message': f"You've seen this! Rated {rating}/10"
            })
        else:
            return jsonify({
                'seen': True,
                'status': 'watchlist',
                'message': "Already in your watchlist"
            })
    else:
        return jsonify({'seen': False})

if __name__ == '__main__':
    print("=" * 60)
    print("FILM CURATOR - Expert Recommendation System")
    print("=" * 60)
    print(f"Watched films: {len(curator.db['watched'])}")
    print(f"Watchlist: {len(curator.db['to_watch'])}")
    print("\nStarting web interface...")
    print("Open: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, port=5000)
