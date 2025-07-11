# Use Python base image
FROM python:3.11-slim

# Install system dependencies required for Playwright and Chromium
RUN apt-get update && apt-get install -y \
    wget curl unzip xvfb \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm1 \
    libasound2 libpangocairo-1.0-0 libgtk-3-0 \
    libx11-xcb1 libxext6 libxfixes3 libxrender1 libxcb1 \
    fonts-liberation libappindicator3-1 lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and Chromium
RUN playwright install chromium

# Default command
CMD ["python", "main.py"]
