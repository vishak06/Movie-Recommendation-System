#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run preprocessing to generate the pickle file
python recommendation/preprocess_data.py

# Collect static files (skip if database is not available)
python manage.py collectstatic --noinput --clear 2>/dev/null || echo "Skipping collectstatic due to missing database"
