# 💭 Memory Catcher

A simple, private Progressive Web App for capturing and recalling life's memories.

## What It Does

Memory Catcher helps you preserve moments that matter:
- **Quick Capture**: Text, photos, or voice notes in seconds
- **Smart Recall**: Fuzzy search finds memories even with partial details
- **Auto-Tagging**: Automatically identifies people, places, and themes
- **Works Offline**: Your memories are always accessible
- **100% Private**: All data stays on your device

## Features

### Capture
- ✍️ **Text** - Jot down thoughts quickly
- 📷 **Photos** - Attach images to memories
- 🎤 **Voice Notes** - Record audio memories

### Organize
- 🏷️ **Auto-Tags** - Automatic keyword extraction
- 🔍 **Smart Search** - Find anything, even with typos
- 📅 **Timeline** - Browse by date (today, week, month, all)

### Recall
- 🎲 **Random Memory** - Rediscover old moments
- 📊 **Statistics** - Track your memory journey
- 📤 **Export** - Backup all memories as JSON

### Tech
- 📱 **PWA** - Installs like a native app
- 🔌 **Offline** - Works without internet
- 💾 **Local Storage** - No servers, no tracking
- 🚀 **Fast** - Instant load, instant save

## Quick Start

### Option 1: Use it Now (No Installation)

1. Visit the deployed app: `https://yourusername.github.io/memory-catcher`
2. Start capturing memories!
3. On mobile: Tap "Share" → "Add to Home Screen"

### Option 2: Deploy Your Own

**Step 1: Enable GitHub Pages**

1. Go to your repo: `https://github.com/regieeller/memory-catcher`
2. Click **Settings** → **Pages**
3. Under "Source", select **main** branch
4. Click **Save**
5. Wait 1-2 minutes for deployment
6. Visit: `https://regieeller.github.io/memory-catcher`

**That's it!** Your personal memory catcher is live.

### Option 3: Run Locally

```bash
# Clone the repo
git clone https://github.com/regieeller/memory-catcher.git
cd memory-catcher

# Open in browser (no build step needed!)
open index.html
# Or use a simple server:
python3 -m http.server 8000
# Then visit: http://localhost:8000
```

## How to Use

### Capturing a Memory

1. **Tap the + button**
2. **Type your memory** (or leave blank for photo/voice only)
3. **Optional**: Add a photo (📷 button)
4. **Optional**: Record voice (🎤 button)
5. **Tap "Save Memory"**

Done! Your memory is saved locally.

### Finding a Memory

**Search:**
- Type in the search bar: "beach", "mom", "birthday", etc.
- Fuzzy matching finds partial matches

**Browse:**
- Today / This Week / This Month tabs
- Scroll through timeline

**Random:**
- Menu → Random Memory
- Nostalgic surprise!

### Installing to Phone

**iPhone:**
1. Open in Safari
2. Tap Share button (□↑)
3. Tap "Add to Home Screen"
4. Tap "Add"

**Android:**
1. Open in Chrome
2. Tap menu (⋮)
3. Tap "Install app" or "Add to Home Screen"

Now it works like a native app!

## Privacy & Data

### Where is my data stored?
- **Locally** in your browser's localStorage
- **Never** sent to any server
- **Never** shared with anyone
- **Never** tracked or analyzed

### Backing up
- Menu → Export All Memories
- Saves a JSON file with all data
- Keep this file safe!

### Restoring
- Currently manual (copy JSON to new device)
- Import feature coming in V3

### Clearing data
- Clear browser data = clear memories
- Export first to back up!

## Tech Stack

Built with vanilla web technologies:
- **HTML5** - Structure
- **CSS3** - Styling (responsive, mobile-first)
- **JavaScript** - Logic (no frameworks!)
- **PWA** - Offline support, installable
- **Web APIs**:
  - localStorage (data persistence)
  - MediaDevices (camera/mic access)
  - MediaRecorder (voice recording)
  - Service Worker (offline mode)

## Browser Support

- ✅ Chrome/Edge (desktop & mobile)
- ✅ Safari (desktop & mobile)
- ✅ Firefox (desktop & mobile)
- ⚠️ Voice recording requires HTTPS or localhost

## Roadmap

**V2.0** ✅ (Current)
- Text, photo, voice capture
- Auto-tagging
- Search & filter
- Timeline view
- Export
- PWA/offline

**V3.0** 🚧 (Future)
- Import from export
- Cloud sync (optional)
- Shared memories (family mode)
- AI-powered insights
- Photo albums
- Advanced search filters
- Themes/customization

## Development

Want to modify or contribute?

```bash
# Clone
git clone https://github.com/regieeller/memory-catcher.git
cd memory-catcher

# Edit files
# - index.html (structure)
# - styles.css (styling)
# - app.js (functionality)

# Test locally
python3 -m http.server 8000

# Commit changes
git add .
git commit -m "Your changes"
git push
```

No build process needed - it's pure HTML/CSS/JS!

## Customization

### Change Colors

Edit `styles.css`:
```css
:root {
    --primary: #4F46E5;  /* Main color */
    --danger: #EF4444;   /* Delete color */
    /* ... more colors */
}
```

### Add More Auto-Tags

Edit `app.js`, search for `extractTags()` function:
```javascript
const keywords = {
    people: ['mom', 'dad', 'friend', 'YourName'],
    places: ['home', 'park', 'YourCity'],
    // Add your own!
}
```

### Change App Name

Edit `manifest.json`:
```json
{
    "name": "Your App Name",
    "short_name": "YourApp"
}
```

## Troubleshooting

**App won't install to home screen**
- Make sure you're using HTTPS (GitHub Pages uses HTTPS)
- Try in different browser
- Clear cache and reload

**Voice recording doesn't work**
- Requires HTTPS or localhost
- Grant microphone permission
- Try different browser

**Search not finding memories**
- Check spelling (fuzzy search helps but isn't perfect)
- Try different keywords
- Use tags

**Memories disappeared**
- Did you clear browser data?
- Try different browser/device
- Always export for backup!

**App is slow**
- 1000+ memories? Export and archive old ones
- Clear browser cache
- Try different browser

## FAQ

**Q: Is this really private?**
A: Yes! Everything stays in your browser. No servers, no tracking, no analytics.

**Q: Can I sync across devices?**
A: Not yet in V2. Coming in V3. For now, export/import.

**Q: What happens if I clear browser data?**
A: Your memories are deleted. Always export regularly!

**Q: Can I share memories with family?**
A: Not yet. Family sharing mode planned for V3.

**Q: Does it work offline?**
A: Yes! Once loaded, works 100% offline.

**Q: Can I use it for journaling?**
A: Absolutely! Perfect for daily journaling.

**Q: Is there a limit to memories?**
A: localStorage limit (~10MB). That's thousands of text memories, or hundreds with photos.

## License

MIT License - Use freely!

## Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/regieeller/memory-catcher/issues)
- 💬 **Feedback**: Open an issue or PR
- 🌟 **Star** the repo if you find it useful!

## Credits

Created with ❤️ for preserving life's moments.

Icon: 💭 (Thought Bubble emoji)

---

**Remember**: The best camera is the one you have with you. The best memory catcher is the one you'll actually use. 💭
