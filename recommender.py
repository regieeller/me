#!/usr/bin/env python3
"""
Film Recommender - THE HUNT
Generates personalized recommendations in the specified voice
"""

import random
from tmdb_api import TMDBClient, TMDB_GENRES

class FilmRecommender:
    def __init__(self, curator):
        self.curator = curator
        self.tmdb = TMDBClient()

    def analyze_preferences(self):
        """Analyze user's rating patterns"""
        patterns = {
            'loves': [],  # 9-10 ratings
            'likes': [],  # 7.5-8.5 ratings
            'avoids': []  # <=6 ratings
        }

        for film in self.curator.db['watched']:
            rating = film['rating']
            title = film['title']

            if rating >= 9:
                patterns['loves'].append(title)
            elif rating >= 7.5:
                patterns['likes'].append(title)
            elif rating <= 6:
                patterns['avoids'].append(title)

        return patterns

    def hunt(self, query, count=3):
        """
        THE HUNT - Main recommendation function

        Args:
            query: User's request (e.g., "cerebral sci-fi", "documentary", "horror")
            count: Number of recommendations (default 3)

        Returns:
            List of recommendations with THE HUNT voice
        """

        # Parse query for genre/keywords
        genre_id = self._extract_genre(query)

        # Get candidates from TMDB
        candidates = self._get_candidates(genre_id, query)

        # Filter out already seen
        candidates = self._filter_seen(candidates)

        # Score based on taste profile
        scored = self._score_candidates(candidates)

        # Select top N
        top_picks = scored[:count]

        # Format in THE HUNT voice
        recommendations = []
        for film in top_picks:
            rec = self._format_hunt_voice(film, query)
            recommendations.append(rec)

        return recommendations

    def _extract_genre(self, query):
        """Extract genre from query"""
        query_lower = query.lower()

        for genre, genre_id in TMDB_GENRES.items():
            if genre in query_lower:
                return genre_id

        return None

    def _get_candidates(self, genre_id, query):
        """Get candidate films from TMDB"""
        if not self.tmdb.api_key:
            return self._fallback_recommendations()

        # Try TMDB discovery
        if genre_id:
            films = self.tmdb.discover_films(genre=genre_id)
        else:
            # General high-rated films
            films = self.tmdb.discover_films(sort_by='vote_average.desc')

        return films[:20]  # Top 20 candidates

    def _filter_seen(self, candidates):
        """Remove films already in database"""
        filtered = []

        for film in candidates:
            title = film.get('title', '')
            seen, _, _ = self.curator.is_already_seen(title)

            if not seen:
                filtered.append(film)

        return filtered

    def _score_candidates(self, candidates):
        """Score candidates based on taste profile"""
        # For now, return top-rated
        # Future: ML-based scoring
        scored = sorted(candidates,
                       key=lambda x: x.get('vote_average', 0),
                       reverse=True)
        return scored

    def _format_hunt_voice(self, film, query):
        """Format recommendation in THE HUNT voice"""
        title = film.get('title', 'Unknown')
        year = film.get('release_date', '')[:4] if film.get('release_date') else '????'
        overview = film.get('overview', '')
        rating = film.get('vote_average', 0)

        # Generate hook in THE HUNT voice
        hook = self._generate_hook(title, overview, query)

        # Why it fits
        why = self._generate_why(film, query)

        return {
            'title': f"{title} ({year})",
            'hook': hook,
            'why': why,
            'tmdb_rating': rating
        }

    def _generate_hook(self, title, overview, query):
        """Generate 2-sentence hook in Backman/Hemingway voice"""
        # Extract key phrases from overview
        sentences = overview.split('.')[:3]

        # For now, use first 2 sentences
        # Future: AI-generated hooks
        if len(sentences) >= 2:
            hook = f"{sentences[0].strip()}. {sentences[1].strip()}."
        else:
            hook = overview[:200] + "..."

        return hook

    def _generate_why(self, film, query):
        """Generate 'Why it fits' explanation"""
        patterns = self.analyze_preferences()

        # Match to user's 10/10s
        if patterns['loves']:
            reference = random.choice(patterns['loves'])
            return f"Matches your love of {reference}'s intensity"

        return "Fits your taste for cerebral narratives"

    def _fallback_recommendations(self):
        """Fallback when TMDB unavailable"""
        # Hand-curated deep cuts based on user's taste
        return [
            {
                'title': 'Triangle of Sadness',
                'release_date': '2022',
                'overview': 'Wealth doesn corrupt. It reveals. The yacht sinks. Power inverts.',
                'vote_average': 7.8
            },
            {
                'title': 'Sound of Metal',
                'release_date': '2019',
                'overview': 'Silence is not peace. Silence is a new problem you didnt ask for.',
                'vote_average': 7.7
            },
            {
                'title': 'Im Thinking of Ending Things',
                'release_date': '2020',
                'overview': 'The farmhouse is wrong. The timeline is wrong. She knows it.',
                'vote_average': 6.6
            }
        ]
