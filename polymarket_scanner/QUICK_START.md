# 5-Minute Quick Start

**For absolute beginners who just want to see it work**

---

## Step 1: Open Terminal

**Mac:** Press `Cmd + Space`, type `Terminal`, press Enter

**Linux:** Press `Ctrl + Alt + T`

**Windows (WSL):** Press `Win + R`, type `wsl`, press Enter

---

## Step 2: Navigate to Scanner

Copy and paste this (then press Enter):

```bash
cd /home/user/me/polymarket_scanner
```

**If error "No such file":** Try this instead:
```bash
cd ~/polymarket_scanner
```

---

## Step 3: Install Requirements

Copy and paste this:

```bash
pip3 install -r requirements.txt
```

**Wait for it to finish** (30-60 seconds)

**If error "pip3 not found":** Install Python first (see SOP_BEGINNERS.md Part 1)

---

## Step 4: Run the Scanner

Copy and paste this:

```bash
python3 scanner.py
```

---

## What You'll See

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

**Then either:**
- ✓ No alerts (normal - markets are quiet)
- 🚨 Alerts appear (someone made a big trade!)

---

## Let It Run

**Watch for 2-3 minutes**

You'll see it scan every 60 seconds

---

## Stop the Scanner

**Press: `Ctrl + C`**

You'll see:
```
🛑 Scanner stopped by user
   Total whale wallets discovered: X
   Alerts saved to: data/alerts.jsonl
```

---

## Check Your Data

```bash
ls data/
```

You should see files created!

---

## ✅ SUCCESS!

**You just ran the scanner!**

**Next steps:**
1. Read `SOP_BEGINNERS.md` for full guide
2. Learn what alerts mean
3. Run scanner daily for 1 week
4. Adjust settings if needed

---

## Daily Use (Simple)

**Every day:**

```bash
cd /home/user/me/polymarket_scanner
python3 scanner.py
```

**When done:** Press `Ctrl + C`

**That's it!**

---

## Need Help?

**Read these in order:**

1. `QUICK_START.md` (you're here) ← 5 minutes
2. `SOP_BEGINNERS.md` ← Complete guide for non-technical users
3. `SOP.md` ← Advanced operations
4. `README.md` ← Technical overview

**Start with #2 (SOP_BEGINNERS.md) if you want step-by-step instructions.**
