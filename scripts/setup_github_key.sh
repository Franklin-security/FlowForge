#!/bin/bash

# Script to generate GitHub SSH key for CI/CD automation
# This script generates an SSH key pair for GitHub authentication

set -e

echo "=========================================="
echo "GitHub SSH Key Setup for CI/CD"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if key already exists
KEY_NAME="github_deploy_key"
KEY_PATH="$HOME/.ssh/${KEY_NAME}"

if [ -f "$KEY_PATH" ]; then
    echo -e "${YELLOW}Warning: Key already exists at $KEY_PATH${NC}"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Exiting without changes."
        exit 0
    fi
    rm -f "$KEY_PATH" "$KEY_PATH.pub"
fi

# Generate SSH key
echo "Generating SSH key pair..."
ssh-keygen -t ed25519 -C "ci-cd-deploy-key" -f "$KEY_PATH" -N ""

echo ""
echo -e "${GREEN}✓ SSH key pair generated successfully!${NC}"
echo ""

# Display public key
echo "=========================================="
echo "PUBLIC KEY (Add this to GitHub):"
echo "=========================================="
cat "$KEY_PATH.pub"
echo ""
echo "=========================================="
echo ""

# Instructions
echo "Next steps:"
echo "1. Copy the PUBLIC KEY above"
echo "2. Go to your GitHub repository → Settings → Deploy keys"
echo "3. Click 'Add deploy key'"
echo "4. Paste the public key"
echo "5. Check 'Allow write access' if needed"
echo "6. Save the key"
echo ""
echo "7. Copy the PRIVATE KEY below to GitHub Secrets:"
echo "   Repository → Settings → Secrets → Actions → New secret"
echo "   Name: DEPLOY_KEY"
echo ""
echo "=========================================="
echo "PRIVATE KEY (Add to GitHub Secrets):"
echo "=========================================="
cat "$KEY_PATH"
echo ""
echo "=========================================="
echo ""

# Save key location info
echo "Key files saved to:"
echo "  Public:  $KEY_PATH.pub"
echo "  Private: $KEY_PATH"
echo ""
echo -e "${GREEN}Setup complete!${NC}"
echo ""
echo "Important: Keep the private key secure and never commit it to the repository!"

