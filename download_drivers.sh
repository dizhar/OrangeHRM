#!/bin/bash

# Script to download browser drivers using Chrome for Testing API

# Create directory for drivers
mkdir -p drivers

echo "Downloading ChromeDriver for Chrome 131..."

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if [[ "$(uname -m)" == "arm64" ]]; then
        # M1/M2 Mac
        echo "Downloading ChromeDriver for macOS ARM64..."
        curl -L "https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.85/mac-arm64/chromedriver-mac-arm64.zip" -o chromedriver.zip
    else
        # Intel Mac
        echo "Downloading ChromeDriver for macOS x64..."
        curl -L "https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.85/mac-x64/chromedriver-mac-x64.zip" -o chromedriver.zip
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "Downloading ChromeDriver for Linux x64..."
    curl -L "https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.85/linux64/chromedriver-linux64.zip" -o chromedriver.zip
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    echo "Downloading ChromeDriver for Windows x64..."
    curl -L "https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.85/win64/chromedriver-win64.zip" -o chromedriver.zip
fi

# Extract ChromeDriver
if [[ -f "chromedriver.zip" ]]; then
    unzip -o chromedriver.zip -d drivers/
    rm chromedriver.zip
    
    # Find the chromedriver executable and move it to the drivers directory
    find drivers/ -name "chromedriver" -type f -exec mv {} drivers/ \;
    
    # Clean up any extra directories
    find drivers/ -type d -name "*chromedriver*" -exec rm -rf {} + 2>/dev/null || true
    
    # Make ChromeDriver executable
    chmod +x drivers/chromedriver
    
    echo "✅ ChromeDriver downloaded successfully"
else
    echo "❌ Failed to download ChromeDriver"
fi

# Get latest GeckoDriver (Firefox)
echo "Downloading latest GeckoDriver..."

# Get the latest release info
GECKO_API_URL="https://api.github.com/repos/mozilla/geckodriver/releases/latest"
GECKO_VERSION=$(curl -s "$GECKO_API_URL" | grep '"tag_name"' | sed -E 's/.*"([^"]+)".*/\1/')

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if [[ "$(uname -m)" == "arm64" ]]; then
        # M1/M2 Mac
        GECKO_URL="https://github.com/mozilla/geckodriver/releases/download/${GECKO_VERSION}/geckodriver-${GECKO_VERSION}-macos-aarch64.tar.gz"
    else
        # Intel Mac
        GECKO_URL="https://github.com/mozilla/geckodriver/releases/download/${GECKO_VERSION}/geckodriver-${GECKO_VERSION}-macos.tar.gz"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    GECKO_URL="https://github.com/mozilla/geckodriver/releases/download/${GECKO_VERSION}/geckodriver-${GECKO_VERSION}-linux64.tar.gz"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    GECKO_URL="https://github.com/mozilla/geckodriver/releases/download/${GECKO_VERSION}/geckodriver-${GECKO_VERSION}-win64.zip"
fi

# Download GeckoDriver
if [[ -n "$GECKO_URL" ]]; then
    echo "Downloading GeckoDriver from: $GECKO_URL"
    
    if [[ "$GECKO_URL" == *".zip"* ]]; then
        curl -L "$GECKO_URL" -o geckodriver.zip
        unzip -o geckodriver.zip -d drivers/
        rm geckodriver.zip
    else
        curl -L "$GECKO_URL" -o geckodriver.tar.gz
        tar -xzf geckodriver.tar.gz -C drivers/
        rm geckodriver.tar.gz
    fi
    
    # Make GeckoDriver executable
    chmod +x drivers/geckodriver
    
    echo "✅ GeckoDriver downloaded successfully"
else
    echo "❌ Failed to determine GeckoDriver download URL"
fi

echo ""
echo "✅ Drivers downloaded to drivers/ directory"
echo "📁 Current drivers:"
ls -la drivers/

echo ""
echo "🔧 To use these drivers, either:"
echo "   1. Add ./drivers to your PATH"
echo "   2. Move drivers to /usr/local/bin/:"
echo "      sudo mv drivers/chromedriver /usr/local/bin/"
echo "      sudo mv drivers/geckodriver /usr/local/bin/"

# Test the drivers
echo ""
echo "🧪 Testing drivers..."
if [[ -f "drivers/chromedriver" ]]; then
    echo "ChromeDriver version: $(./drivers/chromedriver --version)"
else
    echo "❌ ChromeDriver not found"
fi

if [[ -f "drivers/geckodriver" ]]; then
    echo "GeckoDriver version: $(./drivers/geckodriver --version)"
else
    echo "❌ GeckoDriver not found"
fi