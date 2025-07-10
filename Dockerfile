# Use Python image with platform specification
FROM --platform=linux/amd64 python:3.11-slim

# Install Chrome dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Set environment variables
ENV HEADLESS=true
ENV ENVIRONMENT=prod
ENV PYTHONUNBUFFERED=1

# Run tests with allure reporting
CMD ["python", "-m", "pytest", "src/tests/ui/", "--alluredir=reports/allure-results", "-v", "-s", "--tb=short"]