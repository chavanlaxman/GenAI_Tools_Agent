"""Test decorator and helper utilities."""
import os
import pytest
from functools import wraps
from utils.markers import *

def test_case(*test_ids, **kwargs):
    """
    Decorator to link test case IDs and add metadata to tests.
    
    Usage:
    @test_case('TC_001', 'TC_002', feature='login', priority='high')
    def test_login():
        pass
    """
    def decorator(func):
        # Add test case ID to docstring
        tc_str = ', '.join(test_ids)
        original_doc = func.__doc__ or ''
        func.__doc__ = f"Test Case IDs: {tc_str}\n\n{original_doc}"
        
        # Add markers based on kwargs
        markers = []
        if kwargs.get('smoke'):
            markers.append(smoke)
        if kwargs.get('critical'):
            markers.append(critical)
        if 'feature' in kwargs:
            feature = kwargs['feature'].lower()
            if feature == 'login':
                markers.append(login)
            elif feature == 'cart':
                markers.append(cart)
            elif feature == 'payment':
                markers.append(payment)
            elif feature == 'social':
                markers.append(social)
        
        # Apply all markers
        for marker in markers:
            func = marker(func)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get test logger
            test_name = func.__name__
            if args and hasattr(args[0], '__class__'):
                test_name = f"{args[0].__class__.__name__}.{test_name}"
            
            # Log test start with test case IDs
            logger = args[0].logger if hasattr(args[0], 'logger') else None
            if logger:
                logger.info(f"Starting test {test_name} (Test Cases: {tc_str})")
            
            # Run test
            result = func(*args, **kwargs)
            
            # Log test completion
            if logger:
                logger.info(f"Completed test {test_name}")
            
            return result
        
        return wrapper
    return decorator

def skip_if_env(env_name):
    """Skip test if running in specified environment."""
    current_env = os.getenv('TEST_ENV', 'qa')
    return pytest.mark.skipif(
        current_env == env_name,
        reason=f"Test not intended for {env_name} environment"
    )

def retry_if_fails(max_retries=2, delay_seconds=1):
    """Retry test if it fails."""
    return pytest.mark.flaky(
        reruns=max_retries,
        reruns_delay=delay_seconds
    )

def requires_feature_flag(flag_name):
    """Skip test if feature flag is not enabled."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            from utils.config import TestConfig
            config = TestConfig()
            if not config.is_feature_enabled(flag_name):
                pytest.skip(f"Feature {flag_name} is not enabled")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Example usage in test files:
"""
from test_helpers import test_case, skip_if_env, retry_if_fails

@test_case('TC_001', feature='login', smoke=True)
@retry_if_fails(max_retries=3)
@skip_if_env('prod')
def test_user_login():
    pass
"""