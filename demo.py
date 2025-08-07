#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo Vietnamese Spell Checker
Chạy demo để test chức năng kiểm tra chính tả
"""

from spell_checker import VietnameseSpellChecker
import time

def demo_spell_checker():
    """Demo chức năng spell checker"""
    
    print("🎯 Vietnamese Spell Checker Demo")
    print("=" * 50)
    
    # Khởi tạo spell checker
    print("🔧 Khởi tạo spell checker...")
    spell_checker = VietnameseSpellChecker()
    
    # Test cases
    test_cases = [
        {
            "name": "Văn bản đúng chính tả",
            "text": "Tôi là học sinh giỏi. Tôi thích đọc sách và viết văn."
        },
        {
            "name": "Văn bản có lỗi chính tả",
            "text": "Tôii là học sinhh giỏi. Tôii thích đọc sách và viết văn."
        },
        {
            "name": "Văn bản phức tạp",
            "text": "Hôm nay tôii đi học ở trường. Thầy giáo dạy tôii rất nhiều điều bổ ích. Tôii cảm thấy rất vui vẻ."
        },
        {
            "name": "Văn bản có từ mới",
            "text": "Công nghệ AI đang phát triển nhanh chóng. Máy học và trí tuệ nhân tạo đã thay đổi cuộc sống."
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['name']}")
        print("-" * 30)
        print(f"Văn bản gốc: {test_case['text']}")
        
        # Kiểm tra chính tả
        start_time = time.time()
        result = spell_checker.check_text(test_case['text'])
        end_time = time.time()
        
        # Hiển thị kết quả
        print(f"⏱️  Thời gian xử lý: {((end_time - start_time) * 1000):.1f}ms")
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
        
        print()

def demo_suggestions():
    """Demo chức năng gợi ý"""
    
    print("💡 Demo gợi ý sửa lỗi")
    print("=" * 30)
    
    spell_checker = VietnameseSpellChecker()
    
    test_words = [
        "tôii",
        "bạnn", 
        "nhàa",
        "cửaa",
        "học sinhh",
        "thầy giáoo"
    ]
    
    for word in test_words:
        print(f"\n🔍 Từ: '{word}'")
        suggestions = spell_checker.get_suggestions(word)
        if suggestions:
            print(f"💡 Gợi ý: {', '.join(suggestions[:5])}")
        else:
            print("❌ Không có gợi ý")

def demo_performance():
    """Demo hiệu suất"""
    
    print("⚡ Demo hiệu suất")
    print("=" * 20)
    
    spell_checker = VietnameseSpellChecker()
    
    # Test với văn bản dài
    long_text = """
    Tôii là một học sinhh giỏi của trường. Hôm nay tôii đi học rất sớm.
    Thầy giáo dạy tôii rất nhiều điều bổ ích về công nghệ và khoa học.
    Tôii thích đọc sách và viết văn. Tôii cũng thích chơi thể thao.
    Mỗi ngày tôii đều cố gắng học tập chăm chỉ để trở thành người có ích.
    """
    
    print("📊 Test hiệu suất với văn bản dài...")
    
    # Test nhiều lần để tính trung bình
    times = []
    for i in range(5):
        start_time = time.time()
        result = spell_checker.check_text(long_text)
        end_time = time.time()
        times.append((end_time - start_time) * 1000)
    
    avg_time = sum(times) / len(times)
    print(f"⏱️  Thời gian trung bình: {avg_time:.1f}ms")
    print(f"📈 Số từ xử lý: {len(long_text.split())}")
    print(f"🚀 Tốc độ: {len(long_text.split()) / (avg_time / 1000):.1f} từ/giây")

def main():
    """Hàm chính"""
    
    print("🎯 Vietnamese Spell Checker - GPT-OSS Demo")
    print("=" * 60)
    
    try:
        # Demo chính
        demo_spell_checker()
        
        # Demo gợi ý
        demo_suggestions()
        
        # Demo hiệu suất
        demo_performance()
        
        print("\n✅ Demo hoàn thành!")
        print("🚀 Để chạy ứng dụng web, hãy sử dụng: python app.py")
        
    except Exception as e:
        print(f"❌ Lỗi trong demo: {e}")
        print("💡 Hãy đảm bảo đã cài đặt đầy đủ dependencies")

if __name__ == '__main__':
    main() 