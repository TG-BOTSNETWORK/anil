# Use Node as base for frontend build
FROM node:20-alpine AS frontend-build

WORKDIR /app/frontend

# Copy frontend files
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Use Python base for backend
FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./

# Copy built frontend into backend's static folder
# (Assuming your FastAPI serves static files from /app/static)
RUN mkdir -p /app/static
COPY --from=frontend-build /app/frontend/build /app/static

# Expose backend port
EXPOSE 8000

# Set environment variables (optional, can also use .env)
ENV DATABASE_URL=postgresql://postgres:postgres@db:5432/ai_news
ENV OPENAI_API_KEY=your_openai_key

# Run FastAPI backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]