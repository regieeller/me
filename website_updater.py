#!/usr/bin/env python3
"""
Website Updater
Auto-updates films.html and commits to GitHub
"""

from bs4 import BeautifulSoup
import subprocess
import json

class WebsiteUpdater:
    def __init__(self):
        self.films_html_path = 'films.html'

    def update_films_page(self, db):
        """Update films.html with current database"""

        # Read current HTML
        with open(self.films_html_path, 'r', encoding='utf-8') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')

        # Find the watched and to-watch sections
        sections = soup.find_all('section')

        for section in sections:
            h2 = section.find('h2')
            if not h2:
                continue

            section_title = h2.get_text().strip().lower()

            if 'watched' in section_title:
                # Update watched list
                film_list = section.find('ul', class_='film-list')
                if film_list:
                    # Clear existing
                    film_list.clear()

                    # Add updated films (sorted by rating desc)
                    sorted_films = sorted(db['watched'],
                                        key=lambda x: x['rating'],
                                        reverse=True)

                    for film in sorted_films:
                        li = soup.new_tag('li')

                        # Check if this film has a review page
                        title_slug = film['title'].lower().replace(' ', '-').replace("'", '')
                        review_file = f"{title_slug}-review.html"

                        # Create title (with or without link)
                        if film['title'] == 'Primer':  # We know Primer has a review
                            link = soup.new_tag('a', href='primer-review.html')
                            link.string = film['title']
                            li.append(link)
                            li.append(' ')
                        else:
                            li.append(film['title'])
                            li.append(' ')

                        # Add rating
                        rating_span = soup.new_tag('span')
                        rating_span['class'] = 'rating'
                        rating_span.string = f"{film['rating']}/10"
                        li.append(rating_span)

                        film_list.append(li)

            elif 'to watch' in section_title:
                # Update to-watch list
                film_list = section.find('ul', class_='film-list')
                if film_list:
                    # Clear existing
                    film_list.clear()

                    # Add updated films
                    for film in db['to_watch']:
                        li = soup.new_tag('li')
                        li.string = film['title']
                        film_list.append(li)

        # Write updated HTML
        with open(self.films_html_path, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))

        return True

    def git_commit_and_push(self, message):
        """Commit and push changes to GitHub"""
        try:
            # Add films.html and database
            subprocess.run(['git', 'add', 'films.html', 'films_db.json'],
                         check=True, capture_output=True)

            # Commit
            subprocess.run(['git', 'commit', '-m', message],
                         check=True, capture_output=True)

            # Push
            result = subprocess.run(
                ['git', 'push', '-u', 'origin', 'claude/minimalist-website-NpcAJ'],
                check=True,
                capture_output=True,
                text=True
            )

            return True, "Updated and pushed to GitHub"
        except subprocess.CalledProcessError as e:
            return False, f"Git error: {e.stderr}"

    def sync_database_to_website(self, db, commit_message="Update film database"):
        """Full sync: Update HTML and commit"""
        # Update HTML
        self.update_films_page(db)

        # Commit and push
        success, message = self.git_commit_and_push(commit_message)

        return success, message
