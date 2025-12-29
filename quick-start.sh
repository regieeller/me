#!/bin/bash

# Quick start script for X Viral Post Detector
# Run this after initial setup to quickly launch the detector

echo "🔥 X Viral Post Detector - Quick Start"
echo "======================================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup first:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    echo "  playwright install chromium"
    exit 1
fi

# Activate venv
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Run the detector
echo "🚀 Running viral post detector..."
echo ""
python3 find_viral_posts.py

# Check if report was generated
TODAY=$(date +%Y-%m-%d)
REPORT_FILE="reports/${TODAY}.md"

if [ -f "$REPORT_FILE" ]; then
    echo ""
    echo "======================================"
    echo "✅ Report generated successfully!"
    echo "📄 Location: $REPORT_FILE"
    echo ""
    echo "Opening report..."
    open "$REPORT_FILE" 2>/dev/null || cat "$REPORT_FILE"
else
    echo "⚠️  No report generated. Check for errors above."
fi
