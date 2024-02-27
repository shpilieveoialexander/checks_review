#! /usr/bin/env sh

# Create DB
python /backend/db/init_db.py

# Run migrations
alembic upgrade head

# Create initial data
python /backend/db/initial_data.py

echo pre_start.sh has worked
