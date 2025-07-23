#!/bin/bash

echo "GitHub CLI Authentication Setup"
echo "==============================="
echo ""
echo "This will authenticate GitHub CLI with your AIArmstrong account."
echo ""

# Use the full path to gh
GH_PATH="$HOME/.local/bin/gh"

echo "Starting GitHub authentication..."
$GH_PATH auth login --git-protocol https --web

echo ""
echo "After authentication, let's verify the connection:"
$GH_PATH auth status