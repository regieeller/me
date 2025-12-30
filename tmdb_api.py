#!/usr/bin/env python3
"""
TMDB API Integration
Handles film metadata and search via The Movie Database API
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

class TMDBClient:
    def __init__(self):
        self.api_key = os.getenv('TMDB_API_KEY')
        self.base_url = 'https://api.themoviedb.org/3'

    def search_film(self, title):
        """Search for a film by title"""
        if not self.api_key:
            return None

        url = f"{self.base_url}/search/movie"
        params = {
            'api_key': self.api_key,
            'query': title,
            'language': 'en-US'
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if data['results']:
                return data['results'][0]  # Return first match
            return None
        except Exception as e:
            print(f"TMDB API Error: {e}")
            return None

    def get_film_details(self, tmdb_id):
        """Get detailed information about a film"""
        if not self.api_key:
            return None

        url = f"{self.base_url}/movie/{tmdb_id}"
        params = {
            'api_key': self.api_key,
            'append_to_response': 'credits,keywords'
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"TMDB API Error: {e}")
            return None

    def get_similar_films(self, tmdb_id):
        """Get films similar to the given film"""
        if not self.api_key:
            return []

        url = f"{self.base_url}/movie/{tmdb_id}/similar"
        params = {
            'api_key': self.api_key,
            'language': 'en-US',
            'page': 1
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('results', [])
        except Exception as e:
            print(f"TMDB API Error: {e}")
            return []

    def discover_films(self, genre=None, year_min=None, year_max=None, sort_by='vote_average.desc'):
        """Discover films based on criteria"""
        if not self.api_key:
            return []

        url = f"{self.base_url}/discover/movie"
        params = {
            'api_key': self.api_key,
            'language': 'en-US',
            'sort_by': sort_by,
            'vote_count.gte': 100,  # Minimum votes for quality
            'page': 1
        }

        if genre:
            params['with_genres'] = genre
        if year_min:
            params['primary_release_date.gte'] = f"{year_min}-01-01"
        if year_max:
            params['primary_release_date.lte'] = f"{year_max}-12-31"

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('results', [])
        except Exception as e:
            print(f"TMDB API Error: {e}")
            return []

# Genre IDs for reference
TMDB_GENRES = {
    'sci-fi': 878,
    'thriller': 53,
    'horror': 27,
    'mystery': 9648,
    'drama': 18,
    'documentary': 99,
    'crime': 80
}
