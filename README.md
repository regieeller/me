# 🔥 X Viral Post Detector

Find X posts with high viral potential before they blow up. Comment early, get impressions.

## What It Does

This tool uses **three strategies** to find posts that are about to go viral:

1. **Trending Topics** - Scans X's trending section for emerging posts
2. **Viral Keywords** - Searches for posts using viral trigger phrases
3. **Account Monitoring** - Checks recent posts from curated accounts

Then it analyzes each post using a viral scoring algorithm based on:
- Engagement velocity (likes/hour)
- Engagement ratio (engagement vs. follower count)
- Reply activity (discussion level)
- Retweet ratio (share rate)
- Poster's follower sweet spot (2k-50k ideal)

**Output:** A ranked list of top posts to engage with, delivered as a markdown report.

## Setup Instructions (Mac)

### 1. Install Python

Open Terminal and check if Python is installed:

```bash
python3 --version
```

If you don't have Python 3.8+, install it:

**Option A: Using Homebrew (recommended)**
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
```

**Option B: Download from python.org**
- Go to https://www.python.org/downloads/
- Download Python 3.11+ for macOS
- Run the installer

### 2. Clone/Download This Repository

```bash
cd ~/Desktop  # or wherever you want to keep this
# If you have this as a git repo:
git clone <your-repo-url>
cd x-viral-detector

# Or if you're just setting it up:
cd x-viral-detector
```

### 3. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it:
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Install Playwright Browsers

Playwright needs to download browser binaries:

```bash
playwright install chromium
```

This downloads a Chromium browser (about 300MB).

### 6. Configure Accounts to Monitor (Optional)

Edit `config/accounts.json` to add/remove accounts you want to monitor:

```bash
nano config/accounts.json
# or use any text editor
```

The default list includes popular tech/startup accounts. Customize to your interests!

### 7. Stay Logged Into X

**Important:** Open Chrome/Safari and make sure you're logged into X (twitter.com or x.com).

The script will use your session to access X. You need to be logged in.

## Usage

### Run the Detector

Each evening (or whenever), run:

```bash
# Make sure you're in the project directory
cd ~/Desktop/x-viral-detector  # or wherever you put it

# Activate virtual environment
source venv/bin/activate

# Run the script
python3 find_viral_posts.py
```

### What Happens

```
🚀 Starting X Viral Post Detector...
⏰ 2025-12-29 20:30:00

🌐 Launching browser...
📊 Strategy 1: Scanning trending topics...
   Found 23 posts from trending topics

🔍 Strategy 2: Searching viral keywords...
   'min_faves:50 min_replies:10': 15 posts
   'unpopular opinion min_faves:50': 12 posts
   'hot take min_faves:50': 18 posts

👥 Strategy 3: Monitoring 20 accounts...
   Found 31 posts from accounts

📝 Total unique posts collected: 87
🧮 Calculating viral scores...
✅ 34 posts meet criteria

📄 Report saved to: reports/2025-12-29.md

✨ Review your report and start engaging!
```

The script takes about **3-5 minutes** to run.

### Read Your Report

```bash
open reports/2025-12-29.md
# or
cat reports/2025-12-29.md
```

You'll get a ranked list like this:

```markdown
## #1 - Viral Score: 0.78 🔥🔥🔥

**Author:** @username
**Posted:** 2.5 hours ago
**Source:** trending:AI

**Stats:**
- ❤️ 1,234 likes
- 💬 387 replies
- 🔄 456 retweets

**Why it's going viral:**
- Engagement velocity: 493 eng/hour (⭐⭐⭐⭐⭐)
- Engagement ratio: 12.3% (⭐⭐⭐⭐⭐)
- Reply activity: ⭐⭐⭐⭐

**Post preview:**
> "Unpopular opinion: Most productivity advice is just procrastination with extra steps..."

🔗 [View Post](https://x.com/username/status/...)

**💡 Comment suggestions:**
- Add a thoughtful counterpoint or supporting argument
- Share a relevant personal experience
- Ask a thought-provoking follow-up question
```

### Review & Engage

1. Open the report
2. Click through to the top 5-10 posts
3. Leave thoughtful, valuable comments
4. Watch your impressions grow! 📈

## Tips for Success

### Daily Routine

**Evening (5 minutes):**
1. `cd ~/Desktop/x-viral-detector`
2. `source venv/bin/activate`
3. `python3 find_viral_posts.py`
4. Review report while running

**Engagement (10-15 minutes):**
1. Open top 10 posts
2. Write thoughtful comments (not spam!)
3. Aim for value-add, not just "great post"
4. Track which posts actually went viral

### Optimize Your Results

**Week 1:** Run daily, comment on top 10 posts
**Week 2:** Review which posts went viral, adjust accounts list
**Week 3:** Fine-tune scoring weights based on your results
**Week 4:** You're now catching viral posts consistently 🚀

### Customize Account List

Focus on accounts in niches where you want visibility:
- Tech/Startup: naval, levelsio, paulg, sama
- Marketing/Growth: gregisenberg, lennysan
- Design: jackbutcher
- Your specific niche: add relevant accounts

Sweet spot: **5k-100k follower accounts** in your niche

## Troubleshooting

### "Command not found: python3"
- Python isn't installed. Follow step 1 above.

### "playwright: command not found"
- Make sure virtual environment is activated: `source venv/bin/activate`
- Reinstall: `pip install -r requirements.txt`

### "Browser doesn't stay logged in"
- The script uses a fresh browser session each time
- You might need to log in once when running
- Or modify script to use your Chrome profile (advanced)

### Script is slow
- Normal! Scraping takes 3-5 minutes
- Can reduce account list or max_posts in code

### No posts found
- Check that you're logged into X in your browser
- Try adjusting search keywords in the script
- Lower the minimum engagement thresholds

### Selectors broke (X changed their layout)
- X updates their HTML frequently
- You may need to update the CSS selectors in `extract_post_data()`
- Open an issue or check for updates

## Advanced Configuration

### Adjust Scoring Weights

Edit `find_viral_posts.py`, line ~70, function `calculate_viral_score()`:

```python
viral_score = (
    velocity_score * 0.40 +      # Adjust these weights
    ratio_score * 0.30 +
    reply_score * 0.15 +
    follower_score * 0.10 +
    rt_score * 0.05
)
```

### Change Time Window

Edit line ~95, `should_include_post()`:

```python
if hours_ago < 1 or hours_ago > 6:  # Change 6 to wider window
    return False
```

### Add More Search Keywords

Edit line ~27, `__init__()`:

```python
self.trending_keywords = [
    "unpopular opinion",
    "hot take",
    "just realized",
    "your custom phrase here",
]
```

## Privacy & Ethics

- ✅ This tool helps you find posts to engage with authentically
- ✅ Use it to add value to conversations
- ❌ Don't spam or leave generic comments
- ❌ Don't use for manipulation or harassment

**Be a good citizen of X.** Add value, be thoughtful, build genuine connections.

## Files Overview

```
x-viral-detector/
├── find_viral_posts.py      # Main script
├── requirements.txt          # Python dependencies
├── config/
│   └── accounts.json        # Accounts to monitor
├── reports/                 # Daily reports generated here
│   └── 2025-12-29.md       # Example report
└── data/                    # Optional: store historical data
```

## What's Next?

After running for a week, you can:
1. Track your success rate (which posts actually went viral)
2. Measure your impression growth
3. Refine the accounts you monitor
4. Adjust scoring weights based on results
5. Add automation (run via cron job)
6. Build a dashboard to visualize trends

## License

MIT - Use freely, build cool stuff!

## Questions?

Open an issue or ping me on X: [@byregie](https://x.com/byregie)

---

**Built with:** Python, Playwright, and the desire to catch waves early 🏄‍♂️
