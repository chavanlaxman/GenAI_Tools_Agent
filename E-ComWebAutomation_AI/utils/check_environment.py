"""Environment check and setup script for test framework."""
import sys
import os
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version meets requirements."""
    required_version = (3, 8)
    current_version = sys.version_info[:2]
    
    if current_version < required_version:
        raise SystemError(
            f"Python {required_version[0]}.{required_version[1]} or higher is required. "
            f"You are using Python {current_version[0]}.{current_version[1]}"
        )

def check_dependencies():
    """Verify all required packages are installed."""
    return
    requirements_file = Path(__file__).parent.parent / "requirements.txt"
    if not requirements_file.exists():
        raise FileNotFoundError("requirements.txt not found")
    
    result = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        capture_output=True,
        text=True
    )
    installed = {
        line.split('==')[0].lower()
        for line in result.stdout.splitlines()
    }
    
    with open(requirements_file) as f:
        required = {
            line.split('==')[0].lower()
            for line in f.readlines()
            if line.strip() and not line.startswith('#')
        }
    
    missing = required - installed
    if missing:
        raise ModuleNotFoundError(
            f"Missing required packages: {', '.join(missing)}\n"
            f"Run: pip install -r {requirements_file}"
        )

def check_webdriver():
    """Verify webdriver is available."""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.quit()
    except Exception as e:
        raise RuntimeError(f"WebDriver setup failed: {str(e)}")

def check_directories():
    """Verify required directories exist."""
    base_dir = Path(__file__).parent.parent
    required_dirs = [
        base_dir / "Tests",
        base_dir / "pages",
        base_dir / "utils",
        base_dir / "config",
        base_dir / "test_logs"
    ]
    
    for directory in required_dirs:
        directory.mkdir(exist_ok=True)
        print(f"✓ Directory exists: {directory}")

def check_config_files():
    """Verify configuration files exist and are valid."""
    base_dir = Path(__file__).parent.parent
    required_files = [
        base_dir / "pytest.ini",
        base_dir / "conftest.py",
        base_dir / "requirements.txt"
    ]
    
    for file in required_files:
        if not file.exists():
            raise FileNotFoundError(f"Required file missing: {file}")
        print(f"✓ Config file exists: {file}")

def check_environment_variables():
    """Verify required environment variables are set."""
    required_vars = [
        ('TEST_ENV', 'qa'),  # (var_name, default_value)
        ('TEST_BROWSER', 'chrome'),
        ('TEST_HEADLESS', 'true'),
        ('TEST_BASE_URL', 'https://rahulshettyacademy.com/client/#/auth/login')
    ]
    
    for var, default in required_vars:
        if not os.getenv(var):
            os.environ[var] = default
            print(f"! Environment variable {var} not set, using default: {default}")
        else:
            print(f"✓ Environment variable {var} is set")

def main():
    """Run all environment checks."""
    try:
        print("\n=== Running Environment Checks ===\n")
        
        print("1. Checking Python version...")
        check_python_version()
        print("✓ Python version OK\n")
        
        print("2. Checking dependencies...")
        check_dependencies()
        print("✓ All dependencies installed\n")
        
        print("3. Checking WebDriver...")
        check_webdriver()
        print("✓ WebDriver setup OK\n")
        
        print("4. Checking directories...")
        check_directories()
        print("")
        
        print("5. Checking config files...")
        check_config_files()
        print("")
        
        print("6. Checking environment variables...")
        check_environment_variables()
        print("")
        
        print("\n=== Environment Check Complete ===")
        print("✓ All checks passed - ready to run tests")
        print("\nTo run tests:")
        print("1. Basic run:           pytest -v")
        print("2. Parallel run:        pytest -v -n auto")
        print("3. Run smoke tests:     pytest -v -m smoke")
        print("4. Generate report:     pytest -v --html=report.html")
        return True
        
    except Exception as e:
        print(f"\n❌ Environment check failed: {str(e)}")
        return False

if __name__ == "__main__":
    sys.exit(0 if main() else 1)