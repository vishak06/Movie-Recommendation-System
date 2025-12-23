#!/bin/bash
# Build script for deployment platforms (Render, Railway, etc.)

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running preprocessing to generate similarity data..."
python recommendation/preprocess_data.py

echo "Build complete!"
