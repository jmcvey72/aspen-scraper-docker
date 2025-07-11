# Use Python base image
FROM python:3.11-slim

# Install dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget curl unzip xvfb \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libxcomposite1 libxdamage1 \
    libxrandr2 libgbm1 libasound2 libpangocairo-1.0-0 libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Set workdir and copy files
WORKDIR /app
COPY . .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Install Chromium for Playwright
RUN playwright install chromium

# Command to run your scraper
CMD ["python", "main.py"]
