#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run preprocessing to generate the pickle file
python recommendation/preprocess_data.py

# Collect static files
python manage.py collectstatic --noinput --clear
