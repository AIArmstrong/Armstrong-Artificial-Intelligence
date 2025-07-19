#!/bin/bash
# Install dependencies for Supabase integration

echo "🔧 Installing AAI Supabase Dependencies"

# Check if running in WSL/Ubuntu
if command -v apt &> /dev/null; then
    echo "📦 Installing system packages..."
    sudo apt update
    sudo apt install -y python3-pip python3-venv python3-dev libpq-dev
fi

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv supabase/venv

# Activate and install Python packages
echo "📚 Installing Python packages..."
source supabase/venv/bin/activate
pip install psycopg2-binary python-dotenv

echo "✅ Dependencies installed successfully!"
echo ""
echo "To activate the environment, run:"
echo "source supabase/venv/bin/activate"
echo ""
echo "Then you can run:"
echo "python3 supabase/scripts/upload_migration_data.py"