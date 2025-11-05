"""Test runner script with different execution modes."""
import os
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from utils.run_configs import CONFIGS
from utils.check_environment import main as check_env

def setup_environment(config_name):
    """Set up environment variables for the test run."""
    config = CONFIGS.get(config_name)
    if not config:
        raise ValueError(f"Unknown configuration: {config_name}")
    
    # Set environment variables
    for key, value in config["env_vars"].items():
        os.environ[key] = str(value)

def create_run_directory():
    """Create timestamped directory for test artifacts."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path("test_logs") / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir

def run_tests(config_name, additional_args=None):
    """
    Run tests with specified configuration.
    
    Args:
        config_name (str): Name of the configuration to use
        additional_args (list): Additional pytest arguments
    """
    # Check environment first
    if not check_env():
        sys.exit(1)
    
    # Get configuration
    config = CONFIGS.get(config_name)
    if not config:
        print(f"Error: Unknown configuration '{config_name}'")
        print(f"Available configurations: {', '.join(CONFIGS.keys())}")
        sys.exit(1)
    
    # Create run directory
    run_dir = create_run_directory()
    
    # Setup environment
    setup_environment(config_name)
    
    # Build command
    cmd = [sys.executable, "-m", "pytest"]
    cmd.extend(config["pytest_args"])
    if additional_args:
        cmd.extend(additional_args)
    
    # Print run info
    print("\n=== Test Run Information ===")
    print(f"Configuration: {config_name}")
    print(f"Description: {config['description']}")
    print(f"Run Directory: {run_dir}")
    print(f"Command: {' '.join(cmd)}")
    print("===========================\n")
    
    # Run tests
    try:
        result = subprocess.run(cmd)
        return result.returncode
    except KeyboardInterrupt:
        print("\nTest execution interrupted by user")
        return 130
    except Exception as e:
        print(f"\nError running tests: {str(e)}")
        return 1

def list_configurations():
    """Print available test configurations."""
    print("\nAvailable Test Configurations:")
    print("-----------------------------")
    for name, config in CONFIGS.items():
        print(f"\n{name}:")
        print(f"  Description: {config['description']}")
        print(f"  Arguments: {' '.join(config['pytest_args'])}")
        print("  Environment:")
        for key, value in config['env_vars'].items():
            print(f"    {key}={value}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Test Runner")
    parser.add_argument(
        "config",
        choices=list(CONFIGS.keys()) + ["list"],
        help="Test configuration to use or 'list' to see available configs"
    )
    parser.add_argument(
        "pytest_args",
        nargs="*",
        help="Additional pytest arguments"
    )
    
    args = parser.parse_args()
    
    if args.config == "list":
        list_configurations()
        return 0
    
    return run_tests(args.config, args.pytest_args)

if __name__ == "__main__":
    sys.exit(main())