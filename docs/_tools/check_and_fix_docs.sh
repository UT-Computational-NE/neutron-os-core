#!/bin/bash
# Documentation quality check and fix script
# Run this before generating documents to ensure quality

echo "========================================="
echo "DOCUMENTATION QUALITY CHECK"
echo "========================================="

# Navigate to tools directory
cd "$(dirname "$0")"

# First, check for issues
echo ""
echo "Checking for documentation issues..."
python3 doc_quality_checker.py --verbose

# Ask if user wants to fix
read -p "Do you want to automatically fix the issues? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Applying fixes..."
    python3 doc_quality_checker.py --fix
    echo ""
    echo "Fixes applied! Regenerating documents..."
    python3 generate_all_docs.py
else
    echo "Skipping fixes. Documents may have quality issues."
fi