"""Test cases for the main.py file"""

import main


def test_main():
    """Tests the root endpoint"""
    assert main.main() == {"hello": "world"}


def test_convert():
    """Tests the conversion endpoint"""
    assert main.convert("PA", "Pittsburgh") == {
        "lat": "40.4416941",
        "long": "-79.9900861",
    }
