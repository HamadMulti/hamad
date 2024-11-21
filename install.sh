#!/bin/env bash

if [ ! -d ".envs" ]; then
    echo "Creating virtual environment..."
    python -m virtualenv .venv
fi

# shellcheck disable=SC1091
if source .venv/bin/activate; then
    echo "Virtual environment activated."
else
    echo "Failed to activate virtual environment. Exiting..."
    exit 1
fi

if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Exiting..."
    exit 1
fi

echo "Applying database migrations..."
python manage.py makemigrations
python manage.py makemigrations store
python manage.py migrate

echo "Seeding products to Database..."
python manage.py seed_db_api

echo "Installing tailwind dependencies ..."
python manage.py tailwind install

echo "Script completed successfully."
exit 0