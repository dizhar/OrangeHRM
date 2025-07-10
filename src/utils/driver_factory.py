import threading
import time
import tempfile
import random
import os
import shutil
from selenium import webdriver
from src.utils.config_reader import ConfigReader


class DriverFactory:
    @staticmethod
    def get_driver(browser_name=None, headless=None):
        """Set up and return a WebDriver instance"""
        # Get configuration
        browser_config = ConfigReader.get_browser_config()
        wait_times = ConfigReader.get_wait_times()
        
        browser_name = (browser_name or browser_config['browser']).lower()
        headless = headless if headless is not None else browser_config['headless']
        
        # Check if running in Docker
        is_docker = os.path.exists('/.dockerenv')
        
        if browser_name == "chrome":
            driver = DriverFactory._create_chrome_driver(headless, is_docker)
        elif browser_name == "firefox":
            driver = DriverFactory._create_firefox_driver(headless, is_docker)
        else:
            raise ValueError(f"Browser '{browser_name}' is not supported")
        
        # Set window size and timeouts
        if is_docker or headless:
            driver.set_window_size(1920, 1080)
        else:
            driver.maximize_window()
            
        driver.implicitly_wait(wait_times['implicit_wait'])
        return driver
    
    @staticmethod
    def _create_chrome_driver(headless, is_docker):
        """Create Chrome WebDriver with appropriate options"""
        options = webdriver.ChromeOptions()
        
        # Force headless in Docker or if requested
        if is_docker or headless:
            options.add_argument("--headless")
        
        # Basic Chrome options
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        
        # Performance optimizations
        DriverFactory._add_performance_options(options)
        
        # Handle parallel execution
        if is_docker:
            DriverFactory._configure_docker_chrome(options)
        else:
            DriverFactory._configure_local_chrome(options)
        
        return webdriver.Chrome(options=options)
    
    @staticmethod
    def _create_firefox_driver(headless, is_docker):
        """Create Firefox WebDriver with appropriate options"""
        options = webdriver.FirefoxOptions()
        
        if is_docker or headless:
            options.add_argument("--headless")
        
        return webdriver.Firefox(options=options)
    
    @staticmethod
    def _add_performance_options(options):
        """Add performance optimization arguments to Chrome"""
        performance_args = [
            "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding",
            "--disable-backgrounding-occluded-windows",
            "--disable-features=TranslateUI",
            "--disable-ipc-flooding-protection",
            "--disable-web-security",
            "--disable-logging",
            "--memory-pressure-off",
            "--max_old_space_size=4096"
        ]
        
        for arg in performance_args:
            options.add_argument(arg)
    
    @staticmethod
    def _configure_docker_chrome(options):
        """Configure Chrome for Docker environment"""
        # Generate unique debugging port
        unique_port = DriverFactory._generate_unique_port()
        options.add_argument(f"--remote-debugging-port={unique_port}")
        
        # Add Docker-specific optimizations
        docker_args = [
            "--disable-plugins",
            "--disable-images",
            "--disable-features=VizDisplayCompositor"
        ]
        
        for arg in docker_args:
            options.add_argument(arg)
        
        # Stagger startup to avoid conflicts
        time.sleep(random.uniform(0.5, 1.5))
        print(f"Docker mode: Using debug port {unique_port}")
    
    @staticmethod
    def _configure_local_chrome(options):
        """Configure Chrome for local environment"""
        # Generate unique identifiers
        unique_port = DriverFactory._generate_unique_port()
        unique_id = DriverFactory._generate_unique_id()
        
        options.add_argument(f"--remote-debugging-port={unique_port}")
        
        # Create unique user data directory
        user_data_dir = os.path.join(tempfile.gettempdir(), f"chrome_user_data_{unique_id}")
        
        # Clean up existing directory
        if os.path.exists(user_data_dir):
            shutil.rmtree(user_data_dir, ignore_errors=True)
        
        os.makedirs(user_data_dir, exist_ok=True)
        options.add_argument(f"--user-data-dir={user_data_dir}")
        
        # Stagger startup
        time.sleep(random.uniform(0.5, 2.0))
        
        print(f"Local mode: Using user data dir: {user_data_dir}")
        print(f"Local mode: Using debug port: {unique_port}")
    
    @staticmethod
    def _generate_unique_port():
        """Generate a unique debugging port"""
        thread_id = threading.current_thread().ident
        timestamp = int(time.time() * 1000000)
        return 9222 + (hash(f"{thread_id}_{timestamp}") % 10000)
    
    @staticmethod
    def _generate_unique_id():
        """Generate a unique identifier for Chrome instances"""
        thread_id = threading.current_thread().ident
        timestamp = int(time.time() * 1000000)
        random_suffix = random.randint(10000, 99999)
        process_id = os.getpid()
        
        return f"{process_id}_{thread_id}_{timestamp}_{random_suffix}"