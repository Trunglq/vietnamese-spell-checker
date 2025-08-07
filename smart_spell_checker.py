#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Smart Vietnamese Spell Checker
Phiên bản thông minh với validation và context awareness
"""

import re
import time
from typing import List, Dict, Tuple
from vietnamese_dictionary import vietnamese_dict
from pyvi import ViTokenizer, ViPosTagger

class SmartVietnameseSpellChecker:
    """Phiên bản thông minh của Vietnamese Spell Checker"""
    
    def __init__(self):
        self.vietnamese_dict = vietnamese_dict
        self.error_patterns = self._load_smart_error_patterns()
        self.context_rules = self._load_context_rules()
    
    def _load_smart_error_patterns(self) -> Dict[str, str]:
        """Tải các pattern lỗi thông minh"""
        return {
            # Lỗi dấu thanh - chỉ sửa khi chắc chắn
            r'\bcôn\b': 'công',
            r'\bkin\b': 'kính',
            r'\btoi\b': 'tôi',
            r'\bdinh\b': 'định',
            r'\btruong\b': 'trường',
            r'\bđạ\b': 'đại',
            r'\bhoc\b': 'học',
            r'\bjọc\b': 'học',
            r'\btue\b': 'tuệ',
            r'\bnana\b': 'nhân',
            r'\btrun\b': 'trung',
            r'\btam\b': 'tâm',
            r'\bviet\b': 'Việt',
            r'\bnam\b': 'Nam',
            r'\bdivt\b': 'dịch',
            r'\bhoạ\b': 'họa',
            r'\băm\b': 'năm',
            r'\bngâSn\b': 'ngân',
            r'\bhànG\b': 'hàng',
            r'\bCac\b': 'Các',
            r'\bthay\b': 'thấy',
            r'\bngươi\b': 'người',
            r'\bcuôc\b': 'cuộc',
            r'\bsóng\b': 'sống',
            r'\bduojc\b': 'được',
            r'\bnhu\b': 'như',
            r'\bđọi\b': 'đợi',
            r'\bNefn\b': 'Nền',
            r'\bté\b': 'tế',
            r'\bthé\b': 'thế',
            r'\bđúng\b': 'đứng',
            r'\btrươc\b': 'trước',
            r'\bnguyen\b': 'nguy',
            r'\bco\b': 'cơ',
            r'\bmọt\b': 'một',
            r'\bcuoc\b': 'cuộc',
            r'\bthoai\b': 'thoái',
            r'\bKhong\b': 'Không',
            r'\bphai\b': 'phải',
            r'\bca\b': 'cả',
            r'\bgi\b': 'gì',
            r'\bdideu\b': 'điều',
            r'\bsụ\b': 'sự',
            r'\bthat\b': 'thật',
            r'\bchinh\b': 'chính',
            r'\bgăng\b': 'gắng',
            r'\bhet\b': 'hết',
            r'\bsuc\b': 'sức',
            r'\bnaggna\b': 'nâng',
            r'\bchat\b': 'chất',
            r'\bluong\b': 'lượng',
            r'\bduc\b': 'dục',
            r'\bnuoc\b': 'nước',
            r'\bnèn\b': 'nền',
            r'\bthoi\b': 'thời',
            r'\bky\b': 'kỳ',
            r'\bmơi\b': 'mới',
            r'\btung\b': 'từng',
            r'\btienf\b': 'tiền',
            r'\blệ\b': 'lệ',
            r'\bsử\b': 'sử',
            
            # Lỗi từ ghép
            r'\bsinh diên\b': 'sinh viên',
            r'\bPhươngqyết\b': 'Phương quyết',
            r'\bđiểmnày\b': 'điểm này',
            r'\blsovới\b': 'so với',
            
            # Lỗi dấu cách
            r'(\w+)\s{2,}(\w+)': r'\1 \2',
            
            # Lỗi dấu câu
            r'(\w+)=(\w+)': r'\1 \2',
            r'(\w+),(\w+)': r'\1, \2',
        }
    
    def _load_context_rules(self) -> Dict[str, List[str]]:
        """Tải các quy tắc context"""
        return {
            # Từ không nên sửa trong context nhất định
            'AI': ['AI', 'artificial intelligence'],
            'Mitch': ['Mitch', 'hurricane'],
            'Bangladesh': ['Bangladesh', 'country'],
            'Việt Nam': ['Việt Nam', 'Vietnam'],
            'Phương': ['Phương', 'name'],
        }
    
    def check_text(self, text: str) -> Dict:
        """Kiểm tra chính tả với thuật toán thông minh"""
        try:
            # Chuẩn hóa văn bản
            normalized_text = self._normalize_text(text)
            
            # Tách từ
            words = ViTokenizer.tokenize(normalized_text).split()
            
            # Kiểm tra từng từ với context
            errors = []
            corrected_text = normalized_text
            
            for i, word in enumerate(words):
                # Loại bỏ dấu câu
                clean_word = re.sub(r'[^\w\s]', '', word)
                if not clean_word:
                    continue
                
                # Kiểm tra context
                if self._should_skip_word(clean_word, words, i):
                    continue
                
                # Kiểm tra chính tả
                if not self._is_correct_word(clean_word):
                    suggestions = self._get_smart_suggestions(clean_word, words, i)
                    if suggestions:
                        errors.append({
                            'word': word,
                            'position': normalized_text.find(word),
                            'suggestions': suggestions,
                            'corrected': suggestions[0]
                        })
            
            # Áp dụng corrections một cách thông minh
            corrected_text = self._apply_smart_corrections(normalized_text, errors)
            
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
    
    def _normalize_text(self, text: str) -> str:
        """Chuẩn hóa văn bản"""
        # Loại bỏ khoảng trắng thừa
        text = re.sub(r'\s+', ' ', text.strip())
        return text
    
    def _should_skip_word(self, word: str, all_words: List[str], position: int) -> bool:
        """Kiểm tra có nên bỏ qua từ này không"""
        # Bỏ qua tên riêng, từ viết tắt
        if word.upper() in ['AI', 'Mitch', 'Bangladesh']:
            return True
        
        # Bỏ qua số
        if word.isdigit():
            return True
        
        # Bỏ qua từ có dấu cách
        if ' ' in word:
            return True
        
        return False
    
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
    
    def _get_smart_suggestions(self, word: str, all_words: List[str], position: int) -> List[str]:
        """Lấy gợi ý thông minh cho từ"""
        suggestions = []
        
        # Sử dụng từ điển mở rộng
        dict_suggestions = self.vietnamese_dict.get_suggestions(word)
        suggestions.extend(dict_suggestions)
        
        # Thêm gợi ý từ pattern
        pattern_suggestion = self._get_pattern_suggestion(word)
        if pattern_suggestion and pattern_suggestion not in suggestions:
            suggestions.insert(0, pattern_suggestion)
        
        # Validate suggestions
        validated_suggestions = []
        for suggestion in suggestions:
            if self._validate_suggestion(word, suggestion, all_words, position):
                validated_suggestions.append(suggestion)
        
        return validated_suggestions[:3]  # Trả về tối đa 3 gợi ý
    
    def _get_pattern_suggestion(self, word: str) -> str:
        """Lấy gợi ý từ pattern"""
        for pattern, replacement in self.error_patterns.items():
            if re.search(pattern, word, re.IGNORECASE):
                return re.sub(pattern, replacement, word, flags=re.IGNORECASE)
        return ""
    
    def _validate_suggestion(self, original: str, suggestion: str, all_words: List[str], position: int) -> bool:
        """Validate gợi ý sửa lỗi"""
        # Không sửa thành từ quá dài
        if len(suggestion) > len(original) + 2:
            return False
        
        # Không sửa thành từ quá ngắn
        if len(suggestion) < len(original) - 2:
            return False
        
        # Kiểm tra trong từ điển
        if not self.vietnamese_dict.is_correct_word(suggestion):
            return False
        
        return True
    
    def _apply_smart_corrections(self, text: str, errors: List[Dict]) -> str:
        """Áp dụng corrections một cách thông minh"""
        corrected_text = text
        
        # Sắp xếp errors theo vị trí (từ phải sang trái)
        sorted_errors = sorted(errors, key=lambda x: x['position'], reverse=True)
        
        for error in sorted_errors:
            original_word = error['word']
            corrected_word = error['corrected']
            
            # Chỉ sửa nếu từ khác nhau
            if original_word != corrected_word:
                corrected_text = corrected_text.replace(original_word, corrected_word, 1)
        
        return corrected_text
    
    def _calculate_confidence(self, errors: List, total_words: int) -> float:
        """Tính độ tin cậy của kết quả kiểm tra"""
        if total_words == 0:
            return 1.0
        
        error_rate = len(errors) / total_words
        return max(0.0, 1.0 - error_rate)

# Tạo instance global
smart_spell_checker = SmartVietnameseSpellChecker() 