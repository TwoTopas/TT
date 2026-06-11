#!/bin/bash
# Helper: browse a Gumroad category page and extract product listings
# Usage: bash scripts/browse-gumroad-category.sh
# 
# This is NOT a runnable script — it documents the browser workflow.
# The browser toolset auto-fills the commands; use these as reference.

# Step 1: Navigate to category page
# browser_navigate(url="https://gumroad.com/software-development/software-and-plugins")

# Step 2: Extract all product cards with prices and ratings
# browser_console(expression="document.body.innerText.substring(0, 8000)")

# Step 3: Look for patterns in the output:
# Product name, $Price, Rating (N ratings)
# e.g. "Supercharge $20+ 5.0 (254)"

# Step 4: For deeper inspection of a single product:
# browser_navigate(url="https://SELLER.gumroad.com/l/SLUG")
# browser_console(expression="document.body?.innerText?.substring(0, 3000) || 'empty'")

echo "See browser workflow in SKILL.md"
echo "To run: use browser_navigate + browser_console in your agent session"
