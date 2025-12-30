#!/usr/bin/env python3
"""
Film Database Extractor
Extracts film data from films.html and creates films_db.json
"""

from bs4 import BeautifulSoup
import json
import re

def extract_films():
    """Extract films from films.html"""

    with open('films.html', 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    films_db = {
        "watched": [],
        "to_watch": []
    }

    # Find watched section
    sections = soup.find_all('section')

    for section in sections:
        h2 = section.find('h2')
        if not h2:
            continue

        section_title = h2.get_text().strip().lower()

        if 'watched' in section_title:
            # Extract watched films with ratings
            film_list = section.find('ul', class_='film-list')
            if film_list:
                for li in film_list.find_all('li'):
                    # Check if it's a link (like Primer review)
                    link = li.find('a')
                    if link:
                        title = link.get_text().strip()
                    else:
                        # Extract title from text
                        text = li.get_text()
                        # Remove rating
                        title = re.sub(r'\s*\d+\.?\d*/10\s*$', '', text).strip()

                    # Extract rating
                    rating_span = li.find('span', class_='rating')
                    if rating_span:
                        rating_text = rating_span.get_text().strip()
                        rating = float(rating_text.replace('/10', ''))
                    else:
                        rating = None

                    films_db['watched'].append({
                        'title': title,
                        'rating': rating
                    })

        elif 'to watch' in section_title:
            # Extract to-watch films
            film_list = section.find('ul', class_='film-list')
            if film_list:
                for li in film_list.find_all('li'):
                    title = li.get_text().strip()
                    films_db['to_watch'].append({
                        'title': title
                    })

    return films_db

if __name__ == '__main__':
    print("Extracting films from films.html...")
    films_db = extract_films()

    print(f"Found {len(films_db['watched'])} watched films")
    print(f"Found {len(films_db['to_watch'])} to-watch films")

    # Save to JSON
    with open('films_db.json', 'w', encoding='utf-8') as f:
        json.dump(films_db, f, indent=2, ensure_ascii=False)

    print("✓ Database saved to films_db.json")
