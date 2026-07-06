# backend/Dockerfile

FROM python:3.12-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY backend/app /app/app
COPY backend/data /app/data

# If your backend relies on the ML folder, you must copy it into the image too
COPY ml /app/ml 

# ADD THIS LINE:
COPY backend/download_model.py /app/download_model.py

EXPOSE 8000
CMD ["sh", "-c", "python download_model.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]