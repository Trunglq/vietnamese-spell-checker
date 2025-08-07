#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_spell_checker():
    """Test spell checker qua API"""
    url = "http://127.0.0.1:3000/api/check_spelling"
    
    test_text = "toi dang là sinh diên nam hai ở truong đạ hoc khoa jọc tự nhiên , trogn năm ke tiep toi sẽ chọn chuyen nganh về trí tue nhana tạo"
    
    data = {
        "text": test_text
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"Errors: {result['error_count']}")
            print(f"Corrected: {result['corrected_text']}")
            return result
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

if __name__ == "__main__":
    test_spell_checker() 