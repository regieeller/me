# Deployment Instructions

Your Memory Catcher app is built and ready! Here's how to get it live on your phone.

## Files Location

All files are in: `/home/user/memory-catcher/`

## Step 1: Push to GitHub (On Your Mac)

Open Terminal and run these commands:

```bash
# Navigate to the project
cd /home/user/memory-catcher

# Push to GitHub
git push -u origin main
```

If that doesn't work, try:

```bash
cd /home/user/memory-catcher
git remote set-url origin https://github.com/regieeller/memory-catcher.git
git push -u origin main
```

## Step 2: Enable GitHub Pages

1. Go to: https://github.com/regieeller/memory-catcher
2. Click **Settings** (top right)
3. Click **Pages** (left sidebar)
4. Under "Build and deployment":
   - Source: **Deploy from a branch**
   - Branch: **main** / (root)
   - Click **Save**
5. Wait 1-2 minutes

## Step 3: Access Your App

Your app will be live at:
```
https://regieeller.github.io/memory-catcher
```

## Step 4: Install to Your iPhone

1. Open Safari on your iPhone
2. Go to: https://regieeller.github.io/memory-catcher
3. Tap the Share button (square with arrow)
4. Scroll down and tap "Add to Home Screen"
5. Tap "Add"

Done! The app is now on your home screen like a native app.

## What You Get

✅ Full offline support
✅ Text, photo, and voice memories
✅ Auto-tagging
✅ Smart search
✅ Timeline browsing
✅ Export functionality
✅ 100% private (data stays on your device)

## Troubleshooting

**Can't push to GitHub?**
```bash
# Make sure you're authenticated
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Try HTTPS URL
git remote set-url origin https://github.com/regieeller/memory-catcher.git
git push -u origin main
```

**GitHub Pages not working?**
- Wait 2-3 minutes after enabling
- Check Settings → Pages shows green checkmark
- Make sure branch is set to "main"

**App won't install to home screen?**
- Must use Safari on iPhone (not Chrome)
- Must be on HTTPS (GitHub Pages is HTTPS)
- Try force-refreshing the page first

## Next Steps

Once deployed:
1. Test capturing a memory
2. Try voice recording
3. Test offline mode (turn off WiFi)
4. Share with family!

Need help? Check README.md or create an issue on GitHub.
