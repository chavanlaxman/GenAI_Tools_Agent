"""Configuration management for test framework."""
import os
import json
from pathlib import Path

class TestConfig:
    """Test framework configuration handler."""
    
    def __init__(self):
        self._config = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from config files and environment."""
        # Base config
        base_config = {
            'browser': {
                'headless': True,
                'viewport_width': 1920,
                'viewport_height': 1080,
                'timeout': 10
            },
            'test': {
                'parallel': True,
                'max_workers': 'auto',
                'rerun_failures': True,
                'max_reruns': 2
            },
            'reporting': {
                'screenshots_on_failure': True,
                'video_recording': False,
                'excel_report': True,
                'html_report': True
            },
            'logging': {
                'console_level': 'INFO',
                'file_level': 'DEBUG',
                'capture_stdout': True
            }
        }
        
        # Load environment-specific config
        env = os.getenv('TEST_ENV', 'qa').lower()
        env_config_path = Path(__file__).parent.parent / f"config/{env}_config.json"
        
        if env_config_path.exists():
            with open(env_config_path) as f:
                env_config = json.load(f)
                base_config.update(env_config)
        
        # Override with environment variables
        self._update_from_env(base_config)
        self._config = base_config
    
    def _update_from_env(self, config):
        """Update config with environment variables."""
        env_mapping = {
            'TEST_HEADLESS': ('browser', 'headless'),
            'TEST_VIEWPORT_WIDTH': ('browser', 'viewport_width'),
            'TEST_VIEWPORT_HEIGHT': ('browser', 'viewport_height'),
            'TEST_TIMEOUT': ('browser', 'timeout'),
            'TEST_PARALLEL': ('test', 'parallel'),
            'TEST_MAX_WORKERS': ('test', 'max_workers'),
            'TEST_RERUN_FAILURES': ('test', 'rerun_failures'),
            'TEST_MAX_RERUNS': ('test', 'max_reruns'),
            'TEST_SCREENSHOTS_ON_FAILURE': ('reporting', 'screenshots_on_failure'),
            'TEST_VIDEO_RECORDING': ('reporting', 'video_recording'),
            'TEST_EXCEL_REPORT': ('reporting', 'excel_report'),
            'TEST_HTML_REPORT': ('reporting', 'html_report'),
            'TEST_CONSOLE_LOG_LEVEL': ('logging', 'console_level'),
            'TEST_FILE_LOG_LEVEL': ('logging', 'file_level'),
            'TEST_CAPTURE_STDOUT': ('logging', 'capture_stdout')
        }
        
        for env_var, (section, key) in env_mapping.items():
            if env_var in os.environ:
                value = os.getenv(env_var)
                # Convert string to appropriate type
                if isinstance(config[section][key], bool):
                    value = value.lower() == 'true'
                elif isinstance(config[section][key], int):
                    value = int(value)
                config[section][key] = value
    
    def get(self, section, key=None):
        """
        Get configuration value.
        Args:
            section (str): Configuration section
            key (str, optional): Specific key in section
        Returns:
            Value from configuration
        """
        if key:
            return self._config[section][key]
        return self._config[section]
    
    @property
    def browser(self):
        """Get browser configuration."""
        return self._config['browser']
    
    @property
    def test(self):
        """Get test configuration."""
        return self._config['test']
    
    @property
    def reporting(self):
        """Get reporting configuration."""
        return self._config['reporting']
    
    @property
    def logging(self):
        """Get logging configuration."""
        return self._config['logging']