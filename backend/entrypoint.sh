#!/bin/sh

# Create .env
cat > /app/.env <<EOF
TMDB_READ_ACCESS_TOKEN=$TMDB_READ_ACCESS_TOKEN
DATABASE_URL=$DATABASE_URL
SECRET_KEY=$SECRET_KEY
EOF

# Download ML model if needed
python /app/download_model.py

# Start FastAPI
exec uvicorn app.main:app --host 0.0.0.0 --port 8000