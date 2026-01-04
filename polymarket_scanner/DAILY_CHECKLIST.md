# Daily Scanner Checklist

**Print this and keep next to your computer**

---

## Morning Routine (5 minutes)

### □ Start Scanner

```bash
cd /home/user/me/polymarket_scanner
python3 scanner.py
```

### □ Check If Running

Look for:
```
🔄 Starting scan at [TIME]
   Scanning X markets...
```

### □ Keep Terminal Window Open

Don't close it! Scanner needs it.

---

## During the Day (As Needed)

### When You See 🚨 RED Alert

**Stop what you're doing - check immediately:**

1. □ Read the alert
2. □ Write down market name
3. □ Open Polymarket.com
4. □ Search for market
5. □ Check current price
6. □ Decide: Interesting or not?
7. □ Add note to my_notes.txt:
   ```bash
   echo "$(date): [Market] - [Decision]" >> data/my_notes.txt
   ```

### When You See ⚠️ YELLOW Alert

**Check when convenient (within 30 min):**

1. □ Note the market
2. □ If multiple alerts on same market → Treat as RED
3. □ Otherwise → Just note it happened

### When You See ℹ️ BLUE Alert

**Ignore for now - review at end of day**

---

## Evening Routine (5 minutes)

### □ Count Today's Alerts

```bash
grep "$(date +%Y-%m-%d)" data/alerts.jsonl | wc -l
```

Write number here: ________

### □ Check Whale Wallets

```bash
cat data/whale_wallets.json
```

Any new wallets today? YES / NO

### □ Review Notes

```bash
cat data/my_notes.txt | tail -10
```

### □ Stop Scanner

**Press: `Ctrl + C`**

Wait for:
```
🛑 Scanner stopped by user
```

---

## Sunday Evening (10 minutes)

### □ Weekly Backup

```bash
cd /home/user/me/polymarket_scanner
mkdir -p backups
tar -czf backups/backup_$(date +%Y%m%d).tar.gz data/
```

### □ Review Week

Total alerts this week: ________

Top 3 markets by alerts:
1. ________________________________
2. ________________________________
3. ________________________________

### □ Adjust Settings?

Too many alerts (>50/day)? → Increase thresholds
Too few alerts (<5/day)? → Decrease thresholds
Just right (10-30/day)? → Don't change

---

## Monthly (First Sunday)

### □ Performance Review

Alerts this month: ________
Whale wallets discovered: ________
Actions taken based on alerts: ________

### □ Archive Old Data

```bash
cd /home/user/me/polymarket_scanner/data
MONTH_AGO=$(date -d '30 days ago' +%Y-%m-%d)
awk -v d="$MONTH_AGO" '$0 < d' alerts.jsonl > alerts_archive.jsonl
awk -v d="$MONTH_AGO" '$0 >= d' alerts.jsonl > alerts_current.jsonl
mv alerts_current.jsonl alerts.jsonl
gzip alerts_archive.jsonl
```

---

## Quick Reference Commands

### Start scanner:
```bash
cd /home/user/me/polymarket_scanner && python3 scanner.py
```

### Stop scanner:
```
Ctrl + C
```

### Check if running:
```bash
ps aux | grep scanner.py
```

### Today's alerts:
```bash
grep "$(date +%Y-%m-%d)" data/alerts.jsonl
```

### Backup now:
```bash
tar -czf backups/backup_$(date +%Y%m%d).tar.gz data/
```

---

## Week 1 Goals

- [ ] Run scanner every day
- [ ] Respond to at least 1 CRITICAL alert
- [ ] Collect at least 50 total alerts
- [ ] Discover at least 3 whale wallets
- [ ] Complete first weekly backup

---

## Week 2-4 Goals

- [ ] Adjust settings if needed
- [ ] Build watchlist of interesting markets
- [ ] Track which wallets appear most often
- [ ] Reach 100+ total alerts
- [ ] Reach 10+ whale wallets
- [ ] Ready for Phase 2

---

## Emergency Procedures

### Scanner Crashed
```bash
cd /home/user/me/polymarket_scanner
python3 scanner.py
```
(Just restart it)

### Lost Terminal Window
1. Open new Terminal
2. Check if still running: `ps aux | grep scanner.py`
3. If yes: `tail -f scanner.log` to watch
4. If no: Restart scanner

### Computer Restarted
1. Scanner stopped (normal)
2. Restart scanner when you're back
3. Check data/ folder still has files
4. Continue as normal

---

## Red Flags (Call for Help)

❌ Scanner won't start (errors every time)
❌ No data/ folder after running
❌ Disk space <500MB
❌ Crashes every scan cycle
❌ Zero alerts for 7+ days straight

**If you see these → Review SOP_BEGINNERS.md Part 7 (Troubleshooting)**

---

**Checklist Version:** 1.0
**Date Started:** _______________
**Current Week:** _______________
**Total Alerts:** _______________
**Total Whales:** _______________
