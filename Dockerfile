# Use the official Playwright image with all necessary dependencies
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Set working directory inside the container
WORKDIR /app

# Copy your project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install browser dependencies for Playwright (Chromium, etc.)
RUN playwright install --with-deps

# Set the default command to run your scraper
CMD ["python", "main.py"]
