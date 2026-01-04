# Standard Operating Procedure: Polymarket Scanner

**Version:** 1.0
**Last Updated:** 2026-01-04
**Purpose:** Systematic operation and management of the Polymarket market scanner

---

## Table of Contents

1. [Initial Setup](#1-initial-setup)
2. [Daily Operations](#2-daily-operations)
3. [Alert Response Procedures](#3-alert-response-procedures)
4. [Data Management](#4-data-management)
5. [Maintenance Tasks](#5-maintenance-tasks)
6. [Troubleshooting](#6-troubleshooting)
7. [Performance Review](#7-performance-review)
8. [Phase 2 Readiness](#8-phase-2-readiness)

---

## 1. Initial Setup

### 1.1 Installation (One-Time)

**Objective:** Get the scanner operational

**Steps:**

1. Navigate to scanner directory
   ```bash
   cd /home/user/me/polymarket_scanner
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Verify installation
   ```bash
   python polymarket_api.py
   ```

   **Expected output:**
   ```
   Testing Polymarket API Client...
   Fetching active markets...
   Found X markets
   API client ready!
   ```

4. If errors occur, see Section 6 (Troubleshooting)

**Success Criteria:** Installation completes without errors

---

### 1.2 Initial Configuration

**Objective:** Set baseline thresholds for your use case

**Steps:**

1. Open `config.py` in text editor
   ```bash
   nano config.py
   # or: vim config.py
   # or: code config.py
   ```

2. **Week 1 Settings (Conservative)**
   - Start with defaults to understand baseline activity
   - Do NOT modify anything yet
   - Goal: Learn what "normal" looks like

3. Review key settings:
   ```python
   SCAN_INTERVAL = 60              # Check every 60 seconds
   LARGE_TRADE_MIN_USD = 1000      # Trades over $1k
   WHALE_TRADE_MIN_USD = 5000      # Whales over $5k
   MIN_MARKET_VOLUME = 5000        # Ignore small markets
   ```

4. Save and close (Ctrl+X, then Y, then Enter in nano)

**Success Criteria:** Config file saved, defaults understood

---

### 1.3 Test Run

**Objective:** Confirm scanner works before leaving it running

**Steps:**

1. Start scanner in test mode
   ```bash
   python scanner.py
   ```

2. Observe first scan cycle (takes 1-3 minutes)

3. **What to look for:**
   - "🔍 Polymarket Scanner initialized" message appears
   - "Scanning X markets..." shows market count
   - Either alerts appear OR "✓ Scan complete - no unusual activity"
   - No error messages

4. Let it run for 3-5 scan cycles (5 minutes)

5. Stop gracefully: Press `Ctrl+C`

6. **Verify data directory created:**
   ```bash
   ls -la data/
   ```
   Should see: `alerts.jsonl` and possibly `whale_wallets.json`

**Success Criteria:** Scanner runs 3+ cycles without crashes

---

## 2. Daily Operations

### 2.1 Starting the Scanner

**When:** Beginning of your monitoring period (e.g., 9 AM daily, or 24/7)

**Steps:**

1. Navigate to directory
   ```bash
   cd /home/user/me/polymarket_scanner
   ```

2. **Option A: Foreground (for active monitoring)**
   ```bash
   python scanner.py
   ```
   - Keep terminal window open
   - See alerts in real-time
   - Stop with Ctrl+C

3. **Option B: Background (for 24/7 operation)**
   ```bash
   nohup python scanner.py > scanner.log 2>&1 &
   echo $! > scanner.pid
   ```
   - Saves process ID to scanner.pid
   - Logs to scanner.log
   - Continues if terminal closes

4. **Confirm it's running:**
   ```bash
   # If background mode:
   ps aux | grep scanner.py

   # Should show process running
   ```

**Success Criteria:** Scanner is active and scanning markets

---

### 2.2 Monitoring Active Scanner

**When:** While scanner is running (check every 1-4 hours if background)

**Steps:**

1. **If running in foreground:**
   - Watch terminal for alerts
   - Note any CRITICAL (red) alerts immediately

2. **If running in background:**
   ```bash
   # Check last 50 lines of output
   tail -n 50 scanner.log

   # Follow live (Ctrl+C to stop watching)
   tail -f scanner.log
   ```

3. **Check for new alerts:**
   ```bash
   # Count today's alerts
   grep "$(date +%Y-%m-%d)" data/alerts.jsonl | wc -l

   # Show recent critical alerts
   grep "CRITICAL" data/alerts.jsonl | tail -n 10
   ```

4. **Verify scanner is still running:**
   ```bash
   # Check process is alive
   ps aux | grep scanner.py

   # Or check if PID file exists
   cat scanner.pid
   ```

**Success Criteria:** Scanner is active and generating logs

---

### 2.3 Stopping the Scanner

**When:** End of monitoring period, for maintenance, or troubleshooting

**Steps:**

1. **If running in foreground:**
   - Press `Ctrl+C`
   - Wait for graceful shutdown message
   - Note the summary (whale wallets discovered, etc.)

2. **If running in background:**
   ```bash
   # Get process ID
   PID=$(cat scanner.pid)

   # Stop gracefully
   kill $PID

   # Wait 5 seconds
   sleep 5

   # Verify stopped
   ps aux | grep scanner.py

   # Clean up PID file
   rm scanner.pid
   ```

3. **If scanner won't stop:**
   ```bash
   # Force kill (last resort)
   kill -9 $(cat scanner.pid)
   rm scanner.pid
   ```

**Success Criteria:** Scanner stopped, no zombie processes

---

## 3. Alert Response Procedures

### 3.1 Alert Priority System

**Alert Levels:**

| Level | Color | Priority | Response Time | Action Required |
|-------|-------|----------|---------------|-----------------|
| 🚨 CRITICAL | Red | HIGH | Immediate | Investigate now |
| ⚠️ WARNING | Yellow | MEDIUM | Within 30 min | Review when convenient |
| ℹ️ INFO | Cyan | LOW | Daily review | Note for patterns |

---

### 3.2 CRITICAL Alert Response

**When:** Red "🚨 CRITICAL" alert appears

**Steps:**

1. **Read the alert carefully**
   ```
   🚨 CRITICAL: [Market Question]
      [Alert Message]
      • wallet: 0x742d35C...
      • trade_value: $7,500
      • price: 0.073
   ```

2. **Record key information:**
   - Market name/question
   - Wallet address (full, not abbreviated)
   - Trade value
   - Price/odds
   - Timestamp

3. **Immediate actions:**

   **For "WHALE trade at LOW price - POTENTIAL INSIDER":**
   - Open Polymarket and find the market
   - Check current price vs alert price (has it moved?)
   - Look at market volume (is it liquid?)
   - Review market question carefully (what are they betting on?)
   - Check resolution date (how long until outcome?)

   **For "WHALE position detected":**
   - Note wallet is now being tracked
   - Check if this wallet appears in multiple markets
   - Review their position size relative to market

   **For "EXTREME price movement":**
   - Check for breaking news related to market
   - Look at order book (was it one trade or sustained?)
   - Assess if movement is justified

4. **Decision tree:**
   ```
   Is this actionable?
   ├─ YES → Research further, consider position
   ├─ NO → Log as false positive
   └─ UNSURE → Add to watchlist, monitor
   ```

5. **Log your decision:**
   ```bash
   # Create notes file
   echo "$(date): [Market] - [Decision] - [Reasoning]" >> data/my_notes.txt
   ```

**Success Criteria:** All critical alerts reviewed within 15 minutes

---

### 3.3 WARNING Alert Response

**When:** Yellow "⚠️ WARNING" alert appears

**Steps:**

1. **Note the alert type:**
   - Rapid price movement
   - Volume spike
   - High concentration
   - Large trade

2. **Review context:**
   - Is this market already on your watchlist?
   - Have you seen warnings here before?
   - Is the volume high enough to matter?

3. **Action:**
   - Add market to monitoring list
   - Check back in 30-60 minutes
   - Look for follow-up alerts

4. **If multiple warnings on same market:**
   - Elevate to CRITICAL priority
   - Investigate immediately

**Success Criteria:** Warnings reviewed, no patterns missed

---

### 3.4 INFO Alert Response

**When:** Cyan "ℹ️ INFO" alert appears (or during daily review)

**Steps:**

1. **Batch review at end of day**
   ```bash
   grep "INFO" data/alerts.jsonl | grep "$(date +%Y-%m-%d)"
   ```

2. **Look for patterns:**
   - Same markets appearing repeatedly
   - Same wallets across markets
   - Timing patterns (alerts at specific times)

3. **Update watchlist if needed**

**Success Criteria:** Daily review completed, patterns noted

---

## 4. Data Management

### 4.1 Daily Data Review

**When:** End of each day (e.g., 11 PM)

**Steps:**

1. **Count today's activity:**
   ```bash
   cd /home/user/me/polymarket_scanner/data

   # Total alerts today
   grep "$(date +%Y-%m-%d)" alerts.jsonl | wc -l

   # By level
   echo "Critical: $(grep 'CRITICAL' alerts.jsonl | grep "$(date +%Y-%m-%d)" | wc -l)"
   echo "Warning: $(grep 'WARNING' alerts.jsonl | grep "$(date +%Y-%m-%d)" | wc -l)"
   echo "Info: $(grep 'INFO' alerts.jsonl | grep "$(date +%Y-%m-%d)" | wc -l)"
   ```

2. **Review whale wallets discovered:**
   ```bash
   cat whale_wallets.json
   ```

   Note:
   - How many new wallets today?
   - Total tracked wallets
   - Highest discovery trade value

3. **Create daily summary:**
   ```bash
   cat >> data/daily_summary.txt <<EOF

   === $(date +%Y-%m-%d) ===
   Total alerts: [NUMBER]
   Critical: [NUMBER]
   New wallets: [NUMBER]
   Notable markets: [LIST]
   Actions taken: [DESCRIPTION]
   EOF
   ```

**Success Criteria:** Daily summary documented

---

### 4.2 Weekly Data Backup

**When:** Every Sunday at 11 PM (or weekly interval)

**Steps:**

1. **Create backup directory:**
   ```bash
   cd /home/user/me/polymarket_scanner
   mkdir -p backups
   ```

2. **Backup all data:**
   ```bash
   DATE=$(date +%Y%m%d)
   tar -czf backups/scanner_data_$DATE.tar.gz data/
   ```

3. **Verify backup:**
   ```bash
   ls -lh backups/scanner_data_$DATE.tar.gz
   ```

4. **Clean old backups (keep last 4 weeks):**
   ```bash
   cd backups/
   ls -t scanner_data_*.tar.gz | tail -n +5 | xargs rm -f
   ```

**Success Criteria:** Backup created, old backups cleaned

---

### 4.3 Data Analysis (Weekly)

**When:** Every Sunday before creating backup

**Steps:**

1. **Generate week statistics:**
   ```bash
   cd /home/user/me/polymarket_scanner/data

   WEEK_AGO=$(date -d '7 days ago' +%Y-%m-%d)

   echo "=== Week of $(date +%Y-%m-%d) ==="
   echo "Total alerts: $(grep -c "" alerts.jsonl)"
   echo "This week: $(awk -v d="$WEEK_AGO" '$0 > d' alerts.jsonl | wc -l)"
   ```

2. **Find most active markets:**
   ```bash
   # Extract market names from alerts
   grep "market" alerts.jsonl | \
     awk -v d="$WEEK_AGO" '$0 > d' | \
     sort | uniq -c | sort -rn | head -10
   ```

3. **Analyze whale wallet performance:**
   - Count unique wallets tracked
   - Note wallets appearing in multiple alerts
   - Prepare list for Phase 2 analysis

4. **Identify patterns:**
   - What time of day are most alerts?
   - Which alert types are most common?
   - Are you getting too many/too few alerts?

**Success Criteria:** Weekly patterns identified

---

## 5. Maintenance Tasks

### 5.1 Daily Maintenance

**When:** During daily data review

**Checklist:**

- [ ] Scanner is running (or ran today)
- [ ] No error messages in logs
- [ ] Alerts.jsonl is being written to
- [ ] Disk space is sufficient (>1GB free)
- [ ] Daily summary created

**Commands:**
```bash
# Check disk space
df -h /home/user/me/polymarket_scanner

# Check file sizes
ls -lh data/
```

---

### 5.2 Weekly Maintenance

**When:** Every Sunday

**Checklist:**

- [ ] Weekly data backup created
- [ ] Weekly analysis completed
- [ ] Review config.py settings (tune if needed)
- [ ] Check for scanner updates/improvements
- [ ] Clear old log files (if using background mode)

**Commands:**
```bash
# Clean old logs (keep last 7 days)
find . -name "scanner.log*" -mtime +7 -delete

# Rotate alerts if too large (>100MB)
if [ $(stat -f%z data/alerts.jsonl) -gt 104857600 ]; then
  mv data/alerts.jsonl data/alerts_$(date +%Y%m%d).jsonl
  touch data/alerts.jsonl
fi
```

---

### 5.3 Monthly Maintenance

**When:** First Sunday of each month

**Checklist:**

- [ ] Review all config.py settings
- [ ] Analyze false positive rate
- [ ] Archive old data (>30 days)
- [ ] Review Phase 2 readiness
- [ ] Update documentation with learnings

**Steps:**

1. **Archive old alerts:**
   ```bash
   cd data/
   MONTH_AGO=$(date -d '30 days ago' +%Y-%m-%d)

   # Split alerts by age
   awk -v d="$MONTH_AGO" '$0 < d' alerts.jsonl > alerts_archive.jsonl
   awk -v d="$MONTH_AGO" '$0 >= d' alerts.jsonl > alerts_current.jsonl

   # Replace current with recent only
   mv alerts_current.jsonl alerts.jsonl
   gzip alerts_archive.jsonl
   ```

2. **Performance review:**
   - How many actionable alerts this month?
   - How many false positives?
   - Should thresholds be adjusted?

**Success Criteria:** Monthly tasks completed, system optimized

---

## 6. Troubleshooting

### 6.1 Scanner Won't Start

**Symptoms:** Error when running `python scanner.py`

**Solutions:**

1. **Missing dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Python version too old:**
   ```bash
   python --version  # Should be 3.9+
   ```

3. **Permission errors:**
   ```bash
   chmod +x scanner.py
   ```

4. **Port conflicts (if any):**
   - Kill existing scanner process
   - Check no other instance running

---

### 6.2 No Markets Returned / API Errors

**Symptoms:** "No markets returned from API" or connection errors

**Solutions:**

1. **Check internet connection:**
   ```bash
   ping -c 3 polymarket.com
   ```

2. **Test API directly:**
   ```bash
   curl https://clob.polymarket.com/sampling-markets
   ```

3. **Wait and retry:**
   - Polymarket APIs may be temporarily down
   - Wait 5-10 minutes
   - Try again

4. **Check proxy settings (if applicable):**
   - Ensure no firewall blocking
   - Check corporate network restrictions

---

### 6.3 Too Many Alerts (Noise)

**Symptoms:** Hundreds of alerts, mostly irrelevant

**Solutions:**

1. **Increase thresholds in config.py:**
   ```python
   LARGE_TRADE_MIN_USD = 2000       # Was 1000
   WHALE_TRADE_MIN_USD = 10000      # Was 5000
   MIN_MARKET_VOLUME = 25000        # Was 5000
   ```

2. **Disable INFO level:**
   ```python
   SHOW_INFO_ALERTS = False
   ```

3. **Focus on quality markets:**
   ```python
   MAX_MARKETS_TO_SCAN = 50         # Was 100
   ```

---

### 6.4 Too Few Alerts (Missing Opportunities)

**Symptoms:** No alerts for hours/days

**Solutions:**

1. **Lower thresholds in config.py:**
   ```python
   LARGE_TRADE_MIN_USD = 500        # Was 1000
   WHALE_TRADE_MIN_USD = 2000       # Was 5000
   MIN_MARKET_VOLUME = 1000         # Was 5000
   ```

2. **Enable all alert levels:**
   ```python
   SHOW_INFO_ALERTS = True
   SHOW_WARNING_ALERTS = True
   ```

3. **Scan more markets:**
   ```python
   MAX_MARKETS_TO_SCAN = 200        # Was 100
   ```

---

### 6.5 Scanner Crashes/Stops Unexpectedly

**Symptoms:** Process exits, no longer running

**Solutions:**

1. **Check error logs:**
   ```bash
   tail -100 scanner.log
   ```

2. **Common causes:**
   - Out of memory → Reduce MAX_MARKETS_TO_SCAN
   - Network timeout → Increase timeout in polymarket_api.py
   - Rate limiting → Increase SCAN_INTERVAL

3. **Auto-restart script (optional):**
   ```bash
   # Create restart_scanner.sh
   cat > restart_scanner.sh <<'EOF'
   #!/bin/bash
   while true; do
     python scanner.py
     echo "Scanner crashed, restarting in 30 seconds..."
     sleep 30
   done
   EOF

   chmod +x restart_scanner.sh
   nohup ./restart_scanner.sh > scanner.log 2>&1 &
   ```

---

## 7. Performance Review

### 7.1 Weekly Performance Check

**When:** Every Sunday during maintenance

**Metrics to Track:**

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Alert accuracy | >60% actionable | Manual review of alerts |
| Whale wallet discoveries | 2-5 per week | Check whale_wallets.json |
| Uptime | >95% | Check logs for gaps |
| False positives | <40% | Review non-actionable alerts |

**Process:**

1. **Calculate accuracy:**
   ```
   Actionable alerts ÷ Total alerts × 100 = Accuracy %

   Example:
   15 actionable ÷ 30 total × 100 = 50%
   ```

2. **Review discoveries:**
   - How many new whale wallets?
   - Any appearing in multiple markets?
   - Trade values increasing/decreasing?

3. **Assess uptime:**
   ```bash
   # Check for time gaps in alerts
   awk '{print $1}' data/alerts.jsonl | \
     awk -F'T' '{print $1}' | \
     sort | uniq -c
   ```

4. **Document findings:**
   ```bash
   cat >> data/weekly_review.txt <<EOF

   === Week $(date +%Y-%m-%d) ===
   Total alerts: [NUMBER]
   Actionable: [NUMBER] ([PERCENT]%)
   New whales: [NUMBER]
   Uptime: [PERCENT]%
   Adjustments needed: [NOTES]
   EOF
   ```

---

### 7.2 Threshold Optimization

**When:** If accuracy <60% or false positives >40%

**Process:**

1. **Identify problem area:**
   - Too many trade alerts → Increase LARGE_TRADE_MIN_USD
   - Too many price alerts → Increase RAPID_PRICE_CHANGE_PERCENT
   - Too many volume alerts → Increase VOLUME_SPIKE_MULTIPLIER

2. **Make ONE change at a time:**
   ```bash
   # Edit config.py
   nano config.py

   # Change only one threshold
   # Save and restart scanner
   ```

3. **Monitor for 3-7 days**

4. **Measure improvement:**
   - Alert count change
   - Accuracy change
   - Still catching important events?

5. **Repeat until optimized**

**Example adjustment log:**
```
2026-01-04: Increased LARGE_TRADE_MIN_USD from 1000 to 1500
            Result: Alerts reduced from 50/day to 30/day
            Accuracy: Improved from 55% to 70%

2026-01-11: Increased MIN_MARKET_VOLUME from 5000 to 10000
            Result: Focused on liquid markets only
            Accuracy: Improved from 70% to 80%
```

---

## 8. Phase 2 Readiness

### 8.1 Phase 2 Prerequisites

**You're ready for Phase 2 when:**

- [ ] Scanner has run for at least 2 weeks
- [ ] Collected at least 10 whale wallet addresses
- [ ] Have >100 total alerts logged
- [ ] Alert accuracy is >60%
- [ ] You understand your config.py settings
- [ ] Data backup process is working
- [ ] You've identified at least 3 interesting markets

---

### 8.2 Data Required for Phase 2

**Checklist:**

- [ ] `whale_wallets.json` has at least 10 entries
- [ ] `alerts.jsonl` has substantial history
- [ ] You have notes on which wallets seem successful
- [ ] You've observed some wallets in multiple markets
- [ ] You can identify at least 5 wallets worth tracking

**Preparation:**

1. **Audit whale wallets:**
   ```bash
   cat data/whale_wallets.json | \
     python -m json.tool | \
     grep "address"
   ```

2. **Create priority list:**
   - Which wallets appeared most often?
   - Which had highest trade values?
   - Which markets did they trade in?

3. **Document for Phase 2:**
   ```bash
   cat > data/phase2_candidates.txt <<EOF
   Wallets to track in Phase 2:

   1. 0x742d35C... - Discovered [DATE] - $7500 trade
      Markets: [LIST]

   2. 0xabc123... - Discovered [DATE] - $12000 trade
      Markets: [LIST]

   [etc.]
   EOF
   ```

---

### 8.3 Phase 2 Transition

**When ready to move to Phase 2:**

1. **Final Phase 1 backup:**
   ```bash
   tar -czf backups/phase1_final_$(date +%Y%m%d).tar.gz data/
   ```

2. **Generate Phase 1 summary report:**
   - Total runtime
   - Total alerts
   - Whale wallets discovered
   - Most active markets
   - Lessons learned

3. **Keep Phase 1 running:**
   - Don't stop the scanner
   - Phase 2 will augment, not replace

4. **Prepare requirements for Phase 2:**
   - List of wallets to track
   - Performance metrics to calculate
   - Dashboard requirements

---

## Appendix A: Quick Reference Commands

### Start Scanner (Foreground)
```bash
cd /home/user/me/polymarket_scanner && python scanner.py
```

### Start Scanner (Background)
```bash
cd /home/user/me/polymarket_scanner && nohup python scanner.py > scanner.log 2>&1 & echo $! > scanner.pid
```

### Stop Scanner (Background)
```bash
kill $(cat /home/user/me/polymarket_scanner/scanner.pid) && rm /home/user/me/polymarket_scanner/scanner.pid
```

### Check if Running
```bash
ps aux | grep scanner.py
```

### View Recent Alerts
```bash
tail -n 20 /home/user/me/polymarket_scanner/data/alerts.jsonl
```

### Count Today's Alerts
```bash
grep "$(date +%Y-%m-%d)" /home/user/me/polymarket_scanner/data/alerts.jsonl | wc -l
```

### View Whale Wallets
```bash
cat /home/user/me/polymarket_scanner/data/whale_wallets.json
```

### Daily Backup
```bash
cd /home/user/me/polymarket_scanner && tar -czf backups/scanner_data_$(date +%Y%m%d).tar.gz data/
```

---

## Appendix B: Sample Daily Workflow

**Morning (9 AM):**
1. Start scanner in background
2. Check yesterday's alerts
3. Review any critical alerts from overnight

**Midday (12 PM):**
1. Check scanner is still running
2. Review morning alerts
3. Investigate any critical items

**Evening (6 PM):**
1. Review afternoon alerts
2. Check whale wallet discoveries
3. Update notes

**Night (11 PM):**
1. Create daily summary
2. Review all critical alerts
3. Prepare watchlist for tomorrow
4. Keep scanner running overnight (or stop if preferred)

---

## Appendix C: Red Flags

**Stop and investigate immediately if:**

- Scanner hasn't logged alerts in 6+ hours (may be crashed)
- Suddenly seeing 100+ alerts per hour (threshold too low)
- Same market appears in 10+ consecutive alerts (possible bug)
- Disk space below 500MB (risk of data loss)
- Wallet appears in 50+ trades instantly (possible spam)

**These indicate configuration or system issues that need attention.**

---

## Version History

**v1.0 (2026-01-04):**
- Initial SOP for Phase 1 scanner
- Daily, weekly, monthly procedures
- Alert response protocols
- Troubleshooting guide
- Phase 2 readiness criteria

---

**END OF SOP**

For questions or issues not covered here, review:
- README.md (feature overview)
- SETUP_GUIDE.md (installation details)
- PROJECT_SUMMARY.md (technical architecture)
