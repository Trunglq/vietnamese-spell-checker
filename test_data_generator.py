#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test Data Generator for Vietnamese Spell Checker
Tự động sinh dữ liệu test với các loại lỗi khác nhau
"""

import random
import re
from typing import Dict, List, Tuple
from datetime import datetime

class TestDataGenerator:
    def __init__(self):
        # Dữ liệu từ vựng và lỗi phổ biến
        self.vocabulary = {
            'business': [
                'kinh doanh', 'công ty', 'thị trường', 'doanh nghiệp', 'lợi nhuận',
                'đầu tư', 'quản lý', 'nhân viên', 'khách hàng', 'sản phẩm',
                'dịch vụ', 'marketing', 'tài chính', 'ngân hàng', 'bảo hiểm'
            ],
            'education': [
                'học sinh', 'sinh viên', 'giáo viên', 'trường học', 'đại học',
                'khoa học', 'nghiên cứu', 'giáo dục', 'đào tạo', 'chuyên ngành',
                'bài tập', 'thi cử', 'học tập', 'kiến thức', 'kỹ năng'
            ],
            'technology': [
                'máy tính', 'phần mềm', 'công nghệ', 'internet', 'website',
                'ứng dụng', 'lập trình', 'dữ liệu', 'hệ thống', 'mạng',
                'bảo mật', 'trí tuệ nhân tạo', 'robot', 'automation', 'cloud'
            ],
            'news': [
                'tin tức', 'báo chí', 'phóng viên', 'truyền hình', 'radio',
                'sự kiện', 'thời sự', 'chính trị', 'kinh tế', 'xã hội',
                'thể thao', 'giải trí', 'thời tiết', 'giao thông', 'y tế'
            ],
            'personal': [
                'gia đình', 'bạn bè', 'tình yêu', 'cuộc sống', 'sở thích',
                'du lịch', 'ăn uống', 'thể thao', 'sức khỏe', 'hạnh phúc',
                'ước mơ', 'mục tiêu', 'kế hoạch', 'kỷ niệm', 'kỷ niệm'
            ],
            'finance': [
                'tiền bạc', 'ngân hàng', 'tài khoản', 'thẻ tín dụng', 'vay',
                'tiết kiệm', 'đầu tư', 'cổ phiếu', 'bảo hiểm', 'thuế',
                'lương', 'chi tiêu', 'ngân sách', 'lợi nhuận', 'rủi ro'
            ],
            'social': [
                'xã hội', 'cộng đồng', 'dân số', 'văn hóa', 'truyền thống',
                'phong tục', 'lễ hội', 'đời sống', 'an sinh', 'phát triển',
                'bình đẳng', 'công bằng', 'đoàn kết', 'hợp tác', 'chia sẻ'
            ],
            'economics': [
                'kinh tế', 'thị trường', 'cung cầu', 'giá cả', 'lạm phát',
                'tăng trưởng', 'suy thoái', 'khủng hoảng', 'phục hồi', 'ổn định',
                'phát triển', 'cạnh tranh', 'độc quyền', 'thương mại', 'xuất nhập khẩu'
            ],
            'general': [
                'cuộc sống', 'con người', 'thiên nhiên', 'môi trường', 'thời gian',
                'không gian', 'vũ trụ', 'trái đất', 'mặt trời', 'mặt trăng',
                'sao', 'gió', 'mưa', 'nắng', 'bão'
            ],
            'history': [
                'lịch sử', 'quá khứ', 'truyền thống', 'văn hóa', 'di tích',
                'di sản', 'cổ vật', 'khảo cổ', 'nghiên cứu', 'tài liệu',
                'sự kiện', 'chiến tranh', 'hòa bình', 'độc lập', 'tự do'
            ]
        }
        
        # Các loại lỗi phổ biến
        self.error_patterns = {
            'tone_error': {
                'a': ['à', 'á', 'ả', 'ã', 'ạ'],
                'e': ['è', 'é', 'ẻ', 'ẽ', 'ẹ'],
                'i': ['ì', 'í', 'ỉ', 'ĩ', 'ị'],
                'o': ['ò', 'ó', 'ỏ', 'õ', 'ọ'],
                'u': ['ù', 'ú', 'ủ', 'ũ', 'ụ'],
                'y': ['ỳ', 'ý', 'ỷ', 'ỹ', 'ỵ'],
                'ă': ['ằ', 'ắ', 'ẳ', 'ẵ', 'ặ'],
                'ơ': ['ờ', 'ớ', 'ở', 'ỡ', 'ợ'],
                'ô': ['ồ', 'ố', 'ổ', 'ỗ', 'ộ'],
                'ư': ['ừ', 'ứ', 'ử', 'ữ', 'ự']
            },
            'typo_error': {
                'd': 'đ',
                'đ': 'd',
                's': 'x',
                'x': 's',
                'z': 'j',
                'j': 'z',
                'f': 'ph',
                'ph': 'f',
                'c': 'k',
                'k': 'c'
            },
            'sticky_typing': {
                'aa': 'a',
                'ee': 'e',
                'ii': 'i',
                'oo': 'o',
                'uu': 'u',
                'yy': 'y',
                'nn': 'n',
                'mm': 'm',
                'll': 'l',
                'tt': 't'
            },
            'compound_word': {
                'truonghoc': 'trường học',
                'sinhvien': 'sinh viên',
                'giaovien': 'giáo viên',
                'kinhdoanh': 'kinh doanh',
                'congty': 'công ty',
                'thitruong': 'thị trường',
                'doanhnghiep': 'doanh nghiệp',
                'loinhuan': 'lợi nhuận',
                'dautu': 'đầu tư',
                'quanly': 'quản lý'
            },
            'capitalization': {
                'vietnam': 'Việt Nam',
                'hanoi': 'Hà Nội',
                'hochiminh': 'Hồ Chí Minh',
                'danang': 'Đà Nẵng',
                'cantho': 'Cần Thơ',
                'haiphong': 'Hải Phòng',
                'nhatrang': 'Nha Trang',
                'dalat': 'Đà Lạt',
                'sapa': 'Sa Pa',
                'halong': 'Hạ Long'
            }
        }
        
        # Templates cho câu
        self.sentence_templates = [
            "{subject} {action} {object} {location} {time}",
            "{time} {subject} {action} {object} {result}",
            "{location} {subject} {action} {object} {purpose}",
            "{subject} {action} {object} {reason} {time}",
            "{time} {location} {subject} {action} {object}",
            "{subject} {action} {object} {method} {result}",
            "{location} {time} {subject} {action} {object}",
            "{subject} {action} {object} {condition} {time}"
        ]
        
        self.subjects = ['Tôi', 'Chúng ta', 'Họ', 'Cô ấy', 'Anh ấy', 'Chúng tôi', 'Bạn', 'Mọi người']
        self.actions = ['đang', 'sẽ', 'đã', 'vừa', 'luôn', 'thường', 'hiếm khi', 'không bao giờ']
        self.objects = ['làm việc', 'học tập', 'nghiên cứu', 'phát triển', 'cải thiện', 'xây dựng', 'tạo ra', 'thực hiện']
        self.locations = ['ở đây', 'tại đó', 'trong nhà', 'ngoài trời', 'tại văn phòng', 'ở trường học', 'tại bệnh viện', 'ở công ty']
        self.times = ['hôm nay', 'ngày mai', 'tuần trước', 'tháng sau', 'năm ngoái', 'sáng nay', 'chiều tối', 'đêm qua']
        self.results = ['rất tốt', 'khá thành công', 'có tiến bộ', 'đạt kết quả cao', 'vượt mong đợi', 'cần cải thiện']
        self.purposes = ['để học hỏi', 'nhằm phát triển', 'vì lợi ích chung', 'cho tương lai', 'để cải thiện', 'nhằm đạt mục tiêu']
        self.reasons = ['vì lý do cá nhân', 'do hoàn cảnh', 'theo yêu cầu', 'vì sự cần thiết', 'do nhu cầu', 'theo kế hoạch']
        self.methods = ['bằng cách', 'thông qua', 'sử dụng', 'áp dụng', 'vận dụng', 'thực hiện theo']
        self.conditions = ['nếu có thể', 'khi thuận lợi', 'trong điều kiện cho phép', 'nếu đủ điều kiện', 'khi có cơ hội']
    
    def generate_error_word(self, correct_word: str, error_type: str = None) -> Tuple[str, str]:
        """Tạo từ có lỗi từ từ đúng"""
        if error_type is None:
            error_type = random.choice(list(self.error_patterns.keys()))
        
        if error_type == 'tone_error':
            # Thêm dấu thanh ngẫu nhiên
            for vowel, tones in self.error_patterns['tone_error'].items():
                if vowel in correct_word:
                    tone = random.choice(tones)
                    wrong_word = correct_word.replace(vowel, tone)
                    return wrong_word, correct_word
        
        elif error_type == 'typo_error':
            # Thay thế ký tự
            for wrong_char, correct_char in self.error_patterns['typo_error'].items():
                if wrong_char in correct_word:
                    wrong_word = correct_word.replace(wrong_char, correct_char)
                    return wrong_word, correct_word
        
        elif error_type == 'sticky_typing':
            # Lặp ký tự
            for double_char, single_char in self.error_patterns['sticky_typing'].items():
                if double_char in correct_word:
                    wrong_word = correct_word.replace(double_char, single_char)
                    return wrong_word, correct_word
        
        elif error_type == 'compound_word':
            # Tách từ ghép
            for compound, separated in self.error_patterns['compound_word'].items():
                if compound in correct_word:
                    wrong_word = correct_word.replace(compound, separated)
                    return wrong_word, correct_word
        
        elif error_type == 'capitalization':
            # Lỗi viết hoa
            for lowercase, proper_case in self.error_patterns['capitalization'].items():
                if lowercase in correct_word.lower():
                    wrong_word = correct_word.replace(lowercase, lowercase)
                    return wrong_word, correct_word
        
        # Nếu không tạo được lỗi, trả về từ gốc
        return correct_word, correct_word
    
    def generate_test_sentence(self, category: str, error_rate: float = 0.3) -> Dict:
        """Tạo câu test với lỗi chính tả"""
        # Chọn template ngẫu nhiên
        template = random.choice(self.sentence_templates)
        
        # Tạo câu đúng
        sentence_parts = {
            'subject': random.choice(self.subjects),
            'action': random.choice(self.actions),
            'object': random.choice(self.objects),
            'location': random.choice(self.locations),
            'time': random.choice(self.times),
            'result': random.choice(self.results),
            'purpose': random.choice(self.purposes),
            'reason': random.choice(self.reasons),
            'method': random.choice(self.methods),
            'condition': random.choice(self.conditions)
        }
        
        correct_sentence = template.format(**sentence_parts)
        
        # Thêm từ vựng theo category
        category_words = self.vocabulary.get(category, [])
        if category_words:
            extra_words = random.sample(category_words, min(3, len(category_words)))
            correct_sentence += " " + " ".join(extra_words)
        
        # Tạo lỗi trong câu
        words = correct_sentence.split()
        wrong_words = []
        expected_corrections = {}
        
        for word in words:
            # Xác suất tạo lỗi
            if random.random() < error_rate:
                wrong_word, correct_word = self.generate_error_word(word)
                if wrong_word != correct_word:
                    wrong_words.append(wrong_word)
                    expected_corrections[wrong_word] = correct_word
                else:
                    wrong_words.append(word)
            else:
                wrong_words.append(word)
        
        wrong_sentence = " ".join(wrong_words)
        
        return {
            "original": wrong_sentence,
            "expected_corrections": expected_corrections,
            "category": category,
            "correct_sentence": correct_sentence
        }
    
    def generate_test_cases(self, num_cases: int = 10, categories: List[str] = None) -> List[Dict]:
        """Tạo nhiều test cases"""
        if categories is None:
            categories = list(self.vocabulary.keys())
        
        test_cases = []
        for i in range(num_cases):
            category = random.choice(categories)
            test_case = self.generate_test_sentence(category)
            test_cases.append(test_case)
        
        return test_cases
    
    def generate_specific_error_test(self, error_type: str, num_cases: int = 5) -> List[Dict]:
        """Tạo test cases với lỗi cụ thể"""
        test_cases = []
        categories = list(self.vocabulary.keys())
        
        for i in range(num_cases):
            category = random.choice(categories)
            test_case = self.generate_test_sentence(category, error_rate=0.5)
            
            # Đảm bảo có lỗi cụ thể
            if error_type in self.error_patterns:
                # Tạo thêm lỗi cụ thể
                words = test_case["original"].split()
                for j, word in enumerate(words):
                    if random.random() < 0.3:  # 30% chance
                        wrong_word, correct_word = self.generate_error_word(word, error_type)
                        if wrong_word != correct_word:
                            words[j] = wrong_word
                            test_case["expected_corrections"][wrong_word] = correct_word
                
                test_case["original"] = " ".join(words)
            
            test_cases.append(test_case)
        
        return test_cases

def main():
    """Test generator"""
    generator = TestDataGenerator()
    
    print("🎲 Vietnamese Spell Checker - Test Data Generator")
    print("=" * 50)
    
    # Tạo test cases ngẫu nhiên
    test_cases = generator.generate_test_cases(5)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['category'].upper()}")
        print(f"   Original: {test_case['original']}")
        print(f"   Expected corrections: {len(test_case['expected_corrections'])} errors")
        for wrong, correct in test_case['expected_corrections'].items():
            print(f"     '{wrong}' → '{correct}'")

if __name__ == '__main__':
    main()
