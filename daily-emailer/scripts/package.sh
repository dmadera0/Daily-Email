#!/bin/bash
# Packages the Lambda function and its dependencies into a zip file.
# Run this from the project root: bash scripts/package.sh

set -e  # Exit immediately if any command fails

echo "→ Cleaning old build artifacts..."
rm -rf build/
rm -f daily-emailer.zip

echo "→ Installing dependencies into build/..."
mkdir -p build
pip3 install -r lambda/requirements.txt -t build/ --quiet

echo "→ Copying Lambda source files..."
cp lambda/*.py build/

echo "→ Creating deployment zip..."
cd build
zip -r ../daily-emailer.zip . -x "*.pyc" -x "*/__pycache__/*"
cd ..

echo "✓ Package ready: daily-emailer.zip ($(du -sh daily-emailer.zip | cut -f1))"
