# Polymarket Scanner - Beginner's Operating Guide

**Version:** 2.0 (Beginner Edition)
**Last Updated:** 2026-01-04
**Audience:** Non-technical users who want to run the scanner

---

## PART 0: BEFORE YOU START

### What You Need

**Hardware Options (Choose ONE):**

1. **Desktop/Laptop (Easiest)**
   - Windows 10/11, Mac, or Linux
   - Must stay on to run scanner
   - Need: 4GB+ RAM, 10GB free disk space
   - **Recommended for beginners**

2. **Always-On Server/VPS (Advanced)**
   - Runs 24/7 even if your computer is off
   - Costs $5-20/month
   - Examples: DigitalOcean, AWS, Linode
   - **Only if you want 24/7 monitoring**

3. **Raspberry Pi (Advanced)**
   - Small computer that runs 24/7
   - Low power consumption
   - Need technical setup
   - **Only for experienced users**

**For This Guide: We assume you're using a Desktop/Laptop**

---

### Where Are You Running This?

**CRITICAL QUESTION:** Are you on the same computer that has the files in `/home/user/me/polymarket_scanner`?

**Check now:**

**If you're on Windows:**
- Open Command Prompt (Win + R, type `cmd`, press Enter)
- Type: `dir C:\`
- If you see folders, you're on Windows

**If you're on Mac:**
- Open Terminal (Cmd + Space, type "Terminal", press Enter)
- Type: `ls /`
- If you see folders, you're on Mac

**If you're on Linux:**
- Open Terminal
- Type: `ls /`
- You should see folders like "home", "usr", etc.

**The path `/home/user/me/` suggests Linux or Mac.**

**If this is NOT your computer:**
You need to:
1. Download the scanner files to YOUR computer, OR
2. Connect to the Linux server where the files are

**For this guide, we assume the files are already on your Linux/Mac computer.**

---

## PART 1: ABSOLUTE BEGINNER SETUP

### Step 1.1: Open Terminal

**On Mac:**
1. Click the magnifying glass (Spotlight) in top-right corner
2. Type: `Terminal`
3. Press Enter
4. A black or white window will open - this is Terminal

**On Linux (Ubuntu/Debian):**
1. Press `Ctrl + Alt + T`
2. OR: Click Activities → Search "Terminal"
3. A window will open - this is Terminal

**On Windows (if files are on Windows Subsystem for Linux):**
1. Press `Win + R`
2. Type: `wsl`
3. Press Enter
4. A terminal window will open

**What you see:**
```
user@computer:~$
```
The `$` means it's waiting for your command.

---

### Step 1.2: Find the Scanner Files

**Type this command EXACTLY (then press Enter):**
```bash
cd /home/user/me/polymarket_scanner
```

**What happens:**

**If successful:**
```
user@computer:~/polymarket_scanner$
```
The path before `$` changed - you're now in the scanner directory.

**If you see an error:**
```
bash: cd: /home/user/me/polymarket_scanner: No such file or directory
```

**Fix:** The files aren't where we thought. Try this:
```bash
cd ~/polymarket_scanner
```

**Still an error?**
```bash
ls ~
```
This shows all folders in your home directory. Look for `polymarket_scanner`.

**If you see it, do:**
```bash
cd ~/polymarket_scanner
```

**If you DON'T see it:**
The files aren't on this computer. Stop here and ask for help.

---

### Step 1.3: Verify Files Are Present

**Type this command:**
```bash
ls
```

**What you should see:**
```
README.md
SOP.md
SOP_BEGINNERS.md
SETUP_GUIDE.md
config.py
example_output.md
polymarket_api.py
requirements.txt
scanner.py
```

**If you see these files: ✅ SUCCESS - Continue**

**If you DON'T see these files:**
- You're in the wrong directory
- Type: `pwd` (this shows where you are)
- Navigate to the correct directory

---

### Step 1.4: Check Python Is Installed

**Type this command:**
```bash
python3 --version
```

**What you should see:**
```
Python 3.9.7
```
(or 3.10, 3.11, 3.12 - any version 3.9 or higher is good)

**If you see this: ✅ SUCCESS - Continue**

**If you see an error like:**
```
bash: python3: command not found
```

**Fix - Install Python:**

**On Mac:**
```bash
# Install Homebrew first (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Then install Python
brew install python3
```

**On Ubuntu/Debian Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**On Windows (WSL):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**After installing, try again:**
```bash
python3 --version
```

---

### Step 1.5: Install Scanner Dependencies

**Type this command:**
```bash
pip3 install -r requirements.txt
```

**What happens:**
You'll see lines of text scrolling. This is normal. It's downloading libraries.

**Expected output (last few lines):**
```
Successfully installed requests-2.31.0 py-clob-client-0.17.0
```

**If you see this: ✅ SUCCESS - Continue**

**Common errors:**

**Error: "pip3: command not found"**
```bash
# Install pip
sudo apt install python3-pip  # Linux
# or
brew install python3  # Mac (includes pip)
```

**Error: "Permission denied"**
```bash
# Add --user flag
pip3 install --user -r requirements.txt
```

**Error: "No such file 'requirements.txt'"**
```bash
# Make sure you're in the right directory
pwd
# Should show: /home/user/me/polymarket_scanner (or similar)
# If not, go back to Step 1.2
```

---

### Step 1.6: Test the Scanner

**Type this command:**
```bash
python3 polymarket_api.py
```

**What you should see:**
```
Testing Polymarket API Client...

Fetching active markets...
Found 47 markets
Sample market: Will Bitcoin reach $100k by end of 2026?

API client ready!
```

**If you see this: ✅ SUCCESS - Continue**

**If you see errors:**

**Error: "No module named 'requests'"**
```bash
# Dependencies didn't install correctly
pip3 install requests py-clob-client
```

**Error: "API Request failed"**
- Your internet connection might be down
- Polymarket's API might be temporarily unavailable
- Try again in 5 minutes

**If still errors:** See PART 7 (Troubleshooting)

---

### Step 1.7: Review Configuration (Don't Change Anything Yet)

**Type this command:**
```bash
cat config.py
```

**What you see:**
A bunch of Python code with settings. Don't worry about understanding it.

**Look for these numbers:**
```python
SCAN_INTERVAL = 60
LARGE_TRADE_MIN_USD = 1000
WHALE_TRADE_MIN_USD = 5000
```

**These are the defaults. Leave them alone for Week 1.**

**Just press Enter to continue (or Ctrl+C if output is still showing).**

---

### Step 1.8: First Test Run

**This is the moment of truth. Type:**
```bash
python3 scanner.py
```

**What happens:**

**Screen will show:**
```
🔍 Polymarket Scanner initialized
   Scan interval: 60s
   Large trade threshold: $1000
   Whale trade threshold: $5000

============================================================
  POLYMARKET SCANNER - PHASE 1
  Monitoring for unusual market activity...
============================================================

🔄 Starting scan at 14:23:15
   Scanning 47 markets...
```

**Then one of two things:**

**Option A: No alerts**
```
   ✓ Scan complete - no unusual activity detected
   Tracked wallets: 0

   💤 Waiting 60s until next scan...
   --------------------------------------------------
```

**Option B: Alerts appear**
```
🚨 CRITICAL: Will Bitcoin reach $100k?
   🐋 WHALE trade: $7,500 BUY at LOW price 0.073
   • wallet: 0x742d35C...
   • trade_value: $7,500

   ⚡ Scan complete - 2 alerts generated
   Tracked wallets: 1

   💤 Waiting 60s until next scan...
   --------------------------------------------------
```

**Either is GOOD! It means the scanner works.**

**Let it run for 3 scan cycles (3 minutes).**

**You'll see the scan repeat every 60 seconds.**

---

### Step 1.9: Stop the Scanner

**When you see "💤 Waiting 60s until next scan...":**

**Press: `Ctrl + C`** (Hold Ctrl, then press C)

**What you see:**
```
🛑 Scanner stopped by user
   Total whale wallets discovered: 1
   Alerts saved to: data/alerts.jsonl
```

**If you see this: ✅ SUCCESS - Setup Complete!**

---

### Step 1.10: Verify Data Was Saved

**Type:**
```bash
ls data/
```

**You should see:**
```
alerts.jsonl
whale_wallets.json
```
(One or both files)

**If you see these files: ✅ COMPLETE SUCCESS**

**If "data/" directory doesn't exist:**
- Scanner might have crashed before saving
- Try running scanner again (Step 1.8)
- Let it run for 5 minutes

---

## PART 2: DAILY OPERATIONS (SIMPLE VERSION)

### Option A: Run Scanner While You're At Computer (Easiest)

**Use this if:** You only want alerts when you're actively watching

**Every day when you sit down at computer:**

1. Open Terminal
2. Type:
   ```bash
   cd /home/user/me/polymarket_scanner
   python3 scanner.py
   ```
3. Keep Terminal window open
4. Watch for alerts
5. When done (end of day), press `Ctrl + C`

**That's it. Scanner runs while you watch.**

---

### Option B: Run Scanner in Background (Advanced)

**Use this if:** You want scanner to run 24/7, even when not watching

**Start scanner:**
```bash
cd /home/user/me/polymarket_scanner
nohup python3 scanner.py > scanner.log 2>&1 &
echo $! > scanner.pid
```

**What happens:**
- Scanner starts running in background
- You get your terminal back
- Terminal shows a number (this is the process ID)

**Check if it's running:**
```bash
cat scanner.pid
```
This shows the process ID.

**View what scanner is doing:**
```bash
tail -f scanner.log
```
(Press `Ctrl + C` to stop viewing)

**Stop scanner:**
```bash
kill $(cat scanner.pid)
rm scanner.pid
```

---

## PART 3: UNDERSTANDING ALERTS (WHAT TO DO)

### Alert Types (Traffic Light System)

**🚨 RED (CRITICAL) = STOP AND LOOK NOW**
- Someone just made a huge bet ($5000+)
- OR: Big bet on unlikely outcome (potential insider)
- OR: Extreme price movement (>25%)

**⚠️ YELLOW (WARNING) = INTERESTING, CHECK SOON**
- Large trade ($1000+)
- Rapid price change (>10%)
- Volume spike (3x normal)

**ℹ️ BLUE (INFO) = NOTE FOR LATER**
- General observations
- Review at end of day

---

### When You See a 🚨 CRITICAL Alert

**Example:**
```
🚨 CRITICAL: Will Venezuela president step down in 2026?
   🐋 WHALE trade: $7,500 BUY at LOW price 0.073 - POTENTIAL INSIDER?
   • wallet: 0x742d35C...
   • trade_value: $7,500
   • side: BUY
   • price: 0.073
```

**What to do (Step by step):**

**1. Write it down** (pen and paper or note app):
```
Date: [Today's date]
Market: Will Venezuela president step down?
Alert: Someone bet $7,500 on 7.3% odds (YES)
Wallet: 0x742d35C...
```

**2. Open Polymarket website:**
- Go to: https://polymarket.com
- Search for the market name: "Venezuela president"
- Open the market

**3. Check current price:**
- Look at current YES price
- Is it still 7.3¢? Or did it move?
- If it moved UP → Whale might know something
- If it moved DOWN → Might be a mistake

**4. Check market details:**
- When does it resolve? (Days, weeks, months?)
- What's the volume? (High volume = more reliable)
- Read the resolution criteria

**5. Decide:**
- **Interesting?** → Add to your watchlist
- **Not interesting?** → Ignore, move on
- **Unsure?** → Watch for more alerts on same market

**6. Log your decision:**
```bash
# Create notes file (first time only)
touch /home/user/me/polymarket_scanner/data/my_notes.txt

# Add note
echo "$(date): Venezuela market - Watching, seems interesting" >> /home/user/me/polymarket_scanner/data/my_notes.txt
```

**That's it. You've responded to a critical alert.**

---

### When You See a ⚠️ WARNING Alert

**Example:**
```
⚠️ WARNING: Bitcoin above $100k by end of 2026?
   Rapid price movement on YES: +12.3%
   • outcome: YES
   • current_price: 0.423
   • change: +12.3%
```

**What to do:**

1. **Note it** (mentally or write down)
2. **Check within 30 minutes** if convenient
3. **Look for follow-up alerts**
   - If you see another WARNING or CRITICAL on same market → Investigate
   - If nothing else → Just note it happened

**Don't stress about WARNINGS. They're just "FYI" notices.**

---

### When You See a ℹ️ INFO Alert

**What to do:**
- Nothing immediately
- Review at end of day
- Look for patterns

**End of day review:**
```bash
# See today's INFO alerts
grep "INFO" /home/user/me/polymarket_scanner/data/alerts.jsonl | grep "$(date +%Y-%m-%d)"
```

---

## PART 4: CHECKING DATA (SUPER SIMPLE)

### Every Day: Quick Check

**Open Terminal, then:**

```bash
cd /home/user/me/polymarket_scanner

# How many alerts today?
grep "$(date +%Y-%m-%d)" data/alerts.jsonl | wc -l
```

**You'll see a number:**
```
7
```
This means: 7 alerts today

**See what wallets were discovered:**
```bash
cat data/whale_wallets.json
```

**You'll see:**
```json
[
  {
    "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEaE",
    "discovered_at": "2026-01-04T14:24:15",
    "discovery_trade_value": 7500.0
  }
]
```

**This shows:**
- Wallet address
- When you found it
- How much they traded

**That's your daily check. Takes 2 minutes.**

---

### Every Week: Backup Your Data

**Sunday night:**

```bash
cd /home/user/me/polymarket_scanner

# Create backups folder (first time only)
mkdir -p backups

# Backup all data
tar -czf backups/backup_$(date +%Y%m%d).tar.gz data/

# Verify it worked
ls -lh backups/
```

**You should see:**
```
backup_20260104.tar.gz
```

**This is your safety net. If something breaks, you have the data.**

---

## PART 5: ADJUSTING SETTINGS (ONLY AFTER WEEK 1)

### When to Change Settings

**After running for 1 week, ask yourself:**

**Too many alerts? (>50 per day)**
→ Increase thresholds (make less sensitive)

**Too few alerts? (<5 per day)**
→ Decrease thresholds (make more sensitive)

**Just right? (10-30 per day)**
→ Don't change anything

---

### How to Change Settings

**Open config file:**
```bash
nano /home/user/me/polymarket_scanner/config.py
```

**What you see:**
A text editor with the config file

**Find these lines:**
```python
LARGE_TRADE_MIN_USD = 1000
WHALE_TRADE_MIN_USD = 5000
MIN_MARKET_VOLUME = 5000
```

**To get FEWER alerts (too noisy):**
Change TO:
```python
LARGE_TRADE_MIN_USD = 2000       # Was 1000
WHALE_TRADE_MIN_USD = 10000      # Was 5000
MIN_MARKET_VOLUME = 10000        # Was 5000
```

**To get MORE alerts (too quiet):**
Change TO:
```python
LARGE_TRADE_MIN_USD = 500        # Was 1000
WHALE_TRADE_MIN_USD = 2000       # Was 5000
MIN_MARKET_VOLUME = 2000         # Was 5000
```

**Save and exit:**
1. Press: `Ctrl + X`
2. It asks: "Save modified buffer?"
3. Press: `Y`
4. Press: `Enter`

**Restart scanner for changes to take effect.**

---

## PART 6: COMMON QUESTIONS

### "How do I know if the scanner is running?"

**Type:**
```bash
ps aux | grep scanner.py
```

**If running, you see:**
```
user    12345  ... python3 scanner.py
```

**If NOT running, you see:**
```
user    12346  ... grep scanner.py
```
(Only the grep command itself)

---

### "How do I see what the scanner is doing right now?"

**If running in foreground:**
- Just look at the terminal window

**If running in background:**
```bash
tail -f /home/user/me/polymarket_scanner/scanner.log
```
Press `Ctrl + C` to stop viewing

---

### "How do I stop the scanner?"

**If running in foreground:**
- Press `Ctrl + C` in the terminal

**If running in background:**
```bash
kill $(cat /home/user/me/polymarket_scanner/scanner.pid)
rm /home/user/me/polymarket_scanner/scanner.pid
```

---

### "I closed the terminal, is the scanner still running?"

**If you started in foreground (Option A):**
- NO, it stopped when you closed terminal

**If you started in background (Option B with nohup):**
- YES, still running

**Check:**
```bash
ps aux | grep scanner.py
```

---

### "How much data does this use?"

**Very little:**
- ~1-5 MB per day
- After 1 month: ~50-150 MB total
- Internet bandwidth: Minimal (few KB per minute)

---

### "Can I run this on my laptop that I close/sleep?"

**Short answer: Not reliably**

**If you close/sleep laptop:**
- Scanner stops
- Resumes when you wake it

**For 24/7 monitoring:**
- Keep laptop open and awake, OR
- Use a server/VPS, OR
- Use a Raspberry Pi

**For most users:**
- Run when you're at computer
- Stop when you leave
- This is fine! You don't need 24/7

---

### "What if I miss an alert while scanner is off?"

**You won't see real-time alert, BUT:**
- The trade still happened
- It's in Polymarket's history
- Next time scanner runs, if the market is still interesting, you'll get alerted to current activity

**Missing a few hours isn't a big deal.**

---

## PART 7: TROUBLESHOOTING (WHEN THINGS GO WRONG)

### Problem: "Command not found"

**You type a command, get:**
```
bash: python3: command not found
```

**Fix:**
1. Check if Python is installed: `which python3`
2. Try: `python` instead of `python3`
3. If still error: Go back to Step 1.4 (Install Python)

---

### Problem: "No such file or directory"

**You type `cd /home/user/me/polymarket_scanner`, get:**
```
bash: cd: /home/user/me/polymarket_scanner: No such file or directory
```

**Fix:**
1. Check where you are: `pwd`
2. List files: `ls`
3. Try: `cd ~/polymarket_scanner`
4. If still error: Files aren't on this computer

---

### Problem: "Permission denied"

**Fix:**
```bash
# If installing packages:
pip3 install --user -r requirements.txt

# If creating files:
mkdir -p ~/polymarket_scanner/data
cd ~/polymarket_scanner
python3 scanner.py
```

---

### Problem: "API Request failed"

**The scanner shows:**
```
API Request failed: https://gamma-api.polymarket.com/markets - Connection error
```

**Fix:**
1. **Check internet:** Open browser, visit google.com
2. **Wait 5 minutes:** API might be temporarily down
3. **Try again:** Restart scanner
4. **If persists >1 hour:** Polymarket API might be having issues (rare)

---

### Problem: "Scanner keeps crashing"

**Fix:**
1. **Check error message:** Look at last lines before crash
2. **Check disk space:** `df -h` (need >1GB free)
3. **Reduce load:**
   - Edit config.py
   - Change: `MAX_MARKETS_TO_SCAN = 50` (was 100)
4. **Restart scanner**

---

### Problem: "Too many alerts, can't keep up"

**Fix:**
1. **Increase thresholds** (see PART 5)
2. **Turn off INFO alerts:**
   - Edit config.py
   - Change: `SHOW_INFO_ALERTS = False`
3. **Focus on CRITICAL only:**
   - Change: `SHOW_WARNING_ALERTS = False`

---

### Problem: "No alerts at all"

**If scanner runs but shows:**
```
✓ Scan complete - no unusual activity detected
```
**Every single time for days:**

**This might mean:**
1. **Settings too strict** → Lower thresholds (see PART 5)
2. **Markets are quiet** → Normal! Not always action
3. **Something wrong** → Check scanner.log for errors

**To check if scanner is working:**
```bash
# Lower thresholds temporarily
nano config.py
# Change: LARGE_TRADE_MIN_USD = 100
# Save and restart scanner
# If you see alerts now, settings were too strict
```

---

## PART 8: READY FOR PHASE 2?

### Checklist

**You're ready for Phase 2 when you can check ALL these boxes:**

- [ ] I've run scanner for at least 2 weeks
- [ ] I understand what CRITICAL alerts mean
- [ ] I have at least 10 whale wallets discovered
- [ ] I've looked at Polymarket markets based on alerts
- [ ] My data/ folder has at least 100 alerts total
- [ ] I backed up my data at least once
- [ ] I adjusted config.py at least once
- [ ] I know how to start/stop the scanner

**Count your alerts:**
```bash
wc -l /home/user/me/polymarket_scanner/data/alerts.jsonl
```

**Count your wallets:**
```bash
grep -c "address" /home/user/me/polymarket_scanner/data/whale_wallets.json
```

**If both numbers are good (>100 alerts, >10 wallets):**
✅ **READY FOR PHASE 2**

---

## PART 9: QUICK REFERENCE (COPY/PASTE COMMANDS)

### Start Scanner (Watch in Terminal)
```bash
cd /home/user/me/polymarket_scanner
python3 scanner.py
```
Stop: Press `Ctrl + C`

---

### Start Scanner (Background, 24/7)
```bash
cd /home/user/me/polymarket_scanner
nohup python3 scanner.py > scanner.log 2>&1 &
echo $! > scanner.pid
```

---

### Stop Background Scanner
```bash
kill $(cat /home/user/me/polymarket_scanner/scanner.pid)
rm /home/user/me/polymarket_scanner/scanner.pid
```

---

### Check If Running
```bash
ps aux | grep scanner.py
```

---

### See Today's Alerts
```bash
grep "$(date +%Y-%m-%d)" /home/user/me/polymarket_scanner/data/alerts.jsonl
```

---

### Count Today's Alerts
```bash
grep "$(date +%Y-%m-%d)" /home/user/me/polymarket_scanner/data/alerts.jsonl | wc -l
```

---

### See Whale Wallets
```bash
cat /home/user/me/polymarket_scanner/data/whale_wallets.json
```

---

### Backup Data
```bash
cd /home/user/me/polymarket_scanner
mkdir -p backups
tar -czf backups/backup_$(date +%Y%m%d).tar.gz data/
```

---

### View Live Scanner Output
```bash
tail -f /home/user/me/polymarket_scanner/scanner.log
```
Stop viewing: Press `Ctrl + C`

---

## PART 10: YOUR FIRST WEEK PLAN

### Day 1 (Today)
- [ ] Complete PART 1 (Setup)
- [ ] Run scanner for 30 minutes
- [ ] Stop scanner
- [ ] Check data/ folder exists

### Day 2-7
- [ ] Each morning: Start scanner
- [ ] When you see CRITICAL alert: Write it down, check Polymarket
- [ ] Each evening: Stop scanner, count alerts

### End of Week 1
- [ ] Backup data
- [ ] Count total alerts
- [ ] Count whale wallets
- [ ] Decide if settings need adjustment

### Week 2+
- [ ] Adjust settings if needed
- [ ] Keep running scanner
- [ ] Build understanding of markets
- [ ] Prepare for Phase 2

---

## SUPPORT

**If you get completely stuck:**

1. **Check which step failed**
2. **Look at error message** (read it carefully)
3. **Try troubleshooting section** (PART 7)
4. **Take a screenshot** of error
5. **Ask for help** with specific error message

**Most common issues:**
- Python not installed → Step 1.4
- Wrong directory → Step 1.2
- No internet → Check connection
- Permission errors → Add `--user` to pip install

---

**END OF BEGINNER'S GUIDE**

This guide assumes ZERO technical knowledge. Follow it step by step, and you'll be running the scanner successfully.

**Next: After 2 weeks of successful operation → Phase 2**
