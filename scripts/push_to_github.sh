#!/bin/bash

# Script to push FlowForge code to GitHub and trigger CI/CD build
# This script handles authentication and push to GitHub

set -e

echo "=========================================="
echo "FlowForge - Push to GitHub"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

cd "$(dirname "$0")/.."

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}Error: Not a git repository${NC}"
    exit 1
fi

# Check remote
REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
if [ -z "$REMOTE" ]; then
    echo -e "${RED}Error: No remote configured${NC}"
    exit 1
fi

echo "Repository: $REMOTE"
echo ""

# Check if there are commits to push
LOCAL=$(git rev-parse @ 2>/dev/null)
REMOTE_REV=$(git rev-parse @{u} 2>/dev/null || echo "")

if [ -z "$REMOTE_REV" ]; then
    echo -e "${YELLOW}No remote tracking branch found${NC}"
    echo "This appears to be the first push."
    echo ""
fi

# Check current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Current branch: $CURRENT_BRANCH"
echo ""

# Show commits to be pushed
echo "Commits to push:"
git log origin/${CURRENT_BRANCH}..HEAD --oneline 2>/dev/null || git log --oneline -5
echo ""

# Check authentication method
if [[ "$REMOTE" == *"git@github.com"* ]]; then
    echo "Using SSH authentication"
    echo ""
    
    # Test SSH connection
    if ssh -o StrictHostKeyChecking=no -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
        echo -e "${GREEN}✓ SSH authentication successful${NC}"
    else
        echo -e "${YELLOW}⚠ SSH authentication may need setup${NC}"
        echo ""
        echo "Options:"
        echo "1. Run: bash scripts/setup_github_key.sh"
        echo "2. Or use HTTPS with Personal Access Token"
        echo ""
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
else
    echo "Using HTTPS authentication"
    echo "You will be prompted for credentials"
    echo ""
fi

# Ask for confirmation
echo "Ready to push to GitHub?"
echo "This will trigger the CI/CD build pipeline."
echo ""
read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Push cancelled."
    exit 0
fi

# Push to GitHub
echo ""
echo "Pushing to GitHub..."
echo ""

if git push -u origin ${CURRENT_BRANCH} 2>&1; then
    echo ""
    echo -e "${GREEN}✓ Successfully pushed to GitHub!${NC}"
    echo ""
    echo "GitHub Actions build should start automatically."
    echo "View build status at:"
    echo "https://github.com/Franklin-security/FlowForge/actions"
    echo ""
else
    echo ""
    echo -e "${RED}✗ Push failed${NC}"
    echo ""
    echo "Possible solutions:"
    echo "1. Set up SSH key: bash scripts/setup_github_key.sh"
    echo "2. Use Personal Access Token for HTTPS"
    echo "3. Check repository permissions"
    echo ""
    exit 1
fi

