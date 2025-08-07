#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vietnamese Dictionary for Spell Checker
Từ điển tiếng Việt mở rộng cho spell checker
"""

import json
import os
from typing import Set, Dict, List

class VietnameseDictionary:
    """Từ điển tiếng Việt với các từ phổ biến"""
    
    def __init__(self):
        self.words = self._load_dictionary()
        self.common_errors = self._load_common_errors()
        self.word_frequency = self._load_frequency()
    
    def _load_dictionary(self) -> Set[str]:
        """Tải từ điển cơ bản"""
        basic_words = {
            # Đại từ nhân xưng
            'tôi', 'bạn', 'chúng', 'ta', 'chúng ta', 'tôi', 'bạn', 'anh', 'chị', 'em',
            'ông', 'bà', 'cô', 'chú', 'bác', 'dì', 'cậu', 'mợ', 'thím', 'cậu',
            
            # Động từ cơ bản
            'là', 'có', 'không', 'đang', 'đã', 'sẽ', 'phải', 'cần', 'muốn', 'thích',
            'học', 'dạy', 'làm', 'đi', 'đến', 'về', 'ở', 'tại', 'trong', 'ngoài',
            'trên', 'dưới', 'bên', 'cạnh', 'giữa', 'trước', 'sau', 'trong', 'ngoài',
            
            # Danh từ cơ bản
            'người', 'nhà', 'cửa', 'bàn', 'ghế', 'sách', 'vở', 'bút', 'mực', 'giấy',
            'nước', 'trời', 'đất', 'cây', 'hoa', 'lá', 'quả', 'trái', 'cây', 'rễ',
            'thân', 'cành', 'nhánh', 'lá', 'hoa', 'quả', 'hạt', 'mầm', 'chồi', 'lộc',
            
            # Từ chỉ thời gian
            'mùa', 'xuân', 'hạ', 'thu', 'đông', 'năm', 'tháng', 'tuần', 'ngày', 'giờ',
            'phút', 'giây', 'sáng', 'trưa', 'chiều', 'tối', 'đêm', 'hôm', 'nay', 'mai',
            
            # Từ chỉ địa điểm
            'sông', 'biển', 'núi', 'đồi', 'đường', 'phố', 'làng', 'xóm', 'thôn', 'xã',
            'huyện', 'tỉnh', 'thành', 'phố', 'quốc', 'gia', 'dân', 'tộc', 'đất', 'nước',
            
            # Từ chỉ nghề nghiệp
            'giáo viên', 'học sinh', 'sinh viên', 'kỹ sư', 'bác sĩ', 'luật sư', 'nhà báo',
            'công nhân', 'nông dân', 'thương nhân', 'doanh nhân', 'chuyên gia', 'nhà khoa học',
            
            # Từ chỉ giáo dục
            'trường', 'học', 'lớp', 'khóa', 'kỳ', 'năm', 'tháng', 'tuần', 'ngày',
            'giáo viên', 'học sinh', 'sinh viên', 'giảng viên', 'giáo sư', 'tiến sĩ',
            'thạc sĩ', 'cử nhân', 'tốt nghiệp', 'tuyển sinh', 'thi cử', 'điểm số',
            
            # Từ chỉ công nghệ
            'máy tính', 'điện thoại', 'internet', 'website', 'email', 'facebook', 'youtube',
            'google', 'microsoft', 'apple', 'samsung', 'intel', 'amd', 'nvidia',
            'trí tuệ nhân tạo', 'machine learning', 'deep learning', 'neural network',
            'algorithm', 'database', 'programming', 'software', 'hardware', 'cloud',
            
            # Từ chỉ kinh tế
            'kinh tế', 'tài chính', 'ngân hàng', 'công ty', 'doanh nghiệp', 'thị trường',
            'đầu tư', 'tiết kiệm', 'chi tiêu', 'thu nhập', 'lợi nhuận', 'thua lỗ',
            'tăng trưởng', 'phát triển', 'suy thoái', 'khủng hoảng', 'ổn định',
            
            # Từ chỉ chính trị
            'chính phủ', 'quốc hội', 'tổng thống', 'thủ tướng', 'bộ trưởng', 'chủ tịch',
            'đảng', 'chính sách', 'luật pháp', 'hiến pháp', 'bầu cử', 'dân chủ',
            
            # Từ chỉ văn hóa
            'văn hóa', 'nghệ thuật', 'âm nhạc', 'hội họa', 'văn học', 'thơ ca',
            'tiểu thuyết', 'truyện ngắn', 'bài hát', 'bộ phim', 'kịch', 'múa',
            
            # Từ chỉ thể thao
            'bóng đá', 'bóng rổ', 'tennis', 'cầu lông', 'bơi lội', 'chạy bộ',
            'gym', 'yoga', 'võ thuật', 'boxing', 'karate', 'taekwondo',
            
            # Từ chỉ ẩm thực
            'cơm', 'phở', 'bún', 'bánh', 'thịt', 'cá', 'rau', 'củ', 'quả',
            'nước mắm', 'dầu ăn', 'muối', 'đường', 'bột', 'sữa', 'trà', 'cà phê',
            
            # Từ chỉ giao thông
            'xe', 'ô tô', 'xe máy', 'xe đạp', 'tàu', 'máy bay', 'tàu điện',
            'xe buýt', 'taxi', 'grab', 'uber', 'đường', 'cầu', 'hầm', 'cảng',
            
            # Từ chỉ y tế
            'bệnh viện', 'phòng khám', 'bác sĩ', 'y tá', 'dược sĩ', 'thuốc',
            'khám bệnh', 'chữa bệnh', 'phẫu thuật', 'tiêm', 'uống thuốc',
            
            # Từ chỉ môi trường
            'môi trường', 'ô nhiễm', 'bảo vệ', 'xanh', 'sạch', 'đẹp', 'rừng',
            'biển', 'sông', 'hồ', 'không khí', 'nước', 'đất', 'ánh sáng',
            
            # Số đếm
            'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín', 'mười',
            'mười một', 'mười hai', 'mười ba', 'mười bốn', 'mười lăm', 'mười sáu',
            'mười bảy', 'mười tám', 'mười chín', 'hai mươi', 'ba mươi', 'bốn mươi',
            'năm mươi', 'sáu mươi', 'bảy mươi', 'tám mươi', 'chín mươi', 'một trăm',
            
            # Từ chỉ màu sắc
            'đỏ', 'xanh', 'vàng', 'trắng', 'đen', 'nâu', 'tím', 'cam', 'hồng',
            'xám', 'bạc', 'vàng', 'xanh lá', 'xanh dương', 'xanh da trời',
            
            # Từ chỉ kích thước
            'lớn', 'nhỏ', 'to', 'bé', 'cao', 'thấp', 'dài', 'ngắn', 'rộng', 'hẹp',
            'dày', 'mỏng', 'nặng', 'nhẹ', 'nhanh', 'chậm', 'xa', 'gần',
            
            # Từ chỉ cảm xúc
            'vui', 'buồn', 'giận', 'sợ', 'ngạc nhiên', 'thích', 'ghét', 'yêu',
            'thương', 'nhớ', 'mong', 'hy vọng', 'thất vọng', 'tự hào', 'xấu hổ',
            
            # Từ chỉ thời tiết
            'nắng', 'mưa', 'gió', 'bão', 'lũ', 'lụt', 'hạn', 'nóng', 'lạnh',
            'ấm', 'mát', 'ẩm', 'khô', 'trời', 'mây', 'sương', 'sương mù',
        }
        return basic_words
    
    def _load_common_errors(self) -> Dict[str, str]:
        """Tải các lỗi chính tả phổ biến"""
        return {
            # Lỗi dấu thanh
            'côn': 'công', 'kin': 'kính', 'sinh diên': 'sinh viên',
            'truong': 'trường', 'dạ': 'đại', 'jọc': 'học', 'tue': 'tuệ',
            'nana': 'nhân', 'tạo': 'tạo', 'trun': 'trung', 'tam': 'tâm',
            'viet': 'Việt', 'nam': 'Nam', 'divt': 'dịch', 'lsovới': 'so với',
            'thảm': 'thảm', 'hoạ': 'họa', 'ăm': 'năm', 'Phươngqyết': 'Phương quyết',
            'ngâSn': 'ngân', 'hànG': 'hàng', 'Việt': 'Việt', 'Nam': 'Nam',
            'chung': 'chung', 'quan': 'quan', 'điểmnày': 'điểm này',
            'Cac': 'Các', 'so': 'số', 'liệu': 'liệu', 'cho': 'cho', 'thay': 'thấy',
            'ngươi': 'người', 'dân': 'dân', 'viet': 'Việt', 'nam': 'Nam',
            'đang': 'đang', 'sống': 'sống', 'trong': 'trong', 'cuôc': 'cuộc',
            'sóng': 'sống', 'không': 'không', 'duojc': 'được', 'nhu': 'như',
            'mong': 'mong', 'đọi': 'đợi', 'Nefn': 'Nền', 'kinh': 'kinh',
            'té': 'tế', 'thé': 'thế', 'giới': 'giới', 'đang': 'đang',
            'đúng': 'đứng', 'trươc': 'trước', 'nguyen': 'nguy', 'co': 'cơ',
            'của': 'của', 'mọt': 'một', 'cuoc': 'cuộc', 'suy': 'suy',
            'thoai': 'thoái', 'Khong': 'Không', 'phai': 'phải', 'tất': 'tất',
            'ca': 'cả', 'nhưng': 'nhưng', 'gi': 'gì', 'chung': 'chúng',
            'ta': 'ta', 'thấy': 'thấy', 'dideu': 'điều', 'là': 'là',
            'sụ': 'sự', 'that': 'thật', 'chinh': 'chính', 'phủ': 'phủ',
            'luôn': 'luôn', 'cố': 'cố', 'găng': 'gắng', 'het': 'hết',
            'suc': 'sức', 'để': 'để', 'naggna': 'nâng', 'cao': 'cao',
            'chat': 'chất', 'luong': 'lượng', 'nền': 'nền', 'giáo': 'giáo',
            'duc': 'dục', 'của': 'của', 'nuoc': 'nước', 'nhà': 'nhà',
            'nèn': 'nền', 'kinh': 'kinh', 'té': 'tế', 'thé': 'thế',
            'giới': 'giới', 'đang': 'đang', 'đứng': 'đứng', 'trươc': 'trước',
            'nguy': 'nguy', 'co': 'cơ', 'của': 'của', 'mọt': 'một',
            'cuoc': 'cuộc', 'suy': 'suy', 'thoai': 'thoái', 'kinh': 'kinh',
            'tế': 'tế', 'viet': 'Việt', 'nam': 'Nam', 'dang': 'đang',
            'dứng': 'đứng', 'truoc': 'trước', 'thoi': 'thời', 'ky': 'kỳ',
            'đổi': 'đổi', 'mơi': 'mới', 'chưa': 'chưa', 'tung': 'từng',
            'có': 'có', 'tienf': 'tiền', 'lệ': 'lệ', 'trong': 'trong',
            'lịch': 'lịch', 'sử': 'sử',
            
            # Lỗi dấu câu
            'toi': 'tôi', 'dinh': 'định', 'chuyen': 'chuyển', 'sang': 'sang',
            'nghe': 'nghề', 'khac': 'khác', 'dang': 'đang', 'sinh': 'sinh',
            'diên': 'viên', 'nam': 'năm', 'hai': 'hai', 'truong': 'trường',
            'đạ': 'đại', 'hoc': 'học', 'khoa': 'khoa', 'jọc': 'học',
            'tự': 'tự', 'nhiên': 'nhiên', 'trogn': 'trong', 'năm': 'năm',
            'ke': 'kế', 'tiep': 'tiếp', 'toi': 'tôi', 'sẽ': 'sẽ',
            'chọn': 'chọn', 'chuyen': 'chuyên', 'nganh': 'ngành', 'về': 'về',
            'trí': 'trí', 'tue': 'tuệ', 'nana': 'nhân', 'tạo': 'tạo',
            'Tôi': 'Tôi', 'đang': 'đang', 'học': 'học', 'AI': 'AI',
            'trun': 'trung', 'tam': 'tâm', 'AI': 'AI', 'viet': 'Việt',
            'nam': 'Nam', 'Nhưng': 'Nhưng', 'sức': 'sức', 'huỷ': 'hủy',
            'divt': 'dịch', 'của': 'của', 'cơn': 'cơn', 'bão': 'bão',
            'mitch': 'Mitch', 'vẫn': 'vẫn', 'chưa': 'chưa', 'thấm': 'thấm',
            'vào': 'vào', 'đâu': 'đâu', 'lsovới': 'so với', 'thảm': 'thảm',
            'hoạ': 'họa', 'tại': 'tại', 'Bangladesh': 'Bangladesh', 'ăm': 'năm',
            'Lần': 'Lần', 'này': 'này', 'anh': 'anh', 'Phươngqyết': 'Phương quyết',
            'xếp': 'xếp', 'hàng': 'hàng', 'mua': 'mua', 'bằng': 'bằng',
            'được': 'được', 'chiếc': 'chiếc', 'một': 'một', 'số': 'số',
            'chuyen': 'chuyên', 'gia': 'gia', 'tài': 'tài', 'chính': 'chính',
            'ngâSn': 'ngân', 'hànG': 'hàng', 'của': 'của', 'Việt': 'Việt',
            'Nam': 'Nam', 'cũng': 'cũng', 'chung': 'chung', 'quan': 'quan',
            'điểmnày': 'điểm này', 'Cac': 'Các', 'so': 'số', 'liệu': 'liệu',
            'cho': 'cho', 'thay': 'thấy', 'ngươi': 'người', 'dân': 'dân',
            'viet': 'Việt', 'nam': 'Nam', 'đang': 'đang', 'sống': 'sống',
            'trong': 'trong', 'cuôc': 'cuộc', 'sóng': 'sống', 'không': 'không',
            'duojc': 'được', 'nhu': 'như', 'mong': 'mong', 'đọi': 'đợi',
            'Nefn': 'Nền', 'kinh': 'kinh', 'té': 'tế', 'thé': 'thế',
            'giới': 'giới', 'đang': 'đang', 'đúng': 'đứng', 'trươc': 'trước',
            'nguyen': 'nguy', 'co': 'cơ', 'của': 'của', 'mọt': 'một',
            'cuoc': 'cuộc', 'suy': 'suy', 'thoai': 'thoái', 'Khong': 'Không',
            'phai': 'phải', 'tất': 'tất', 'ca': 'cả', 'nhưng': 'nhưng',
            'gi': 'gì', 'chung': 'chúng', 'ta': 'ta', 'thấy': 'thấy',
            'dideu': 'điều', 'là': 'là', 'sụ': 'sự', 'that': 'thật',
            'chinh': 'chính', 'phủ': 'phủ', 'luôn': 'luôn', 'cố': 'cố',
            'găng': 'gắng', 'het': 'hết', 'suc': 'sức', 'để': 'để',
            'naggna': 'nâng', 'cao': 'cao', 'chat': 'chất', 'luong': 'lượng',
            'nền': 'nền', 'giáo': 'giáo', 'duc': 'dục', 'của': 'của',
            'nuoc': 'nước', 'nhà': 'nhà', 'nèn': 'nền', 'kinh': 'kinh',
            'té': 'tế', 'thé': 'thế', 'giới': 'giới', 'đang': 'đang',
            'đứng': 'đứng', 'trươc': 'trước', 'nguy': 'nguy', 'co': 'cơ',
            'của': 'của', 'mọt': 'một', 'cuoc': 'cuộc', 'suy': 'suy',
            'thoai': 'thoái', 'kinh': 'kinh', 'tế': 'tế', 'viet': 'Việt',
            'nam': 'Nam', 'dang': 'đang', 'dứng': 'đứng', 'truoc': 'trước',
            'thoi': 'thời', 'ky': 'kỳ', 'đổi': 'đổi', 'mơi': 'mới',
            'chưa': 'chưa', 'tung': 'từng', 'có': 'có', 'tienf': 'tiền',
            'lệ': 'lệ', 'trong': 'trong', 'lịch': 'lịch', 'sử': 'sử',
        }
    
    def _load_frequency(self) -> Dict[str, int]:
        """Tải tần suất sử dụng từ"""
        return {
            'tôi': 1000, 'bạn': 800, 'là': 900, 'có': 850, 'không': 750,
            'đang': 600, 'đã': 550, 'sẽ': 500, 'phải': 450, 'cần': 400,
            'muốn': 350, 'thích': 300, 'học': 250, 'dạy': 200, 'làm': 180,
            'đi': 160, 'đến': 140, 'về': 120, 'ở': 100, 'tại': 90,
            'trong': 85, 'ngoài': 80, 'trên': 75, 'dưới': 70, 'bên': 65,
            'cạnh': 60, 'giữa': 55, 'trước': 50, 'sau': 45, 'người': 40,
            'nhà': 35, 'cửa': 30, 'bàn': 25, 'ghế': 20, 'sách': 15,
            'vở': 10, 'bút': 8, 'mực': 5, 'giấy': 3,
        }
    
    def is_correct_word(self, word: str) -> bool:
        """Kiểm tra từ có đúng chính tả không"""
        return word.lower() in self.words
    
    def get_correction(self, word: str) -> str:
        """Lấy từ sửa lỗi"""
        return self.common_errors.get(word.lower(), word)
    
    def get_suggestions(self, word: str, max_suggestions: int = 5) -> List[str]:
        """Lấy danh sách gợi ý sửa lỗi"""
        suggestions = []
        
        # Kiểm tra trong common errors
        if word.lower() in self.common_errors:
            suggestions.append(self.common_errors[word.lower()])
        
        # Tìm từ tương tự trong từ điển
        for dict_word in self.words:
            if self._similarity(word.lower(), dict_word) > 0.7:
                suggestions.append(dict_word)
        
        # Sắp xếp theo tần suất sử dụng
        suggestions.sort(key=lambda x: self.word_frequency.get(x.lower(), 0), reverse=True)
        
        return suggestions[:max_suggestions]
    
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

# Tạo instance global
vietnamese_dict = VietnameseDictionary() 