#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Auto Evaluation Test Suite for Vietnamese Spell Checker
Hệ thống tự động đánh giá và tính điểm cho Vietnamese Spell Checker
"""

import requests
import json
import time
import statistics
from typing import Dict, List, Tuple
from datetime import datetime
import re

class AutoEvaluator:
    def __init__(self, base_url: str = "http://127.0.0.1:3000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
        
        # Dữ liệu test mẫu với đáp án đúng
        self.test_data = [
            {
                "original": "côn viec kin doanh thì rất kho khan nên toi quyết dinh chuyển sang nghề khac",
                "expected_corrections": {
                    "côn": "công",
                    "viec": "việc", 
                    "kin": "kinh",
                    "doanh": "doanh",
                    "kho": "khó",
                    "khan": "khăn",
                    "toi": "tôi",
                    "quyết": "quyết",
                    "dinh": "định",
                    "chuyển": "chuyển",
                    "sang": "sang",
                    "nghề": "nghề",
                    "khac": "khác"
                },
                "category": "business"
            },
            {
                "original": "toi dang là sinh diên nam hai ở truong đạ hoc khoa jọc tự nhiên , trogn năm ke tiep toi sẽ chọn chuyen nganh về trí tue nhana tạo",
                "expected_corrections": {
                    "toi": "tôi",
                    "dang": "đang",
                    "sinh": "sinh",
                    "diên": "viên",
                    "nam": "Nam",
                    "hai": "Hai",
                    "truong": "trường",
                    "đạ": "đại",
                    "hoc": "học",
                    "khoa": "khoa",
                    "jọc": "học",
                    "tự": "tự",
                    "nhiên": "nhiên",
                    "trogn": "trong",
                    "năm": "năm",
                    "ke": "kế",
                    "tiep": "tiếp",
                    "chọn": "chọn",
                    "chuyen": "chuyên",
                    "nganh": "ngành",
                    "về": "về",
                    "trí": "trí",
                    "tue": "tuệ",
                    "nhana": "nhân",
                    "tạo": "tạo"
                },
                "category": "education"
            },
            {
                "original": "Tôi  đang học AI ở trun tam AI viet nam",
                "expected_corrections": {
                    "Tôi": "Tôi",
                    "đang": "đang",
                    "học": "học",
                    "AI": "AI",
                    "trun": "trung",
                    "tam": "tâm",
                    "AI": "AI",
                    "viet": "Việt",
                    "nam": "Nam"
                },
                "category": "technology"
            },
            {
                "original": "Nhưng sức huỷ divt của cơn bão mitch vẫn chưa thấm vào đâu lsovớithảm hoạ tại Bangladesh ăm 1970",
                "expected_corrections": {
                    "Nhưng": "Nhưng",
                    "sức": "sức",
                    "huỷ": "hủy",
                    "divt": "diệt",
                    "của": "của",
                    "cơn": "cơn",
                    "bão": "bão",
                    "mitch": "Mitch",
                    "vẫn": "vẫn",
                    "chưa": "chưa",
                    "thấm": "thấm",
                    "vào": "vào",
                    "đâu": "đâu",
                    "lsovớithảm": "lso với thảm",
                    "hoạ": "họa",
                    "tại": "tại",
                    "Bangladesh": "Bangladesh",
                    "ăm": "năm",
                    "1970": "1970"
                },
                "category": "news"
            },
            {
                "original": "Lần này anh Phươngqyết xếp hàng mua bằng được 1 chiếc",
                "expected_corrections": {
                    "Lần": "Lần",
                    "này": "này",
                    "anh": "anh",
                    "Phươngqyết": "Phương quyết",
                    "xếp": "xếp",
                    "hàng": "hàng",
                    "mua": "mua",
                    "bằng": "bằng",
                    "được": "được",
                    "1": "1",
                    "chiếc": "chiếc"
                },
                "category": "personal"
            },
            {
                "original": "một số chuyen gia tài chính ngâSn hànG của Việt Nam cũng chung quan điểmnày",
                "expected_corrections": {
                    "một": "một",
                    "số": "số",
                    "chuyen": "chuyên",
                    "gia": "gia",
                    "tài": "tài",
                    "chính": "chính",
                    "ngâSn": "ngân",
                    "hànG": "hàng",
                    "của": "của",
                    "Việt": "Việt",
                    "Nam": "Nam",
                    "cũng": "cũng",
                    "chung": "chung",
                    "quan": "quan",
                    "điểmnày": "điểm này"
                },
                "category": "finance"
            },
            {
                "original": "Cac so liệu cho thay ngươi dân viet nam đang sống trong 1 cuôc sóng không duojc nhu mong đọi",
                "expected_corrections": {
                    "Cac": "Các",
                    "so": "số",
                    "liệu": "liệu",
                    "cho": "cho",
                    "thay": "thấy",
                    "ngươi": "người",
                    "dân": "dân",
                    "viet": "Việt",
                    "nam": "Nam",
                    "đang": "đang",
                    "sống": "sống",
                    "trong": "trong",
                    "1": "1",
                    "cuôc": "cuộc",
                    "sóng": "sống",
                    "không": "không",
                    "duojc": "được",
                    "nhu": "như",
                    "mong": "mong",
                    "đọi": "đợi"
                },
                "category": "social"
            },
            {
                "original": "Nefn kinh té thé giới đang đúng trươc nguyen co của mọt cuoc suy thoai",
                "expected_corrections": {
                    "Nefn": "Nền",
                    "kinh": "kinh",
                    "té": "tế",
                    "thé": "thế",
                    "giới": "giới",
                    "đang": "đang",
                    "đúng": "đứng",
                    "trươc": "trước",
                    "nguyen": "nguy",
                    "co": "cơ",
                    "của": "của",
                    "mọt": "một",
                    "cuoc": "cuộc",
                    "suy": "suy",
                    "thoai": "thoái"
                },
                "category": "economics"
            },
            {
                "original": "Khong phai tất ca nhưng gi chung ta thấy dideu là sụ that",
                "expected_corrections": {
                    "Khong": "Không",
                    "phai": "phải",
                    "tất": "tất",
                    "ca": "cả",
                    "nhưng": "nhưng",
                    "gi": "gì",
                    "chung": "chúng",
                    "ta": "ta",
                    "thấy": "thấy",
                    "dideu": "điều",
                    "là": "là",
                    "sụ": "sự",
                    "that": "thật"
                },
                "category": "general"
            },
            {
                "original": "chinh phủ luôn cố găng het suc để naggna cao chat luong nền giáo duc =cua nuoc nhà",
                "expected_corrections": {
                    "chinh": "chính",
                    "phủ": "phủ",
                    "luôn": "luôn",
                    "cố": "cố",
                    "găng": "gắng",
                    "het": "hết",
                    "suc": "sức",
                    "để": "để",
                    "naggna": "nâng",
                    "cao": "cao",
                    "chat": "chất",
                    "luong": "lượng",
                    "nền": "nền",
                    "giáo": "giáo",
                    "duc": "dục",
                    "=cua": "của",
                    "nuoc": "nước",
                    "nhà": "nhà"
                },
                "category": "education"
            },
            {
                "original": "nèn kinh te thé giới đang đứng trươc nguy co của mọt cuoc suy thoai",
                "expected_corrections": {
                    "nèn": "nền",
                    "kinh": "kinh",
                    "te": "tế",
                    "thé": "thế",
                    "giới": "giới",
                    "đang": "đang",
                    "đứng": "đứng",
                    "trươc": "trước",
                    "nguy": "nguy",
                    "co": "cơ",
                    "của": "của",
                    "mọt": "một",
                    "cuoc": "cuộc",
                    "suy": "suy",
                    "thoai": "thoái"
                },
                "category": "economics"
            },
            {
                "original": "kinh tế viet nam dang dứng truoc 1 thoi ky đổi mơi chưa tung có tienf lệ trong lịch sử",
                "expected_corrections": {
                    "kinh": "kinh",
                    "tế": "tế",
                    "viet": "Việt",
                    "nam": "Nam",
                    "dang": "đang",
                    "dứng": "đứng",
                    "truoc": "trước",
                    "1": "1",
                    "thoi": "thời",
                    "ky": "kỳ",
                    "đổi": "đổi",
                    "mơi": "mới",
                    "chưa": "chưa",
                    "tung": "từng",
                    "có": "có",
                    "tienf": "tiền",
                    "lệ": "lệ",
                    "trong": "trong",
                    "lịch": "lịch",
                    "sử": "sử"
                },
                "category": "history"
            }
        ]
    
    def evaluate_correction(self, original_text: str, corrected_text: str, expected_corrections: Dict[str, str]) -> Dict:
        """Đánh giá độ chính xác của việc sửa lỗi"""
        
        # Tách từ trong văn bản gốc và đã sửa
        original_words = re.findall(r'\b\w+\b', original_text.lower())
        corrected_words = re.findall(r'\b\w+\b', corrected_text.lower())
        
        # Đếm số lỗi được phát hiện và sửa đúng
        detected_errors = 0
        corrected_errors = 0
        false_positives = 0
        missed_errors = 0
        
        # Kiểm tra từng từ trong expected_corrections
        for wrong_word, correct_word in expected_corrections.items():
            wrong_word_lower = wrong_word.lower()
            correct_word_lower = correct_word.lower()
            
            # Kiểm tra xem lỗi có được phát hiện không
            if wrong_word_lower in original_words:
                detected_errors += 1
                
                # Kiểm tra xem lỗi có được sửa đúng không
                if correct_word_lower in corrected_words:
                    corrected_errors += 1
                else:
                    missed_errors += 1
        
        # Tính toán các metrics
        total_expected_errors = len(expected_corrections)
        precision = corrected_errors / detected_errors if detected_errors > 0 else 0
        recall = corrected_errors / total_expected_errors if total_expected_errors > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        accuracy = corrected_errors / total_expected_errors if total_expected_errors > 0 else 0
        
        return {
            'total_expected_errors': total_expected_errors,
            'detected_errors': detected_errors,
            'corrected_errors': corrected_errors,
            'missed_errors': missed_errors,
            'false_positives': false_positives,
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'accuracy': accuracy,
            'score_percentage': accuracy * 100
        }
    
    def test_spell_checking(self, test_case: Dict) -> Dict:
        """Test spell checking cho một test case"""
        try:
            start_time = time.time()
            
            # Gửi request kiểm tra chính tả
            response = self.session.post(
                f"{self.base_url}/api/check_spelling",
                json={"text": test_case["original"]},
                timeout=30
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                result = response.json()
                
                # Đánh giá kết quả
                evaluation = self.evaluate_correction(
                    test_case["original"],
                    result.get('corrected_text', ''),
                    test_case["expected_corrections"]
                )
                
                return {
                    'test_case': test_case,
                    'response': result,
                    'evaluation': evaluation,
                    'processing_time': processing_time,
                    'success': True
                }
            else:
                return {
                    'test_case': test_case,
                    'response': None,
                    'evaluation': None,
                    'processing_time': processing_time,
                    'success': False,
                    'error': f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                'test_case': test_case,
                'response': None,
                'evaluation': None,
                'processing_time': 0,
                'success': False,
                'error': str(e)
            }
    
    def run_all_tests(self) -> Dict:
        """Chạy tất cả test cases và tính toán tổng kết"""
        print("🎯 Vietnamese Spell Checker - Auto Evaluation Test Suite")
        print("=" * 60)
        
        all_results = []
        total_score = 0
        total_tests = len(self.test_data)
        
        for i, test_case in enumerate(self.test_data, 1):
            print(f"\n📝 Test {i}/{total_tests}: {test_case['category'].upper()}")
            print(f"   Original: {test_case['original'][:50]}...")
            
            result = self.test_spell_checking(test_case)
            all_results.append(result)
            
            if result['success'] and result['evaluation']:
                evaluation = result['evaluation']
                score = evaluation['score_percentage']
                total_score += score
                
                print(f"   ✅ Score: {score:.1f}%")
                print(f"   📊 Precision: {evaluation['precision']:.2f}")
                print(f"   📊 Recall: {evaluation['recall']:.2f}")
                print(f"   📊 F1-Score: {evaluation['f1_score']:.2f}")
                print(f"   ⏱️  Time: {result['processing_time']:.2f}ms")
            else:
                print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
        
        # Tính toán tổng kết
        average_score = total_score / total_tests if total_tests > 0 else 0
        
        # Phân tích theo category
        category_scores = {}
        for result in all_results:
            if result['success'] and result['evaluation']:
                category = result['test_case']['category']
                if category not in category_scores:
                    category_scores[category] = []
                category_scores[category].append(result['evaluation']['score_percentage'])
        
        category_averages = {}
        for category, scores in category_scores.items():
            category_averages[category] = statistics.mean(scores)
        
        # Tạo báo cáo tổng kết
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': total_tests,
            'successful_tests': len([r for r in all_results if r['success']]),
            'average_score': average_score,
            'category_scores': category_averages,
            'detailed_results': all_results,
            'performance_stats': {
                'average_processing_time': statistics.mean([r['processing_time'] for r in all_results if r['success']]),
                'total_processing_time': sum([r['processing_time'] for r in all_results if r['success']])
            }
        }
        
        # In báo cáo tổng kết
        print(f"\n🎯 TỔNG KẾT ĐÁNH GIÁ")
        print("=" * 60)
        print(f"📊 Tổng số test: {total_tests}")
        print(f"✅ Test thành công: {summary['successful_tests']}")
        print(f"🎯 Điểm trung bình: {average_score:.1f}%")
        print(f"⏱️  Thời gian xử lý trung bình: {summary['performance_stats']['average_processing_time']:.2f}ms")
        
        print(f"\n📈 ĐIỂM THEO DANH MỤC:")
        for category, score in category_averages.items():
            print(f"   {category.upper()}: {score:.1f}%")
        
        # Đánh giá tổng thể
        if average_score >= 90:
            grade = "A+ (Xuất sắc)"
        elif average_score >= 80:
            grade = "A (Tốt)"
        elif average_score >= 70:
            grade = "B (Khá)"
        elif average_score >= 60:
            grade = "C (Trung bình)"
        else:
            grade = "D (Cần cải thiện)"
        
        print(f"\n🏆 ĐÁNH GIÁ TỔNG THỂ: {grade}")
        
        return summary
    
    def save_results(self, results: Dict, filename: str = None):
        """Lưu kết quả vào file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"evaluation_results_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Kết quả đã được lưu vào: {filename}")
        return filename

def main():
    """Main function"""
    evaluator = AutoEvaluator()
    
    # Chạy tất cả test
    results = evaluator.run_all_tests()
    
    # Lưu kết quả
    filename = evaluator.save_results(results)
    
    print(f"\n🎉 Hoàn thành đánh giá tự động!")
    print(f"📁 Kết quả chi tiết: {filename}")

if __name__ == '__main__':
    main()
