FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget curl unzip xvfb \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libxcomposite1 libxdamage1 \
    libxrandr2 libgbm1 libasound2 libpangocairo-1.0-0 libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install chromium

CMD ["python", "main.py"]
