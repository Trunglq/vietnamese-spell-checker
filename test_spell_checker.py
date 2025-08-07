#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from spell_checker import VietnameseSpellChecker

class TestVietnameseSpellChecker(unittest.TestCase):
    
    def setUp(self):
        """Khởi tạo spell checker cho test"""
        self.spell_checker = VietnameseSpellChecker()
    
    def test_vietnamese_dictionary(self):
        """Test từ điển tiếng Việt cơ bản"""
        # Test các từ đúng
        correct_words = ['tôi', 'bạn', 'nhà', 'cửa', 'sách', 'vở']
        for word in correct_words:
            self.assertTrue(self.spell_checker._is_correct_word(word))
        
        # Test các từ sai
        incorrect_words = ['tôii', 'bạnn', 'nhàa', 'cửaa']
        for word in incorrect_words:
            self.assertFalse(self.spell_checker._is_correct_word(word))
    
    def test_similarity_calculation(self):
        """Test tính độ tương đồng giữa các từ"""
        # Test từ giống nhau
        self.assertEqual(self.spell_checker._similarity('tôi', 'tôi'), 1.0)
        
        # Test từ khác nhau
        self.assertLess(self.spell_checker._similarity('tôi', 'bạn'), 1.0)
        
        # Test từ tương tự
        similarity = self.spell_checker._similarity('tôii', 'tôi')
        self.assertGreater(similarity, 0.5)
    
    def test_text_checking(self):
        """Test kiểm tra văn bản"""
        # Test văn bản đúng
        correct_text = "Tôi là học sinh"
        result = self.spell_checker.check_text(correct_text)
        self.assertEqual(result['error_count'], 0)
        self.assertEqual(result['original_text'], correct_text)
        self.assertEqual(result['corrected_text'], correct_text)
        
        # Test văn bản có lỗi
        incorrect_text = "Tôii là học sinhh"
        result = self.spell_checker.check_text(incorrect_text)
        self.assertGreater(result['error_count'], 0)
        self.assertNotEqual(result['original_text'], result['corrected_text'])
    
    def test_suggestions(self):
        """Test gợi ý sửa lỗi"""
        # Test gợi ý cho từ sai
        suggestions = self.spell_checker.get_suggestions('tôii')
        self.assertIsInstance(suggestions, list)
        self.assertGreater(len(suggestions), 0)
        
        # Test gợi ý cho từ đúng
        suggestions = self.spell_checker.get_suggestions('tôi')
        self.assertIsInstance(suggestions, list)
    
    def test_confidence_calculation(self):
        """Test tính độ tin cậy"""
        # Test văn bản không có lỗi
        result = self.spell_checker.check_text("Tôi là học sinh")
        self.assertGreaterEqual(result['confidence'], 0.8)
        
        # Test văn bản có nhiều lỗi
        result = self.spell_checker.check_text("Tôii là học sinhh")
        self.assertLess(result['confidence'], 0.8)
    
    def test_error_detection(self):
        """Test phát hiện lỗi cụ thể"""
        test_cases = [
            ("Tôii", "Tôi"),
            ("bạnn", "bạn"),
            ("nhàa", "nhà"),
            ("cửaa", "cửa")
        ]
        
        for incorrect, correct in test_cases:
            result = self.spell_checker.check_text(incorrect)
            self.assertGreater(result['error_count'], 0)
            
            # Kiểm tra xem có gợi ý đúng không
            suggestions = self.spell_checker.get_suggestions(incorrect)
            self.assertIn(correct, suggestions)
    
    def test_complex_text(self):
        """Test văn bản phức tạp"""
        complex_text = """
        Tôii là một học sinhh giỏi. Tôii thích đọc sách và viết văn.
        Hôm nay tôii đi học ở trường. Thầy giáo dạy tôii rất nhiều điều bổ ích.
        """
        
        result = self.spell_checker.check_text(complex_text)
        self.assertGreater(result['error_count'], 0)
        self.assertNotEqual(result['original_text'], result['corrected_text'])
    
    def test_empty_text(self):
        """Test văn bản rỗng"""
        result = self.spell_checker.check_text("")
        self.assertEqual(result['error_count'], 0)
        self.assertEqual(result['confidence'], 1.0)
    
    def test_special_characters(self):
        """Test văn bản có ký tự đặc biệt"""
        text_with_special = "Tôi! là học sinh? Có 123 số và @#$ ký tự đặc biệt."
        result = self.spell_checker.check_text(text_with_special)
        self.assertIsInstance(result, dict)
        self.assertIn('original_text', result)
        self.assertIn('corrected_text', result)

def run_tests():
    """Chạy tất cả tests"""
    print("🧪 Chạy tests cho Vietnamese Spell Checker...")
    print("=" * 50)
    
    # Tạo test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVietnameseSpellChecker)
    
    # Chạy tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # In kết quả
    print("\n" + "=" * 50)
    print(f"📊 Kết quả tests:")
    print(f"   ✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"   ❌ Failed: {len(result.failures)}")
    print(f"   ⚠️  Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback}")
    
    if result.errors:
        print("\n⚠️  Errors:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1) 