# Film Curator - Expert Recommendation System

Your personalized film recommendation engine that learns from your taste.

## Quick Start

### 1. Get TMDB API Key (Free, takes 2 minutes)

1. Go to https://www.themoviedb.org/
2. Create a free account
3. Go to Settings → API
4. Request an API key (select "Developer")
5. Copy your API key

### 2. Set Up API Key

Create a file called `.env` in this directory:

```bash
echo "TMDB_API_KEY=your_api_key_here" > .env
```

Replace `your_api_key_here` with your actual key.

### 3. Run the Film Curator

```bash
python3 film_curator.py
```

Then open your browser to: **http://localhost:5000**

## What You Can Do

### Rate Films
- Enter a film title and rating (0-10)
- System updates your database
- Learns from your preferences
- Auto-commits to your website

### Check if Seen
- Enter a film title
- System checks watched and watchlist
- Shows your rating if already watched

### Add to Watchlist
- Enter a film title
- Adds to your to-watch list
- Won't add if already watched

### View Taste Profile
- Click "Show Taste Analysis"
- See your 10/10s, 9/10s, etc.
- Understand what you love

## How It Works

### Your Taste Profile

Based on your ratings, the system knows:

**Perfect 10/10:**
- Primer, Coherence, Interstellar, Arrival
- **Pattern:** Cerebral, time-bending, trust the audience

**Excellence 9-9.5/10:**
- Mind-bending narratives
- Psychological depth
- Indie aesthetic

**Low Rated (≤6/10):**
- Films that avoid these patterns

### The System Learns

Every time you rate a film:
1. Database updates
2. Taste profile recalculates
3. Future recommendations improve
4. Website auto-updates (coming soon)

## Files

- `film_curator.py` - Main web interface
- `films_db.json` - Your film database
- `extract_films.py` - Sync with films.html
- `templates/index.html` - Web interface

## Next Features (In Progress)

- [ ] TMDB API integration for film metadata
- [ ] Recommendation engine with "THE HUNT" voice
- [ ] Auto-update films.html
- [ ] Auto-commit and push to GitHub
- [ ] Film similarity analysis
- [ ] Genre-aware recommendations

## Your Workflow

1. **Get Recommendations:** (Coming soon with TMDB)
   - "Give me cerebral sci-fi"
   - System suggests 3 films in "THE HUNT" voice

2. **Already Seen It?**
   - Rate it immediately
   - System learns and moves on

3. **Haven't Seen It?**
   - Add to watchlist or watch it
   - Rate when done
   - System gets smarter

## The Voice

Recommendations will use your specified style:
- Short sentences. Fragments.
- Sensory details.
- 2-sentence hook per film.
- No plot summaries. Just texture.

Example:
```
Triangle of Sadness (2022)
Wealth doesn't corrupt. It reveals. The yacht sinks.
Power inverts. Watch them eat each other.
Why: Primer's class consciousness meets Coherence's trapped space.
```

## Database Format

Your `films_db.json`:

```json
{
  "watched": [
    {"title": "Primer", "rating": 10},
    {"title": "Coherence", "rating": 10}
  ],
  "to_watch": [
    {"title": "Aniara"}
  ]
}
```

## Support

The system will NEVER recommend films you've already watched or have in your watchlist.
If it does, just rate it and keep moving - the system learns.

---

**Built specifically for your taste in film as art, not content.**
