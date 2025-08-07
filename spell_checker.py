#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import requests
import subprocess
import re
import time
from typing import List, Dict, Tuple
# import underthesea  # Tạm thời comment out
from pyvi import ViTokenizer, ViPosTagger
from vietnamese_dictionary import vietnamese_dict

class VietnameseSpellChecker:
    """Kiểm tra lỗi chính tả tiếng Việt sử dụng GPT-OSS"""
    
    def __init__(self, model_path: str = None, server_url: str = "http://localhost:8080"):
        """
        Khởi tạo spell checker
        
        Args:
            model_path: Đường dẫn đến model GGUF
            server_url: URL của llama-server
        """
        self.server_url = server_url
        self.model_path = model_path
        self.server_process = None
        
        # Sử dụng từ điển tiếng Việt mở rộng
        self.vietnamese_dict = vietnamese_dict
        
        # Khởi động server nếu cần
        if model_path and os.path.exists(model_path):
            self._start_server()
    
    def _load_vietnamese_dictionary(self) -> set:
        """Tải từ điển tiếng Việt cơ bản (legacy)"""
        return self.vietnamese_dict.words
    
    def _start_server(self):
        """Khởi động llama-server"""
        try:
            # Kiểm tra xem server đã chạy chưa
            response = requests.get(f"{self.server_url}/health", timeout=2)
            if response.status_code == 200:
                print("✅ Server đã đang chạy")
                return
        except:
            pass
        
        try:
            # Khởi động server
            llama_server_path = "../build/bin/llama-server"
            if os.path.exists(llama_server_path):
                cmd = [
                    llama_server_path,
                    "-m", self.model_path,
                    "--host", "0.0.0.0",
                    "--port", "8080",
                    "--ctx-size", "2048"
                ]
                
                self.server_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
                # Đợi server khởi động
                time.sleep(5)
                print("✅ Server đã được khởi động")
            else:
                print("⚠️ Không tìm thấy llama-server")
                
        except Exception as e:
            print(f"❌ Lỗi khởi động server: {e}")
    
    def check_text(self, text: str) -> Dict:
        """
        Kiểm tra chính tả trong văn bản
        
        Args:
            text: Văn bản cần kiểm tra
            
        Returns:
            Dict chứa kết quả kiểm tra
        """
        try:
            # Tách từ
            words = ViTokenizer.tokenize(text).split()
            
            # Kiểm tra từng từ
            errors = []
            corrected_text = text
            
            for word in words:
                # Loại bỏ dấu câu
                clean_word = re.sub(r'[^\w\s]', '', word)
                if not clean_word:
                    continue
                
                # Kiểm tra chính tả
                if not self._is_correct_word(clean_word):
                    suggestions = self._get_suggestions(clean_word)
                    errors.append({
                        'word': word,
                        'position': text.find(word),
                        'suggestions': suggestions,
                        'corrected': suggestions[0] if suggestions else word
                    })
            
            # Sửa lỗi trong văn bản
            for error in errors:
                corrected_text = corrected_text.replace(error['word'], error['corrected'])
            
            return {
                'original_text': text,
                'corrected_text': corrected_text,
                'errors': errors,
                'error_count': len(errors),
                'confidence': self._calculate_confidence(errors, len(words))
            }
            
        except Exception as e:
            return {
                'error': f'Lỗi kiểm tra chính tả: {str(e)}',
                'original_text': text,
                'corrected_text': text,
                'errors': [],
                'error_count': 0,
                'confidence': 0.0
            }
    
    def _is_correct_word(self, word: str) -> bool:
        """Kiểm tra xem từ có đúng chính tả không"""
        # Kiểm tra trong từ điển mở rộng
        if self.vietnamese_dict.is_correct_word(word):
            return True
        
        # Kiểm tra trong common errors
        if word.lower() in self.vietnamese_dict.common_errors:
            return False
        
        # Kiểm tra bằng pyvi
        try:
            pos_tags = ViPosTagger.postagging(word)
            if pos_tags and pos_tags[0]:
                return True
        except:
            pass
        
        # Kiểm tra bằng GPT-OSS nếu có server
        if self.server_process:
            return self._check_with_gpt(word)
        
        return False
    
    def _check_with_gpt(self, word: str) -> bool:
        """Kiểm tra từ bằng GPT-OSS"""
        try:
            prompt = f"""Kiểm tra xem từ "{word}" có phải là từ tiếng Việt đúng chính tả không. 
            Chỉ trả lời "ĐÚNG" hoặc "SAI"."""
            
            response = requests.post(
                f"{self.server_url}/completion",
                json={
                    "prompt": prompt,
                    "n_predict": 10,
                    "temperature": 0.1,
                    "stop": ["\n", ".", "!"]
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('content', '').strip().upper()
                return "ĐÚNG" in answer
            
        except Exception as e:
            print(f"Lỗi kiểm tra với GPT: {e}")
        
        return False
    
    def get_suggestions(self, word: str) -> List[str]:
        """Lấy gợi ý sửa lỗi cho từ"""
        # Sử dụng từ điển mở rộng để lấy gợi ý
        suggestions = self.vietnamese_dict.get_suggestions(word)
        
        # Gợi ý bằng GPT-OSS nếu có server
        if self.server_process:
            gpt_suggestions = self._get_gpt_suggestions(word)
            suggestions.extend(gpt_suggestions)
        
        # Loại bỏ trùng lặp và sắp xếp theo độ tương đồng
        unique_suggestions = list(set(suggestions))
        unique_suggestions.sort(key=lambda x: self._similarity(word, x), reverse=True)
        
        return unique_suggestions[:5]  # Trả về tối đa 5 gợi ý
    
    def _get_gpt_suggestions(self, word: str) -> List[str]:
        """Lấy gợi ý từ GPT-OSS"""
        try:
            prompt = f"""Cho từ "{word}" bị sai chính tả tiếng Việt, hãy đưa ra 3 từ gợi ý sửa lỗi.
            Chỉ trả lời các từ, cách nhau bằng dấu phẩy."""
            
            response = requests.post(
                f"{self.server_url}/completion",
                json={
                    "prompt": prompt,
                    "n_predict": 50,
                    "temperature": 0.3,
                    "stop": ["\n", ".", "!"]
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get('content', '').strip()
                suggestions = [s.strip() for s in content.split(',')]
                return [s for s in suggestions if s and len(s) > 1]
            
        except Exception as e:
            print(f"Lỗi lấy gợi ý từ GPT: {e}")
        
        return []
    
    def _similarity(self, word1: str, word2: str) -> float:
        """Tính độ tương đồng giữa hai từ"""
        if word1 == word2:
            return 1.0
        
        # Tính Levenshtein distance
        len1, len2 = len(word1), len(word2)
        matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        
        for i in range(len1 + 1):
            matrix[i][0] = i
        for j in range(len2 + 1):
            matrix[0][j] = j
        
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                cost = 0 if word1[i-1] == word2[j-1] else 1
                matrix[i][j] = min(
                    matrix[i-1][j] + 1,      # deletion
                    matrix[i][j-1] + 1,      # insertion
                    matrix[i-1][j-1] + cost  # substitution
                )
        
        distance = matrix[len1][len2]
        max_len = max(len1, len2)
        return 1 - (distance / max_len) if max_len > 0 else 0
    
    def _calculate_confidence(self, errors: List, total_words: int) -> float:
        """Tính độ tin cậy của kết quả kiểm tra"""
        if total_words == 0:
            return 1.0
        
        error_rate = len(errors) / total_words
        return max(0.0, 1.0 - error_rate)
    
    def __del__(self):
        """Dọn dẹp khi object bị hủy"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait() 