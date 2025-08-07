#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test Vietnamese Spell Checker với dữ liệu thực tế
"""

from spell_checker import VietnameseSpellChecker
import time

def test_real_data():
    """Test với dữ liệu thực tế từ user"""
    
    print("🧪 Test Vietnamese Spell Checker với dữ liệu thực tế")
    print("=" * 60)
    
    # Khởi tạo spell checker
    spell_checker = VietnameseSpellChecker()
    
    # Dữ liệu test từ user
    test_cases = [
        "côn viec kin doanh thì rất kho khan nên toi quyết dinh chuyển sang nghề khac",
        "toi dang là sinh diên nam hai ở truong đạ hoc khoa jọc tự nhiên , trogn năm ke tiep toi sẽ chọn chuyen nganh về trí tue nana tạo",
        "Tôi  đang học AI ở trun tam AI viet nam",
        "Nhưng sức huỷ divt của cơn bão mitch vẫn chưa thấm vào đâu lsovớithảm hoạ tại Bangladesh ăm 1970",
        "Lần này anh Phươngqyết xếp hàng mua bằng được 1 chiếc",
        "một số chuyen gia tài chính ngâSn hànG của Việt Nam cũng chung quan điểmnày",
        "Cac so liệu cho thay ngươi dân viet nam đang sống trong 1 cuôc sóng không duojc nhu mong đọi",
        "Nefn kinh té thé giới đang đúng trươc nguyen co của mọt cuoc suy thoai",
        "Khong phai tất ca nhưng gi chung ta thấy dideu là sụ that",
        "chinh phủ luôn cố găng het suc để naggna cao chat luong nền giáo duc =cua nuoc nhà",
        "nèn kinh te thé giới đang đứng trươc nguy co của mọt cuoc suy thoai",
        "kinh tế viet nam dang dứng truoc 1 thoi ky đổi mơi chưa tung có tienf lệ trong lịch sử"
    ]
    
    total_errors = 0
    total_words = 0
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}:")
        print(f"Văn bản gốc: {text}")
        
        # Kiểm tra chính tả
        start_time = time.time()
        result = spell_checker.check_text(text)
        end_time = time.time()
        
        # Hiển thị kết quả
        processing_time = (end_time - start_time) * 1000
        print(f"⏱️  Thời gian xử lý: {processing_time:.1f}ms")
        print(f"🔍 Số lỗi tìm thấy: {result['error_count']}")
        print(f"📊 Độ tin cậy: {result['confidence']:.1%}")
        
        if result['error_count'] > 0:
            print(f"✅ Văn bản đã sửa: {result['corrected_text']}")
            print("🔧 Chi tiết lỗi:")
            for error in result['errors']:
                print(f"   - '{error['word']}' → '{error['corrected']}'")
                print(f"     Gợi ý: {', '.join(error['suggestions'][:3])}")
        else:
            print("✅ Không tìm thấy lỗi chính tả!")
        
        total_errors += result['error_count']
        total_words += len(text.split())
        
        print("-" * 50)
    
    # Thống kê tổng quan
    print(f"\n📊 Thống kê tổng quan:")
    print(f"   Tổng số từ kiểm tra: {total_words}")
    print(f"   Tổng số lỗi phát hiện: {total_errors}")
    print(f"   Tỷ lệ lỗi: {total_errors/total_words*100:.1f}%")
    print(f"   Hiệu suất trung bình: {total_words/(processing_time/1000):.1f} từ/giây")

def test_individual_words():
    """Test từng từ riêng lẻ"""
    
    print("\n🔍 Test từng từ riêng lẻ:")
    print("=" * 40)
    
    spell_checker = VietnameseSpellChecker()
    
    # Danh sách từ cần test
    test_words = [
        "côn", "viec", "kin", "doanh", "kho", "khan", "toi", "quyết", "dinh",
        "sinh", "diên", "truong", "đạ", "hoc", "jọc", "tue", "nana", "tạo",
        "trun", "tam", "viet", "nam", "huỷ", "divt", "lsovới", "thảm", "hoạ",
        "Phươngqyết", "ngâSn", "hànG", "điểmnày", "Cac", "thay", "ngươi",
        "cuôc", "sóng", "duojc", "nhu", "đọi", "Nefn", "té", "thé", "đúng",
        "trươc", "nguyen", "co", "mọt", "cuoc", "thoai", "Khong", "phai",
        "ca", "gi", "dideu", "sụ", "that", "chinh", "găng", "het", "suc",
        "naggna", "chat", "luong", "duc", "nuoc", "nèn", "đứng", "nguy",
        "thoi", "ky", "mơi", "tung", "tienf", "lệ", "sử"
    ]
    
    for word in test_words:
        is_correct = spell_checker._is_correct_word(word)
        suggestions = spell_checker.get_suggestions(word)
        
        status = "✅" if is_correct else "❌"
        print(f"{status} '{word}' → {'ĐÚNG' if is_correct else 'SAI'}")
        if not is_correct and suggestions:
            print(f"    💡 Gợi ý: {', '.join(suggestions[:3])}")

if __name__ == '__main__':
    test_real_data()
    test_individual_words() 