#!/bin/bash

# Build Docker image
echo "Building Docker image..."
if docker build -t percepto-test .; then
    echo "Docker image 'percepto-test' built successfully!"
    
    # Create reports directory
    mkdir -p reports/allure-results reports/screenshots
    
    # Check TerminalX website availability
    echo "Checking TerminalX website availability..."
    if ! curl -s -m 10 https://opensource-demo.orangehrmlive.com> /dev/null; then
        echo "Error: TerminalX website is not accessible!"
        exit 1
    fi
    
    # Run tests with volume mount
    echo "Running tests..."
    if ! docker run --rm -v $(pwd)/reports:/app/reports percepto-test; then
        echo "Tests failed or timed out!"
    else
        echo "Tests completed!"
    fi
    
    # Run Allure report server using Docker Compose
    echo "Starting Allure report server..."
    echo "🌐 Allure reports will be available at: http://localhost:4040"
    if docker compose up --build allure; then
        echo "Allure report server started successfully!"
    else
        echo "Failed to start Allure report server."
        echo "View HTML report at: reports/report.html"
    fi
else
    echo "Docker build failed!"
    exit 1
fi