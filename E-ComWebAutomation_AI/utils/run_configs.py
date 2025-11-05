"""Test run configurations for different scenarios."""
import os
from pathlib import Path

# Base directory for test artifacts
ARTIFACTS_DIR = Path("test_logs")

# Test Run Configurations
CONFIGS = {
    "smoke": {
        "description": "Quick smoke test suite",
        "pytest_args": [
            "-v",
            "-m", "smoke",
            "--html=test_logs/smoke_test_report.html",
        ],
        "env_vars": {
            "TEST_ENV": "qa",
            "TEST_HEADLESS": "true"
        }
    },
    "regression": {
        "description": "Full regression test suite",
        "pytest_args": [
            "-v",
            "-n", "auto",
            "--dist=loadfile",
            "-m", "not slow",
            "--html=test_logs/regression_test_report.html",
        ],
        "env_vars": {
            "TEST_ENV": "qa",
            "TEST_HEADLESS": "true"
        }
    },
    "parallel": {
        "description": "Parallel execution of all tests",
        "pytest_args": [
            "-v",
            "-n", "auto",
            "--dist=loadfile",
            "--html=test_logs/parallel_test_report.html",
        ],
        "env_vars": {
            "TEST_ENV": "qa",
            "TEST_HEADLESS": "true"
        }
    },
    "debug": {
        "description": "Single test with debug settings",
        "pytest_args": [
            "-v",
            "--pdb",
            "--no-cov",
            "--html=test_logs/debug_test_report.html",
        ],
        "env_vars": {
            "TEST_ENV": "qa",
            "TEST_HEADLESS": "false",
            "TEST_BROWSER": "chrome"
        }
    },
    "ci": {
        "description": "CI pipeline test execution",
        "pytest_args": [
            "-v",
            "-n", "auto",
            "--dist=loadfile",
            "--html=test_logs/ci_test_report.html",
            "--junitxml=test_logs/junit_report.xml",
        ],
        "env_vars": {
            "TEST_ENV": "qa",
            "TEST_HEADLESS": "true",
            "TEST_RERUNS": "2"
        }
    }
}