#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test Data Generator for Vietnamese Spell Checker
Tự động sinh dữ liệu test với các loại lỗi khác nhau - Phiên bản cải tiến
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
                'dịch vụ', 'marketing', 'tài chính', 'ngân hàng', 'bảo hiểm',
                'cổ phiếu', 'thương mại', 'xuất khẩu', 'nhập khẩu', 'hợp đồng'
            ],
            'education': [
                'học sinh', 'sinh viên', 'giáo viên', 'trường học', 'đại học',
                'khoa học', 'nghiên cứu', 'giáo dục', 'đào tạo', 'chuyên ngành',
                'bài tập', 'thi cử', 'học tập', 'kiến thức', 'kỹ năng',
                'luận văn', 'báo cáo', 'thuyết trình', 'thực tập', 'tốt nghiệp'
            ],
            'technology': [
                'máy tính', 'phần mềm', 'công nghệ', 'internet', 'website',
                'ứng dụng', 'lập trình', 'dữ liệu', 'hệ thống', 'mạng',
                'bảo mật', 'trí tuệ nhân tạo', 'robot', 'automation', 'cloud',
                'blockchain', 'machine learning', 'deep learning', 'IoT', '5G'
            ],
            'news': [
                'tin tức', 'báo chí', 'phóng viên', 'truyền hình', 'radio',
                'sự kiện', 'thời sự', 'chính trị', 'kinh tế', 'xã hội',
                'thể thao', 'giải trí', 'thời tiết', 'giao thông', 'y tế',
                'an ninh', 'quốc phòng', 'đối ngoại', 'nội chính', 'tư pháp'
            ],
            'personal': [
                'gia đình', 'bạn bè', 'tình yêu', 'cuộc sống', 'sở thích',
                'du lịch', 'ăn uống', 'thể thao', 'sức khỏe', 'hạnh phúc',
                'ước mơ', 'mục tiêu', 'kế hoạch', 'kỷ niệm', 'kỷ niệm',
                'sinh nhật', 'lễ tết', 'họp mặt', 'tiệc tùng', 'nghỉ ngơi'
            ],
            'finance': [
                'tiền bạc', 'ngân hàng', 'tài khoản', 'thẻ tín dụng', 'vay',
                'tiết kiệm', 'đầu tư', 'cổ phiếu', 'bảo hiểm', 'thuế',
                'lương', 'chi tiêu', 'ngân sách', 'lợi nhuận', 'rủi ro',
                'lạm phát', 'tỷ giá', 'hối đoái', 'chứng khoán', 'quỹ đầu tư'
            ],
            'social': [
                'xã hội', 'cộng đồng', 'dân số', 'văn hóa', 'truyền thống',
                'phong tục', 'lễ hội', 'đời sống', 'an sinh', 'phát triển',
                'bình đẳng', 'công bằng', 'đoàn kết', 'hợp tác', 'chia sẻ',
                'tình nguyện', 'từ thiện', 'nhân đạo', 'cứu trợ', 'hỗ trợ'
            ],
            'economics': [
                'kinh tế', 'thị trường', 'cung cầu', 'giá cả', 'lạm phát',
                'tăng trưởng', 'suy thoái', 'khủng hoảng', 'phục hồi', 'ổn định',
                'phát triển', 'cạnh tranh', 'độc quyền', 'thương mại', 'xuất nhập khẩu',
                'GDP', 'CPI', 'lãi suất', 'tỷ lệ thất nghiệp', 'chỉ số giá'
            ],
            'general': [
                'cuộc sống', 'con người', 'thiên nhiên', 'môi trường', 'thời gian',
                'không gian', 'vũ trụ', 'trái đất', 'mặt trời', 'mặt trăng',
                'sao', 'gió', 'mưa', 'nắng', 'bão', 'động vật', 'thực vật',
                'khí hậu', 'thời tiết', 'địa lý'
            ],
            'history': [
                'lịch sử', 'quá khứ', 'truyền thống', 'văn hóa', 'di tích',
                'di sản', 'cổ vật', 'khảo cổ', 'nghiên cứu', 'tài liệu',
                'sự kiện', 'chiến tranh', 'hòa bình', 'độc lập', 'tự do',
                'cách mạng', 'kháng chiến', 'thống nhất', 'đổi mới', 'phát triển'
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
        
        # Templates câu tự nhiên hơn
        self.natural_sentences = {
            'business': [
                "Công ty chúng tôi đang phát triển rất nhanh trong lĩnh vực {topic}.",
                "Thị trường {topic} hiện nay có nhiều cơ hội cho các doanh nghiệp.",
                "Tôi đang làm việc tại một công ty {topic} ở {location}.",
                "Dự án {topic} này sẽ mang lại lợi nhuận cao cho công ty.",
                "Chúng ta cần đầu tư vào {topic} để cạnh tranh với đối thủ.",
                "Báo cáo về {topic} cho thấy xu hướng tăng trưởng tích cực.",
                "Khách hàng rất hài lòng với dịch vụ {topic} của chúng tôi.",
                "Cuộc họp về {topic} sẽ diễn ra vào tuần tới.",
                "Nhân viên mới cần được đào tạo về {topic}.",
                "Chiến lược {topic} đã được thông qua bởi ban lãnh đạo."
            ],
            'education': [
                "Sinh viên cần học tập chăm chỉ để đạt kết quả tốt trong {topic}.",
                "Giáo viên đang giảng dạy môn {topic} cho học sinh lớp 12.",
                "Trường đại học này có chương trình {topic} rất chất lượng.",
                "Tôi đang nghiên cứu về {topic} cho luận văn tốt nghiệp.",
                "Bài tập về {topic} khá khó nhưng rất thú vị.",
                "Thư viện có nhiều sách về {topic} cho sinh viên tham khảo.",
                "Kỳ thi {topic} sẽ diễn ra vào cuối tháng này.",
                "Học sinh cần chuẩn bị kỹ cho bài kiểm tra {topic}.",
                "Giáo viên đã giải thích rất rõ về {topic} trong buổi học.",
                "Sinh viên có thể thực tập tại các công ty về {topic}."
            ],
            'technology': [
                "Công nghệ {topic} đang phát triển rất nhanh trên thế giới.",
                "Chúng tôi đang phát triển ứng dụng {topic} cho khách hàng.",
                "Máy tính hiện đại có thể xử lý {topic} một cách hiệu quả.",
                "Internet đã thay đổi cách chúng ta sử dụng {topic}.",
                "Lập trình viên cần học thêm về {topic} để cập nhật kiến thức.",
                "Hệ thống {topic} này rất ổn định và bảo mật.",
                "Công ty đang đầu tư vào {topic} để nâng cao hiệu suất.",
                "Người dùng rất thích giao diện của ứng dụng {topic}.",
                "Dữ liệu về {topic} được lưu trữ an toàn trên cloud.",
                "Trí tuệ nhân tạo đang được áp dụng trong {topic}."
            ],
            'news': [
                "Tin tức về {topic} đang thu hút sự chú ý của công chúng.",
                "Phóng viên đang tác nghiệp tại hiện trường vụ {topic}.",
                "Báo chí đã đưa tin chi tiết về sự kiện {topic}.",
                "Truyền hình sẽ phát sóng chương trình về {topic} tối nay.",
                "Thời sự hôm nay có nhiều tin tức quan trọng về {topic}.",
                "Chính phủ đã có phản ứng về vấn đề {topic}.",
                "Công chúng đang quan tâm đến thông tin về {topic}.",
                "Báo cáo về {topic} cho thấy nhiều điểm đáng chú ý.",
                "Các chuyên gia đang phân tích tình hình {topic}.",
                "Sự kiện {topic} đã thu hút sự tham gia của nhiều người."
            ],
            'personal': [
                "Gia đình tôi rất vui khi được đi du lịch {topic}.",
                "Bạn bè đã tổ chức tiệc sinh nhật cho tôi tại {location}.",
                "Tôi rất thích {topic} và thường dành thời gian cho nó.",
                "Cuộc sống của tôi đã thay đổi nhiều kể từ khi {topic}.",
                "Tôi đang lên kế hoạch cho {topic} trong tương lai.",
                "Sức khỏe của tôi đã cải thiện nhờ {topic}.",
                "Tôi cảm thấy hạnh phúc khi được {topic} cùng gia đình.",
                "Kỷ niệm về {topic} sẽ mãi in sâu trong tâm trí tôi.",
                "Tôi đang học cách {topic} để phát triển bản thân.",
                "Mục tiêu của tôi là {topic} trong năm nay."
            ],
            'finance': [
                "Ngân hàng đã thông báo về thay đổi lãi suất {topic}.",
                "Tôi đang tiết kiệm tiền để {topic} trong tương lai.",
                "Thị trường {topic} đang có nhiều biến động.",
                "Công ty đã đầu tư vào {topic} để tăng lợi nhuận.",
                "Báo cáo tài chính cho thấy {topic} đang phát triển tốt.",
                "Khách hàng đang quan tâm đến sản phẩm {topic}.",
                "Cổ phiếu {topic} đã tăng giá trong tuần qua.",
                "Bảo hiểm {topic} đang được nhiều người lựa chọn.",
                "Thuế {topic} đã được điều chỉnh theo quy định mới.",
                "Lương của nhân viên {topic} đã được tăng lên."
            ],
            'social': [
                "Xã hội đang quan tâm đến vấn đề {topic}.",
                "Cộng đồng đã tổ chức nhiều hoạt động về {topic}.",
                "Dân số {topic} đang tăng nhanh trong những năm qua.",
                "Văn hóa {topic} đã được bảo tồn và phát triển.",
                "Truyền thống {topic} được truyền từ đời này sang đời khác.",
                "Lễ hội {topic} thu hút nhiều du khách trong và ngoài nước.",
                "Đời sống của người dân {topic} đã được cải thiện.",
                "An sinh xã hội về {topic} đang được quan tâm.",
                "Phát triển {topic} là mục tiêu của chính phủ.",
                "Bình đẳng trong {topic} đã được thực hiện tốt."
            ],
            'economics': [
                "Kinh tế {topic} đang phục hồi sau khủng hoảng.",
                "Thị trường {topic} có nhiều cơ hội cho nhà đầu tư.",
                "Cung cầu {topic} đang cân bằng trong thời gian gần đây.",
                "Giá cả {topic} đã ổn định sau thời gian biến động.",
                "Lạm phát {topic} đã được kiểm soát tốt.",
                "Tăng trưởng {topic} đạt mức cao trong quý này.",
                "Suy thoái {topic} đã được khắc phục.",
                "Khủng hoảng {topic} đã qua đi và kinh tế đang phục hồi.",
                "Phục hồi {topic} đang diễn ra mạnh mẽ.",
                "Ổn định {topic} là mục tiêu của chính sách kinh tế."
            ],
            'general': [
                "Cuộc sống {topic} đang thay đổi nhanh chóng.",
                "Con người {topic} đã thích nghi với môi trường mới.",
                "Thiên nhiên {topic} đang được bảo vệ tốt hơn.",
                "Môi trường {topic} đã được cải thiện đáng kể.",
                "Thời gian {topic} đã trôi qua rất nhanh.",
                "Không gian {topic} đang được khám phá.",
                "Vũ trụ {topic} chứa đựng nhiều bí ẩn.",
                "Trái đất {topic} đang đối mặt với nhiều thách thức.",
                "Mặt trời {topic} đang chiếu sáng rực rỡ.",
                "Mặt trăng {topic} đã xuất hiện trên bầu trời."
            ],
            'history': [
                "Lịch sử {topic} đã được ghi chép chi tiết.",
                "Quá khứ {topic} đã để lại nhiều bài học quý giá.",
                "Truyền thống {topic} được bảo tồn qua nhiều thế hệ.",
                "Văn hóa {topic} đã phát triển rực rỡ.",
                "Di tích {topic} đã được công nhận là di sản.",
                "Di sản {topic} đang được bảo vệ và phát huy.",
                "Cổ vật {topic} đã được khai quật và nghiên cứu.",
                "Khảo cổ {topic} đã phát hiện nhiều điều thú vị.",
                "Nghiên cứu {topic} đã được thực hiện công phu.",
                "Tài liệu {topic} đã được lưu trữ cẩn thận."
            ]
        }
        
        # Từ nối và liên từ tự nhiên
        self.connectors = [
            'và', 'hoặc', 'nhưng', 'tuy nhiên', 'do đó', 'vì vậy', 'nếu', 'khi',
            'sau khi', 'trước khi', 'trong khi', 'mặc dù', 'bởi vì', 'cho nên',
            'để', 'nhằm', 'theo', 'theo như', 'theo đó', 'về', 'về phía', 'về phía'
        ]
        
        # Từ chỉ định và đại từ
        self.determiners = [
            'cái', 'con', 'chiếc', 'quyển', 'cuốn', 'tờ', 'tấm', 'bức', 'ngôi',
            'căn', 'cái', 'đôi', 'bộ', 'bộ', 'dãy', 'dãy', 'hàng', 'hàng'
        ]
        
        # Tính từ phổ biến
        self.adjectives = [
            'tốt', 'xấu', 'đẹp', 'xấu', 'lớn', 'nhỏ', 'cao', 'thấp', 'dài', 'ngắn',
            'rộng', 'hẹp', 'dày', 'mỏng', 'nặng', 'nhẹ', 'nhanh', 'chậm', 'mạnh', 'yếu',
            'sáng', 'tối', 'sạch', 'bẩn', 'mới', 'cũ', 'già', 'trẻ', 'giàu', 'nghèo'
        ]
        
        # Động từ phổ biến
        self.verbs = [
            'làm', 'làm', 'làm', 'làm', 'làm', 'làm', 'làm', 'làm', 'làm', 'làm',
            'học', 'dạy', 'nghiên cứu', 'phát triển', 'cải thiện', 'xây dựng', 'tạo ra', 'thực hiện',
            'quản lý', 'điều hành', 'kiểm soát', 'giám sát', 'đánh giá', 'phân tích', 'tổng hợp', 'báo cáo'
        ]
    
    def generate_natural_sentence(self, category: str, error_rate: float = 0.3) -> Dict:
        """Tạo câu tự nhiên với lỗi chính tả"""
        # Chọn template ngẫu nhiên từ natural_sentences
        templates = self.natural_sentences.get(category, self.natural_sentences['general'])
        template = random.choice(templates)
        
        # Chọn từ vựng theo category
        category_words = self.vocabulary.get(category, [])
        if category_words:
            topic_word = random.choice(category_words)
            location_word = random.choice(['Hà Nội', 'TP.HCM', 'Đà Nẵng', 'Cần Thơ', 'Hải Phòng'])
        else:
            topic_word = 'này'
            location_word = 'đây'
        
        # Thay thế placeholder
        sentence = template.format(topic=topic_word, location=location_word)
        
        # Thêm các yếu tố tự nhiên
        if random.random() < 0.3:
            connector = random.choice(self.connectors)
            sentence = f"{connector.capitalize()} {sentence.lower()}"
        
        if random.random() < 0.2:
            adjective = random.choice(self.adjectives)
            sentence = sentence.replace(topic_word, f"{adjective} {topic_word}")
        
        # Tạo lỗi trong câu
        words = sentence.split()
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
            "correct_sentence": sentence
        }
    
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
    
    def generate_test_cases(self, num_cases: int = 10, categories: List[str] = None) -> List[Dict]:
        """Tạo nhiều test cases với câu tự nhiên"""
        if categories is None:
            categories = list(self.vocabulary.keys())
        
        test_cases = []
        for i in range(num_cases):
            category = random.choice(categories)
            test_case = self.generate_natural_sentence(category)
            test_cases.append(test_case)
        
        return test_cases
    
    def generate_specific_error_test(self, error_type: str, num_cases: int = 5) -> List[Dict]:
        """Tạo test cases với lỗi cụ thể"""
        test_cases = []
        categories = list(self.vocabulary.keys())
        
        for i in range(num_cases):
            category = random.choice(categories)
            test_case = self.generate_natural_sentence(category, error_rate=0.5)
            
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
    
    print("🎲 Vietnamese Spell Checker - Test Data Generator (Improved)")
    print("=" * 60)
    
    # Tạo test cases ngẫu nhiên
    test_cases = generator.generate_test_cases(5)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['category'].upper()}")
        print(f"   Original: {test_case['original']}")
        print(f"   Correct:  {test_case['correct_sentence']}")
        print(f"   Expected corrections: {len(test_case['expected_corrections'])} errors")
        for wrong, correct in test_case['expected_corrections'].items():
            print(f"     '{wrong}' → '{correct}'")

if __name__ == '__main__':
    main()
