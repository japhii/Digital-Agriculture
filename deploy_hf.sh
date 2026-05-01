#!/bin/bash
echo "Resetting repository to fix LFS tracking for all binary files..."
rm -rf .git
git init

# Configure LFS BEFORE adding files
git lfs install
git lfs track "*.pkl"
git lfs track "*.h5"
git lfs track "*.keras"
git lfs track "*.zip"
git lfs track "*.pdf"
git lfs track "*.png"
git lfs track "*.jpg"
git lfs track "*.jpeg"
git lfs track "*.ico"
git lfs track "*.csv"
git add .gitattributes

# Add everything else
git add .
git commit -m "Initial commit with proper LFS tracking for all binaries"

# Setup remotes
git branch -M main

echo ""
echo "============================================================"
echo "Please enter your Hugging Face Access Token (Must have WRITE permissions):"
read -s HF_TOKEN

echo "Pushing the repository to Hugging Face (Space: MyAgrii-App)..."
git remote add space "https://j4phi:${HF_TOKEN}@huggingface.co/spaces/j4phi/MyAgrii-App"
git push -u space main --force
echo "Deployment initiated!"
