#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from categorized_spell_checker import categorized_spell_checker

def test_patterns():
    """Test các pattern để debug"""
    
    # Test pattern "kin" -> "kinh"
    text = "kin doanh"
    print(f"Original: {text}")
    
    # Test pattern matching
    pattern = r'\bkin\b'
    replacement = 'kinh'
    
    matches = re.finditer(pattern, text, re.IGNORECASE)
    for match in matches:
        print(f"Found match: '{match.group()}' at position {match.start()}")
        corrected = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        print(f"Corrected: {corrected}")
    
    # Test với spell checker
    result = categorized_spell_checker.check_text(text)
    print(f"Spell checker result: {result['corrected_text']}")
    print(f"Errors: {result['errors']}")

if __name__ == "__main__":
    test_patterns() 