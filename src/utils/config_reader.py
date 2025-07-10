import configparser
import os
from pathlib import Path

class ConfigReader:
    _config = None
    
    @classmethod
    def get_config(cls):
        """Get the configuration, loading it if necessary"""
        if cls._config is None:
            cls._config = cls.read_config()
        return cls._config
    
    @staticmethod
    def read_config():
        """Read and return the configuration from config.ini"""
        config = configparser.ConfigParser()
        
        # Get the absolute path to the config file
        base_dir = Path(__file__).parent.parent
        config_path = os.path.join(base_dir, 'config', 'config.ini')
        
        # Read the config file
        config.read(config_path)
        return config
    
    @staticmethod
    def get_base_url():
        """Get OrangeHRM base URL"""
        config = ConfigReader.read_config()
        return config.get('OrangeHRM', 'base_url', fallback='https://opensource-demo.orangehrmlive.com')
    
    @staticmethod
    def get_browser_config():
        """Get the browser configuration"""
        config = ConfigReader.read_config()
        return {
            'browser': config.get('Browsers', 'browser'),
            'headless': config.getboolean('Browsers', 'headless')
        }
    
    @staticmethod
    def get_wait_times():
        """Get the wait times configuration"""
        config = ConfigReader.read_config()
        return {
            'implicit_wait': config.getint('Test', 'implicit_wait'),
            'explicit_wait': config.getint('Test', 'explicit_wait')
        }

    @staticmethod
    def get_orangehrm_config():
        """Get OrangeHRM specific configuration"""
        config = ConfigReader.read_config()
        return {
            'base_url': config.get('OrangeHRM', 'base_url'),
            'default_password': config.get('OrangeHRM', 'default_password'),
            'admin_username': config.get('OrangeHRM', 'admin_username'),
            'admin_password': config.get('OrangeHRM', 'admin_password')
        }