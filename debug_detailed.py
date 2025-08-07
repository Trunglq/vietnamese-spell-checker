#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from categorized_spell_checker import categorized_spell_checker

def test_all_patterns():
    """Test tất cả các pattern để debug"""
    
    text = "kin doanh"
    print(f"Original: {text}")
    
    # Test từng pattern trong tone_errors
    tone_patterns = categorized_spell_checker.error_categories['tone_errors']
    
    for pattern, replacement in tone_patterns.items():
        if 'kin' in pattern or 'kính' in pattern:
            print(f"\nTesting pattern: {pattern} -> {replacement}")
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                print(f"  Found match: '{match.group()}' at position {match.start()}")
                corrected = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
                print(f"  Corrected: {corrected}")
    
    # Test với spell checker
    result = categorized_spell_checker.check_text(text)
    print(f"\nSpell checker result: {result['corrected_text']}")
    print(f"Errors: {result['errors']}")

if __name__ == "__main__":
    test_all_patterns() 