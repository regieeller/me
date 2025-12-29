#!/usr/bin/env python3
"""
X Viral Post Detector
Finds posts with high viral potential for early engagement
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from playwright.async_api import async_playwright
import re

class ViralPostDetector:
    def __init__(self):
        self.posts = []
        self.config_dir = Path("config")
        self.data_dir = Path("data")
        self.reports_dir = Path("reports")

        # Create directories if they don't exist
        for dir in [self.config_dir, self.data_dir, self.reports_dir]:
            dir.mkdir(exist_ok=True)

        # Load configuration
        self.accounts_to_monitor = self.load_accounts()
        self.trending_keywords = [
            "unpopular opinion",
            "hot take",
            "just realized",
            "nobody talks about",
            "controversial opinion"
        ]

    def load_accounts(self):
        """Load list of accounts to monitor from config"""
        config_file = self.config_dir / "accounts.json"
        if config_file.exists():
            with open(config_file, 'r') as f:
                data = json.load(f)
                return data.get('accounts', [])
        return []

    def calculate_viral_score(self, post_data):
        """Calculate viral potential score for a post"""

        # Extract metrics
        likes = post_data.get('likes', 0)
        replies = post_data.get('replies', 0)
        retweets = post_data.get('retweets', 0)
        followers = post_data.get('author_followers', 1)
        hours_ago = post_data.get('hours_ago', 24)

        # Prevent division by zero
        if hours_ago == 0:
            hours_ago = 0.5

        # Calculate component scores
        total_engagement = likes + replies + retweets

        # 1. Engagement Velocity (40% weight)
        velocity = total_engagement / hours_ago
        velocity_score = min(velocity / 100, 1.0)  # Normalize: 100+ eng/hour = 1.0

        # 2. Engagement Ratio (30% weight)
        engagement_ratio = total_engagement / max(followers, 1)
        ratio_score = min(engagement_ratio * 10, 1.0)  # 10% ratio = 1.0

        # 3. Reply-to-Like Ratio (15% weight)
        reply_ratio = replies / max(likes, 1)
        reply_score = min(reply_ratio * 2, 1.0)  # 50% ratio = 1.0

        # 4. Follower Quality (10% weight)
        # Sweet spot: 2k-50k followers
        if followers < 500:
            follower_score = 0.2
        elif followers < 2000:
            follower_score = 0.5
        elif followers < 50000:
            follower_score = 1.0
        elif followers < 100000:
            follower_score = 0.7
        else:
            follower_score = 0.4

        # 5. RT-to-Like Ratio (5% weight)
        rt_ratio = retweets / max(likes, 1)
        rt_score = min(rt_ratio * 5, 1.0)  # 20% ratio = 1.0

        # Calculate weighted score
        viral_score = (
            velocity_score * 0.40 +
            ratio_score * 0.30 +
            reply_score * 0.15 +
            follower_score * 0.10 +
            rt_score * 0.05
        )

        # Store breakdown for reporting
        post_data['score_breakdown'] = {
            'velocity': round(velocity_score, 2),
            'engagement_ratio': round(ratio_score, 2),
            'reply_ratio': round(reply_score, 2),
            'follower_quality': round(follower_score, 2),
            'rt_ratio': round(rt_score, 2)
        }
        post_data['metrics'] = {
            'velocity': round(velocity, 1),
            'eng_ratio_pct': round(engagement_ratio * 100, 1)
        }

        return round(viral_score, 3)

    def should_include_post(self, post_data):
        """Filter criteria for posts"""

        # Minimum engagement threshold
        if post_data.get('likes', 0) < 50:
            return False

        if post_data.get('replies', 0) < 10:
            return False

        # Recency filter (1-6 hours)
        hours_ago = post_data.get('hours_ago', 24)
        if hours_ago < 1 or hours_ago > 6:
            return False

        return True

    async def scrape_search_results(self, page, search_query, max_posts=20):
        """Scrape posts from X search results"""
        posts = []

        try:
            # Navigate to search
            search_url = f"https://x.com/search?q={search_query}&src=typed_query&f=live"
            await page.goto(search_url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(3)

            # Scroll to load posts
            for _ in range(3):
                await page.evaluate("window.scrollBy(0, 1000)")
                await asyncio.sleep(1)

            # Extract posts (simplified - you'll need to adjust selectors)
            articles = await page.query_selector_all('article[data-testid="tweet"]')

            for article in articles[:max_posts]:
                try:
                    post_data = await self.extract_post_data(article, page)
                    if post_data:
                        posts.append(post_data)
                except Exception as e:
                    print(f"Error extracting post: {e}")
                    continue

        except Exception as e:
            print(f"Error scraping search '{search_query}': {e}")

        return posts

    async def scrape_account_timeline(self, page, username, max_posts=5):
        """Scrape recent posts from a specific account"""
        posts = []

        try:
            await page.goto(f"https://x.com/{username}", wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2)

            # Scroll to load posts
            await page.evaluate("window.scrollBy(0, 500)")
            await asyncio.sleep(1)

            articles = await page.query_selector_all('article[data-testid="tweet"]')

            for article in articles[:max_posts]:
                try:
                    post_data = await self.extract_post_data(article, page)
                    if post_data:
                        post_data['source'] = f'account:{username}'
                        posts.append(post_data)
                except Exception as e:
                    continue

        except Exception as e:
            print(f"Error scraping @{username}: {e}")

        return posts

    async def scrape_trending_topics(self, page):
        """Scrape posts from trending topics"""
        posts = []

        try:
            # Go to explore/trending
            await page.goto("https://x.com/explore/tabs/trending", wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2)

            # Extract trending topics
            trends = await page.query_selector_all('[data-testid="trend"]')
            trend_topics = []

            for trend in trends[:5]:  # Top 5 trends
                try:
                    text_elem = await trend.query_selector('span')
                    if text_elem:
                        text = await text_elem.inner_text()
                        if text and not text.startswith('·'):
                            trend_topics.append(text.strip())
                except:
                    continue

            # Search each trending topic
            for topic in trend_topics:
                topic_posts = await self.scrape_search_results(page, topic, max_posts=10)
                for post in topic_posts:
                    post['source'] = f'trending:{topic}'
                posts.extend(topic_posts)

        except Exception as e:
            print(f"Error scraping trending topics: {e}")

        return posts

    async def extract_post_data(self, article, page):
        """Extract data from a single post element"""
        try:
            post_data = {}

            # Get post link/ID
            link_elem = await article.query_selector('a[href*="/status/"]')
            if link_elem:
                href = await link_elem.get_attribute('href')
                post_data['url'] = f"https://x.com{href}"
                post_data['id'] = href.split('/status/')[-1].split('?')[0] if '/status/' in href else None

            # Get author
            author_elem = await article.query_selector('[data-testid="User-Name"] a')
            if author_elem:
                author_href = await author_elem.get_attribute('href')
                post_data['author'] = author_href.strip('/') if author_href else 'unknown'

            # Get post text
            text_elem = await article.query_selector('[data-testid="tweetText"]')
            if text_elem:
                post_data['text'] = await text_elem.inner_text()
            else:
                post_data['text'] = ''

            # Get engagement metrics
            # Likes
            like_elem = await article.query_selector('[data-testid="like"]')
            if like_elem:
                like_text = await like_elem.inner_text()
                post_data['likes'] = self.parse_metric(like_text)

            # Replies
            reply_elem = await article.query_selector('[data-testid="reply"]')
            if reply_elem:
                reply_text = await reply_elem.inner_text()
                post_data['replies'] = self.parse_metric(reply_text)

            # Retweets
            retweet_elem = await article.query_selector('[data-testid="retweet"]')
            if retweet_elem:
                retweet_text = await retweet_elem.inner_text()
                post_data['retweets'] = self.parse_metric(retweet_text)

            # Get timestamp
            time_elem = await article.query_selector('time')
            if time_elem:
                datetime_str = await time_elem.get_attribute('datetime')
                if datetime_str:
                    post_time = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
                    hours_ago = (datetime.now().astimezone() - post_time).total_seconds() / 3600
                    post_data['hours_ago'] = round(hours_ago, 1)
                    post_data['posted_at'] = datetime_str

            # For follower count, we'd need to visit the profile (expensive)
            # For now, we'll estimate or skip
            post_data['author_followers'] = 10000  # Placeholder - can enhance later

            return post_data if post_data.get('id') else None

        except Exception as e:
            print(f"Error extracting post data: {e}")
            return None

    def parse_metric(self, text):
        """Parse engagement metric (handles K, M notation)"""
        if not text:
            return 0

        text = text.strip().upper()
        multiplier = 1

        if 'K' in text:
            multiplier = 1000
            text = text.replace('K', '')
        elif 'M' in text:
            multiplier = 1000000
            text = text.replace('M', '')

        try:
            number = float(text)
            return int(number * multiplier)
        except:
            return 0

    async def run_detection(self):
        """Main detection workflow"""
        print("🚀 Starting X Viral Post Detector...")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        async with async_playwright() as p:
            # Launch browser
            print("🌐 Launching browser...")
            browser = await p.chromium.launch(
                headless=True,  # Set to False to see browser
                args=['--disable-blink-features=AutomationControlled']
            )

            # Use existing Chrome profile to stay logged in
            # On Mac: ~/Library/Application Support/Google/Chrome/Default
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )

            page = await context.new_page()

            all_posts = []

            # Strategy 1: Trending Topics
            print("📊 Strategy 1: Scanning trending topics...")
            trending_posts = await self.scrape_trending_topics(page)
            all_posts.extend(trending_posts)
            print(f"   Found {len(trending_posts)} posts from trending topics")

            # Strategy 2: Keyword Search
            print("\n🔍 Strategy 2: Searching viral keywords...")
            keyword_searches = [
                "min_faves:50 min_replies:10",  # Posts with engagement
                "unpopular opinion min_faves:50",
                "hot take min_faves:50",
            ]

            for search in keyword_searches:
                posts = await self.scrape_search_results(page, search, max_posts=15)
                all_posts.extend(posts)
                print(f"   '{search}': {len(posts)} posts")
                await asyncio.sleep(2)

            # Strategy 3: Monitor Accounts
            if self.accounts_to_monitor:
                print(f"\n👥 Strategy 3: Monitoring {len(self.accounts_to_monitor)} accounts...")
                for username in self.accounts_to_monitor[:10]:  # Limit for speed
                    posts = await self.scrape_account_timeline(page, username, max_posts=3)
                    all_posts.extend(posts)
                    await asyncio.sleep(1)
                print(f"   Found {len([p for p in all_posts if p.get('source', '').startswith('account:')])} posts from accounts")

            await browser.close()

        # Deduplicate posts by ID
        seen_ids = set()
        unique_posts = []
        for post in all_posts:
            post_id = post.get('id')
            if post_id and post_id not in seen_ids:
                seen_ids.add(post_id)
                unique_posts.append(post)

        print(f"\n📝 Total unique posts collected: {len(unique_posts)}")

        # Calculate viral scores
        print("🧮 Calculating viral scores...")
        scored_posts = []
        for post in unique_posts:
            if self.should_include_post(post):
                score = self.calculate_viral_score(post)
                post['viral_score'] = score
                scored_posts.append(post)

        # Sort by score
        scored_posts.sort(key=lambda x: x['viral_score'], reverse=True)

        print(f"✅ {len(scored_posts)} posts meet criteria\n")

        # Generate report
        self.generate_report(scored_posts[:15])  # Top 15

        return scored_posts

    def generate_report(self, posts):
        """Generate markdown report"""
        today = datetime.now().strftime('%Y-%m-%d')
        report_file = self.reports_dir / f"{today}.md"

        with open(report_file, 'w') as f:
            f.write(f"# 🔥 Viral Post Candidates - {today}\n\n")
            f.write(f"Generated at {datetime.now().strftime('%H:%M:%S')}\n\n")
            f.write(f"**Found {len(posts)} high-potential posts**\n\n")
            f.write("---\n\n")

            for i, post in enumerate(posts, 1):
                score = post['viral_score']

                # Emoji based on score
                if score >= 0.7:
                    emoji = "🔥🔥🔥"
                elif score >= 0.5:
                    emoji = "🔥🔥"
                elif score >= 0.3:
                    emoji = "🔥"
                else:
                    emoji = "💡"

                f.write(f"## #{i} - Viral Score: {score} {emoji}\n\n")

                # Post details
                f.write(f"**Author:** @{post.get('author', 'unknown')}\n")
                f.write(f"**Posted:** {post.get('hours_ago', 'N/A')} hours ago\n")
                f.write(f"**Source:** {post.get('source', 'search')}\n\n")

                # Stats
                f.write(f"**Stats:**\n")
                f.write(f"- ❤️ {post.get('likes', 0):,} likes\n")
                f.write(f"- 💬 {post.get('replies', 0):,} replies\n")
                f.write(f"- 🔄 {post.get('retweets', 0):,} retweets\n\n")

                # Why it's viral
                breakdown = post.get('score_breakdown', {})
                metrics = post.get('metrics', {})
                f.write(f"**Why it's going viral:**\n")
                f.write(f"- Engagement velocity: {metrics.get('velocity', 0)} eng/hour ")
                f.write(f"({self.score_to_stars(breakdown.get('velocity', 0))})\n")
                f.write(f"- Engagement ratio: {metrics.get('eng_ratio_pct', 0)}% ")
                f.write(f"({self.score_to_stars(breakdown.get('engagement_ratio', 0))})\n")
                f.write(f"- Reply activity: {self.score_to_stars(breakdown.get('reply_ratio', 0))}\n\n")

                # Post text preview
                text = post.get('text', '')
                if len(text) > 200:
                    text = text[:200] + "..."
                f.write(f"**Post preview:**\n> {text}\n\n")

                # Link
                f.write(f"**🔗 [View Post]({post.get('url', '#')})**\n\n")

                # Comment suggestions
                f.write(f"**💡 Comment suggestions:**\n")
                f.write(f"- Add a thoughtful counterpoint or supporting argument\n")
                f.write(f"- Share a relevant personal experience\n")
                f.write(f"- Ask a thought-provoking follow-up question\n")
                f.write(f"- Provide additional context or data\n\n")

                f.write("---\n\n")

        print(f"📄 Report saved to: {report_file}")
        print(f"\n✨ Review your report and start engaging!\n")

    def score_to_stars(self, score):
        """Convert score to star rating"""
        stars = int(score * 5)
        return "⭐" * stars if stars > 0 else "○"


async def main():
    detector = ViralPostDetector()
    await detector.run_detection()


if __name__ == "__main__":
    asyncio.run(main())
