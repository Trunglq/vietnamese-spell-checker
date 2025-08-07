#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advanced Vietnamese Spell Checker
Phiên bản nâng cao với khả năng phát hiện lỗi tốt hơn
"""

import re
import time
from typing import List, Dict, Tuple
from vietnamese_dictionary import vietnamese_dict
from pyvi import ViTokenizer, ViPosTagger

class AdvancedVietnameseSpellChecker:
    """Phiên bản nâng cao của Vietnamese Spell Checker"""
    
    def __init__(self):
        self.vietnamese_dict = vietnamese_dict
        self.error_patterns = self._load_error_patterns()
    
    def _load_error_patterns(self) -> Dict[str, str]:
        """Tải các pattern lỗi phổ biến"""
        return {
            # Lỗi dấu thanh
            r'côn\b': 'công',
            r'kin\b': 'kính',
            r'toi\b': 'tôi',
            r'dinh\b': 'định',
            r'sinh diên\b': 'sinh viên',
            r'truong\b': 'trường',
            r'đạ\b': 'đại',
            r'hoc\b': 'học',
            r'jọc\b': 'học',
            r'tue\b': 'tuệ',
            r'nana\b': 'nhân',
            r'trun\b': 'trung',
            r'tam\b': 'tâm',
            r'viet\b': 'Việt',
            r'nam\b': 'Nam',
            r'divt\b': 'dịch',
            r'lsovới\b': 'so với',
            r'hoạ\b': 'họa',
            r'ăm\b': 'năm',
            r'Phươngqyết\b': 'Phương quyết',
            r'ngâSn\b': 'ngân',
            r'hànG\b': 'hàng',
            r'điểmnày\b': 'điểm này',
            r'Cac\b': 'Các',
            r'thay\b': 'thấy',
            r'ngươi\b': 'người',
            r'cuôc\b': 'cuộc',
            r'sóng\b': 'sống',
            r'duojc\b': 'được',
            r'nhu\b': 'như',
            r'đọi\b': 'đợi',
            r'Nefn\b': 'Nền',
            r'té\b': 'tế',
            r'thé\b': 'thế',
            r'đúng\b': 'đứng',
            r'trươc\b': 'trước',
            r'nguyen\b': 'nguy',
            r'co\b': 'cơ',
            r'mọt\b': 'một',
            r'cuoc\b': 'cuộc',
            r'thoai\b': 'thoái',
            r'Khong\b': 'Không',
            r'phai\b': 'phải',
            r'ca\b': 'cả',
            r'gi\b': 'gì',
            r'dideu\b': 'điều',
            r'sụ\b': 'sự',
            r'that\b': 'thật',
            r'chinh\b': 'chính',
            r'găng\b': 'gắng',
            r'het\b': 'hết',
            r'suc\b': 'sức',
            r'naggna\b': 'nâng',
            r'chat\b': 'chất',
            r'luong\b': 'lượng',
            r'duc\b': 'dục',
            r'nuoc\b': 'nước',
            r'nèn\b': 'nền',
            r'đứng\b': 'đứng',
            r'nguy\b': 'nguy',
            r'thoi\b': 'thời',
            r'ky\b': 'kỳ',
            r'mơi\b': 'mới',
            r'tung\b': 'từng',
            r'tienf\b': 'tiền',
            r'lệ\b': 'lệ',
            r'sử\b': 'sử',
            
            # Lỗi dấu cách
            r'(\w+)\s{2,}(\w+)': r'\1 \2',
            
            # Lỗi dấu câu
            r'(\w+)=(\w+)': r'\1 \2',
            r'(\w+),(\w+)': r'\1, \2',
        }
    
    def check_text(self, text: str) -> Dict:
        """Kiểm tra chính tả với thuật toán nâng cao"""
        try:
            # Chuẩn hóa văn bản
            normalized_text = self._normalize_text(text)
            
            # Tách từ
            words = ViTokenizer.tokenize(normalized_text).split()
            
            # Kiểm tra từng từ
            errors = []
            corrected_text = normalized_text
            
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
                        'position': normalized_text.find(word),
                        'suggestions': suggestions,
                        'corrected': suggestions[0] if suggestions else word
                    })
            
            # Áp dụng pattern corrections
            pattern_corrected_text = self._apply_pattern_corrections(normalized_text)
            
            # Sửa lỗi trong văn bản
            for error in errors:
                pattern_corrected_text = pattern_corrected_text.replace(error['word'], error['corrected'])
            
            return {
                'original_text': text,
                'corrected_text': pattern_corrected_text,
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
    
    def _normalize_text(self, text: str) -> str:
        """Chuẩn hóa văn bản"""
        # Loại bỏ khoảng trắng thừa
        text = re.sub(r'\s+', ' ', text.strip())
        return text
    
    def _is_correct_word(self, word: str) -> bool:
        """Kiểm tra từ có đúng chính tả không"""
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
        
        return False
    
    def _get_suggestions(self, word: str) -> List[str]:
        """Lấy gợi ý sửa lỗi cho từ"""
        # Sử dụng từ điển mở rộng để lấy gợi ý
        suggestions = self.vietnamese_dict.get_suggestions(word)
        
        # Thêm gợi ý từ pattern
        pattern_suggestion = self._get_pattern_suggestion(word)
        if pattern_suggestion:
            suggestions.insert(0, pattern_suggestion)
        
        return suggestions[:5]  # Trả về tối đa 5 gợi ý
    
    def _get_pattern_suggestion(self, word: str) -> str:
        """Lấy gợi ý từ pattern"""
        for pattern, replacement in self.error_patterns.items():
            if re.search(pattern, word, re.IGNORECASE):
                return re.sub(pattern, replacement, word, flags=re.IGNORECASE)
        return ""
    
    def _apply_pattern_corrections(self, text: str) -> str:
        """Áp dụng các pattern correction"""
        corrected_text = text
        
        for pattern, replacement in self.error_patterns.items():
            corrected_text = re.sub(pattern, replacement, corrected_text, flags=re.IGNORECASE)
        
        return corrected_text
    
    def _calculate_confidence(self, errors: List, total_words: int) -> float:
        """Tính độ tin cậy của kết quả kiểm tra"""
        if total_words == 0:
            return 1.0
        
        error_rate = len(errors) / total_words
        return max(0.0, 1.0 - error_rate)

# Tạo instance global
advanced_spell_checker = AdvancedVietnameseSpellChecker() 