"""
Test configuration and fixtures for the test suite
"""

import sys
from pathlib import Path

# Add the src directory to the Python path so we can import our modules
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))
