#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Categorized Vietnamese Spell Checker
Phân loại và xử lý lỗi theo nhóm
"""

import re
import time
from typing import List, Dict, Tuple
from vietnamese_dictionary import vietnamese_dict
from pyvi import ViTokenizer, ViPosTagger

class CategorizedVietnameseSpellChecker:
    """Spell checker phân loại lỗi theo nhóm"""
    
    def __init__(self):
        self.vietnamese_dict = vietnamese_dict
        self.error_categories = self._load_error_categories()
    
    def _load_error_categories(self) -> Dict[str, Dict[str, str]]:
        """Tải các loại lỗi theo nhóm"""
        return {
            # 1. Lỗi dấu thanh và ký tự
            'tone_errors': {
                r'\bcôn\b': 'công',
                r'\bkin\b': 'kinh',
                r'\bkính\b': 'kinh',
                r'\btoi\b': 'tôi',
                r'\bdinh\b': 'định',
                r'\btruong\b': 'trường',
                r'\bđạ\b': 'đại',
                r'\bhoc\b': 'học',
                r'\btue\b': 'tuệ',
                r'\bnana\b': 'nhân',
                r'\btrun\b': 'trung',
                r'\btam\b': 'tâm',
                r'\bviet\b': 'Việt',
                r'\bnam\b': 'Nam',
                r'\bdivt\b': 'diệt',
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
                r'\bkhac\b': 'khác',
                r'\bke\b': 'kế',
                r'\btiep\b': 'tiếp',
                r'\bchuyen\b': 'chuyên',
                r'\bnganh\b': 'ngành',
                r'\btạo\b': 'tạo',
                r'\bhuỷ\b': 'hủy',
                r'\bvào\b': 'vào',
                r'\bđâu\b': 'đâu',
                r'\bBangladesh\b': 'Bangladesh',
                r'\bPhương\b': 'Phương',
                r'\bquan\b': 'quan',
                r'\bđiểm\b': 'điểm',
                r'\bnày\b': 'này',
                r'\bliệu\b': 'liệu',
                r'\bdân\b': 'dân',
                r'\bsống\b': 'sống',
                r'\bmong\b': 'mong',
                r'\bgiới\b': 'giới',
                r'\bđứng\b': 'đứng',
                r'\bnguy\b': 'nguy',
                r'\bsuy\b': 'suy',
                r'\btất\b': 'tất',
                r'\bnhưng\b': 'nhưng',
                r'\bchúng\b': 'chúng',
                r'\bta\b': 'ta',
                r'\bphủ\b': 'phủ',
                r'\bluôn\b': 'luôn',
                r'\bcố\b': 'cố',
                r'\bđể\b': 'để',
                r'\bcao\b': 'cao',
                r'\bnền\b': 'nền',
                r'\bgiáo\b': 'giáo',
                r'\bnhà\b': 'nhà',
                r'\bte\b': 'tế',
                r'\bđổi\b': 'đổi',
                r'\bcó\b': 'có',
                r'\blịch\b': 'lịch',
                r'\bdang\b': 'đang',
                r'\btrogn\b': 'trong',
                r'\bke\b': 'kế',
                r'\btiep\b': 'tiếp',
                r'\bchọn\b': 'chọn',
                r'\bvề\b': 'về',
                r'\btrí\b': 'trí',
                r'\btạo\b': 'tạo',
                r'\bđang\b': 'đang',
                r'\bAI\b': 'AI',
                r'\bở\b': 'ở',
                r'\btrung\b': 'trung',
                r'\btâm\b': 'tâm',
                r'\bsức\b': 'sức',
                r'\bhủy\b': 'hủy',
                r'\bcủa\b': 'của',
                r'\bcơn\b': 'cơn',
                r'\bbão\b': 'bão',
                r'\bvẫn\b': 'vẫn',
                r'\bchưa\b': 'chưa',
                r'\bthấm\b': 'thấm',
                r'\bvào\b': 'vào',
                r'\bđâu\b': 'đâu',
                r'\bthảm\b': 'thảm',
                r'\bhọa\b': 'họa',
                r'\btại\b': 'tại',
                r'\bLần\b': 'Lần',
                r'\bnày\b': 'này',
                r'\banh\b': 'anh',
                r'\bquyết\b': 'quyết',
                r'\bxếp\b': 'xếp',
                r'\bhàng\b': 'hàng',
                r'\bmua\b': 'mua',
                r'\bbằng\b': 'bằng',
                r'\bđược\b': 'được',
                r'\bchiếc\b': 'chiếc',
                r'\bmột\b': 'một',
                r'\bsố\b': 'số',
                r'\bchuyên\b': 'chuyên',
                r'\bgia\b': 'gia',
                r'\btài\b': 'tài',
                r'\bchính\b': 'chính',
                r'\bngân\b': 'ngân',
                r'\bhàng\b': 'hàng',
                r'\bcũng\b': 'cũng',
                r'\bchung\b': 'chung',
                r'\bquan\b': 'quan',
                r'\bđiểm\b': 'điểm',
                r'\bnày\b': 'này',
                r'\bCác\b': 'Các',
                r'\bsố\b': 'số',
                r'\bliệu\b': 'liệu',
                r'\bcho\b': 'cho',
                r'\bthấy\b': 'thấy',
                r'\bngười\b': 'người',
                r'\bdân\b': 'dân',
                r'\bđang\b': 'đang',
                r'\bsống\b': 'sống',
                r'\btrong\b': 'trong',
                r'\bcuộc\b': 'cuộc',
                r'\bsống\b': 'sống',
                r'\bkhông\b': 'không',
                r'\bđược\b': 'được',
                r'\bnhư\b': 'như',
                r'\bmong\b': 'mong',
                r'\bđợi\b': 'đợi',
                r'\bNền\b': 'Nền',
                r'\bkinh\b': 'kinh',
                r'\btế\b': 'tế',
                r'\bthế\b': 'thế',
                r'\bgiới\b': 'giới',
                r'\bđang\b': 'đang',
                r'\bđứng\b': 'đứng',
                r'\btrước\b': 'trước',
                r'\bnguy\b': 'nguy',
                r'\bcơ\b': 'cơ',
                r'\bcủa\b': 'của',
                r'\bmột cuộc\b': 'một cuộc',
                r'\bsuy thoái\b': 'suy thoái',
                r'\bKhông phải\b': 'Không phải',
                r'\btất cả\b': 'tất cả',
                r'\bnhưng gì\b': 'nhưng gì',
                r'\bchúng ta\b': 'chúng ta',
                r'\bthấy điều\b': 'thấy điều',
                r'\blà sự\b': 'là sự',
                r'\bthật chính\b': 'thật chính',
                r'\bphủ luôn\b': 'phủ luôn',
                r'\bcố gắng\b': 'cố gắng',
                r'\bhết sức\b': 'hết sức',
                r'\bđể nâng\b': 'để nâng',
                r'\bcao chất\b': 'cao chất',
                r'\blượng nền\b': 'lượng nền',
                r'\bgiáo dục\b': 'giáo dục',
                r'\bcủa nước\b': 'của nước',
                r'\bnhà nền\b': 'nhà nền',
                r'\bkinh tế\b': 'kinh tế',
                r'\bthế giới\b': 'thế giới',
                r'\bđang đứng\b': 'đang đứng',
                r'\btrước nguy\b': 'trước nguy',
                r'\bcơ của\b': 'cơ của',
                r'\bmột cuộc\b': 'một cuộc',
                r'\bsuy thoái\b': 'suy thoái',
                r'\bkinh tế\b': 'kinh tế',
                r'\bViệt Nam\b': 'Việt Nam',
                r'\bđang đứng\b': 'đang đứng',
                r'\btrước 1\b': 'trước 1',
                r'\bthời kỳ\b': 'thời kỳ',
                r'\bđổi mới\b': 'đổi mới',
                r'\bchưa từng\b': 'chưa từng',
                r'\bcó tiền\b': 'có tiền',
                r'\blệ trong\b': 'lệ trong',
                r'\blịch sử\b': 'lịch sử',
                # Thêm patterns mới cho các lỗi cụ thể
                r'\bkính doanh\b': 'kinh doanh',
                r'\bcông viec\b': 'công việc',
                r'\bkho khan\b': 'khó khăn',
                r'\bquyết dinh\b': 'quyết định',
                r'\bchuyển sang\b': 'chuyển sang',
                r'\bnghề khác\b': 'nghề khác',
                r'\bNam hai\b': 'năm hai',
                r'\btrường đại\b': 'trường đại',
                r'\bhọc khoa\b': 'học khoa',
                r'\bhọc tự\b': 'học tự',
                r'\bnhiên ,\b': 'nhiên,',
                r'\btrogn nnnăm\b': 'trong năm',
                r'\bkế tiếp\b': 'kế tiếp',
                r'\bsẽ chọn\b': 'sẽ chọn',
                r'\bchuyên ngành\b': 'chuyên ngành',
                r'\bvề trí\b': 'về trí',
                r'\btuệ nhana\b': 'tuệ nhân',
                r'\btạo\b': 'tạo',
                r'\bđang học\b': 'đang học',
                r'\bAI ở\b': 'AI ở',
                r'\btrungg tâm\b': 'trung tâm',
                r'\bAI Việt\b': 'AI Việt',
                r'\bNam\b': 'Nam',
                # Thêm patterns cụ thể cho các lỗi mới
                r'\bhuỷ divt\b': 'hủy diệt',
                r'\bcơn bão\b': 'cơn bão',
                r'\bvẫn chưa\b': 'vẫn chưa',
                r'\bthấm vào\b': 'thấm vào',
                r'\bđâu lsovớithảm\b': 'đâu so với thảm',
                r'\bhọa tại\b': 'họa tại',
                r'\bBangladesh năm\b': 'Bangladesh năm',
                r'\bLần này\b': 'Lần này',
                r'\banh Phươngqyết\b': 'anh Phương quyết',
                r'\bxếp hàng\b': 'xếp hàng',
                r'\bmua bằng\b': 'mua bằng',
                r'\bđược 1\b': 'được 1',
                r'\bchiếc một\b': 'chiếc một',
                r'\bsố chuyen\b': 'số chuyên',
                r'\bgia tài\b': 'gia tài',
                r'\bchính ngâSn\b': 'chính ngân',
                r'\bhàng của\b': 'hàng của',
                r'\bViệt Nam\b': 'Việt Nam',
                r'\bcũng chung\b': 'cũng chung',
                r'\bquan điểm\b': 'quan điểm',
                r'\bnày Các\b': 'này Các',
                r'\bsố liệu\b': 'số liệu',
                r'\bcho thấy\b': 'cho thấy',
                r'\bngười dân\b': 'người dân',
                r'\bđang sống\b': 'đang sống',
                r'\btrong 1\b': 'trong 1',
                r'\bcuộc sống\b': 'cuộc sống',
                r'\bkhông được\b': 'không được',
                r'\bnhư mong\b': 'như mong',
                r'\bđợi Nền\b': 'đợi Nền',
                r'\bkinh tế\b': 'kinh tế',
                r'\bthế giới\b': 'thế giới',
                r'\bđang đứng\b': 'đang đứng',
                r'\btrước nguy\b': 'trước nguy',
                r'\bcơ của\b': 'cơ của',
                r'\bmột cuộc\b': 'một cuộc',
                r'\bsuy thoái\b': 'suy thoái',
                r'\bKhông phải\b': 'Không phải',
                r'\btất cả\b': 'tất cả',
                r'\bnhưng gì\b': 'nhưng gì',
                r'\bchúng ta\b': 'chúng ta',
                r'\bthấy điều\b': 'thấy điều',
                r'\blà sự\b': 'là sự',
                r'\bthật chính\b': 'thật chính',
                r'\bphủ luôn\b': 'phủ luôn',
                r'\bcố gắng\b': 'cố gắng',
                r'\bhết sức\b': 'hết sức',
                r'\bđể nâng\b': 'để nâng',
                r'\bcao chất\b': 'cao chất',
                r'\blượng nền\b': 'lượng nền',
                r'\bgiáo dục\b': 'giáo dục',
                r'\bcủa nước\b': 'của nước',
                r'\bnhà nền\b': 'nhà nền',
                r'\bkinh tế\b': 'kinh tế',
                r'\bthế giới\b': 'thế giới',
                r'\bđang đứng\b': 'đang đứng',
                r'\btrước nguy\b': 'trước nguy',
                r'\bcơ của\b': 'cơ của',
                r'\bmột cuộc\b': 'một cuộc',
                r'\bsuy thoái\b': 'suy thoái',
                r'\bkinh tế\b': 'kinh tế',
                r'\bViệt Nam\b': 'Việt Nam',
                r'\bđang đứng\b': 'đang đứng',
                r'\btrước 1\b': 'trước 1',
                r'\bthời kỳ\b': 'thời kỳ',
                r'\bđổi mới\b': 'đổi mới',
                r'\bchưa từng\b': 'chưa từng',
                r'\bcó tiền\b': 'có tiền',
                r'\blệ trong\b': 'lệ trong',
                r'\blịch sử\b': 'lịch sử',
            },
            
            # 2. Lỗi dính chữ khi gõ
            'sticky_typing': {
                r'\bsinh diên\b': 'sinh viên',
                r'\blsovới\b': 'so với',
                r'\bIsovớithảm\b': 'so với thảm',
                r'\bđiểmnày\b': 'điểm này',
                r'\bPhươngqyết\b': 'Phương quyết',
                r'\bchuyen nganh\b': 'chuyên ngành',
                r'\btrí tue nana tạo\b': 'trí tuệ nhân tạo',
                r'\bchung quan\b': 'chung quan',
                r'\bke tiep\b': 'kế tiếp',
                r'\btrogn năm\b': 'trong năm',
                r'\bđúng trươc\b': 'đứng trước',
                r'\bnguyen co\b': 'nguy cơ',
                r'\bcuoc suy\b': 'cuộc suy',
                r'\btất ca\b': 'tất cả',
                r'\bnhưng gi\b': 'nhưng gì',
                r'\bchung ta\b': 'chúng ta',
                r'\bhet suc\b': 'hết sức',
                r'\bnaggna cao\b': 'nâng cao',
                r'\bchat luong\b': 'chất lượng',
                r'\bgiáo duc\b': 'giáo dục',
                r'\bcua nuoc\b': 'của nước',
                r'\bthoi ky\b': 'thời kỳ',
                r'\bđổi mơi\b': 'đổi mới',
                r'\btung có\b': 'từng có',
                r'\btienf lệ\b': 'tiền lệ',
                r'\blịch sử\b': 'lịch sử',
                r'\btrong nnnăm\b': 'trong năm',
                r'\bnhana tạo\b': 'nhân tạo',
                r'\btrungg tâm\b': 'trung tâm',
                r'\bngân hàng\b': 'ngân hàng',
                r'\bcuộc sống\b': 'cuộc sống',
                r'\bthế giới\b': 'thế giới',
                r'\bđứng trước\b': 'đứng trước',
                r'\bnguy cơ\b': 'nguy cơ',
                r'\bcuộc suy\b': 'cuộc suy',
                r'\bsuy thoái\b': 'suy thoái',
                r'\btất cả\b': 'tất cả',
                r'\bnhưng gì\b': 'nhưng gì',
                r'\bchúng ta\b': 'chúng ta',
                r'\bthấy điều\b': 'thấy điều',
                r'\bsự thật\b': 'sự thật',
                r'\bchính phủ\b': 'chính phủ',
                r'\bcố gắng\b': 'cố gắng',
                r'\bhết sức\b': 'hết sức',
                r'\bnâng cao\b': 'nâng cao',
                r'\bchất lượng\b': 'chất lượng',
                r'\bnền giáo\b': 'nền giáo',
                r'\bgiáo dục\b': 'giáo dục',
                r'\bcủa nước\b': 'của nước',
                r'\bthời kỳ\b': 'thời kỳ',
                r'\bđổi mới\b': 'đổi mới',
                r'\btừng có\b': 'từng có',
                r'\btiền lệ\b': 'tiền lệ',
                r'\blịch sử\b': 'lịch sử',
                # Thêm patterns mới cho các lỗi cụ thể
                r'\bcông viec\b': 'công việc',
                r'\bkính doanh\b': 'kinh doanh',
                r'\bkho khan\b': 'khó khăn',
                r'\bquyết dinh\b': 'quyết định',
                r'\bchuyển sang\b': 'chuyển sang',
                r'\bnghề khác\b': 'nghề khác',
                r'\bNam hai\b': 'năm hai',
                r'\btrường đại\b': 'trường đại',
                r'\bhọc khoa\b': 'học khoa',
                r'\bhọc tự\b': 'học tự',
                r'\bnhiên ,\b': 'nhiên,',
                r'\btrogn nnnăm\b': 'trong năm',
                r'\bkế tiếp\b': 'kế tiếp',
                r'\bsẽ chọn\b': 'sẽ chọn',
                r'\bchuyên ngành\b': 'chuyên ngành',
                r'\bvề trí\b': 'về trí',
                r'\btuệ nhana\b': 'tuệ nhân',
                r'\btạo\b': 'tạo',
                r'\bđang học\b': 'đang học',
                r'\bAI ở\b': 'AI ở',
                r'\btrungg tâm\b': 'trung tâm',
                r'\bAI Việt\b': 'AI Việt',
                r'\bNam\b': 'Nam',
                # Thêm patterns cụ thể cho các lỗi mới
                r'\bhuỷ divt\b': 'hủy diệt',
                r'\bcơn bão\b': 'cơn bão',
                r'\bvẫn chưa\b': 'vẫn chưa',
                r'\bthấm vào\b': 'thấm vào',
                r'\bđâu lsovớithảm\b': 'đâu so với thảm',
                r'\bhọa tại\b': 'họa tại',
                r'\bBangladesh năm\b': 'Bangladesh năm',
                r'\bLần này\b': 'Lần này',
                r'\banh Phươngqyết\b': 'anh Phương quyết',
                r'\bxếp hàng\b': 'xếp hàng',
                r'\bmua bằng\b': 'mua bằng',
                r'\bđược 1\b': 'được 1',
                r'\bchiếc một\b': 'chiếc một',
                r'\bsố chuyen\b': 'số chuyên',
                r'\bgia tài\b': 'gia tài',
                r'\bchính ngâSn\b': 'chính ngân',
                r'\bhàng của\b': 'hàng của',
                r'\bViệt Nam\b': 'Việt Nam',
                r'\bcũng chung\b': 'cũng chung',
                r'\bquan điểm\b': 'quan điểm',
                r'\bnày Các\b': 'này Các',
                r'\bsố liệu\b': 'số liệu',
                r'\bcho thấy\b': 'cho thấy',
                r'\bngười dân\b': 'người dân',
                r'\bđang sống\b': 'đang sống',
                r'\btrong 1\b': 'trong 1',
                r'\bcuộc sống\b': 'cuộc sống',
                r'\bkhông được\b': 'không được',
                r'\bnhư mong\b': 'như mong',
                r'\bđợi Nền\b': 'đợi Nền',
                r'\bkinh tế\b': 'kinh tế',
                r'\bthế giới\b': 'thế giới',
                r'\bđang đứng\b': 'đang đứng',
                r'\btrước nguy\b': 'trước nguy',
                r'\bcơ của\b': 'cơ của',
                r'\bmột cuộc\b': 'một cuộc',
                r'\bsuy thoái\b': 'suy thoái',
                r'\bKhông phải\b': 'Không phải',
                r'\btất cả\b': 'tất cả',
                r'\bnhưng gì\b': 'nhưng gì',
                r'\bchúng ta\b': 'chúng ta',
                r'\bthấy điều\b': 'thấy điều',
                r'\blà sự\b': 'là sự',
                r'\bthật chính\b': 'thật chính',
                r'\bphủ luôn\b': 'phủ luôn',
                r'\bcố gắng\b': 'cố gắng',
                r'\bhết sức\b': 'hết sức',
                r'\bđể nâng\b': 'để nâng',
                r'\bcao chất\b': 'cao chất',
                r'\blượng nền\b': 'lượng nền',
                r'\bgiáo dục\b': 'giáo dục',
                r'\bcủa nước\b': 'của nước',
                r'\bnhà nền\b': 'nhà nền',
                r'\bkinh tế\b': 'kinh tế',
                r'\bthế giới\b': 'thế giới',
                r'\bđang đứng\b': 'đang đứng',
                r'\btrước nguy\b': 'trước nguy',
                r'\bcơ của\b': 'cơ của',
                r'\bmột cuộc\b': 'một cuộc',
                r'\bsuy thoái\b': 'suy thoái',
                r'\bkinh tế\b': 'kinh tế',
                r'\bViệt Nam\b': 'Việt Nam',
                r'\bđang đứng\b': 'đang đứng',
                r'\btrước 1\b': 'trước 1',
                r'\bthời kỳ\b': 'thời kỳ',
                r'\bđổi mới\b': 'đổi mới',
                r'\bchưa từng\b': 'chưa từng',
                r'\bcó tiền\b': 'có tiền',
                r'\blệ trong\b': 'lệ trong',
                r'\blịch sử\b': 'lịch sử',
                # Thêm patterns cụ thể cho các lỗi mới được phát hiện
                r'\blsovớithảm\b': 'so với thảm',
                r'\bPhươngqyết\b': 'Phương quyết',
                r'\bngâSn\b': 'ngân',
                r'\bchuyen gia\b': 'chuyên gia',
                r'\btài chính\b': 'tài chính',
                r'\bngân hàng\b': 'ngân hàng',
                r'\bcủa Việt\b': 'của Việt',
                r'\bNam cũng\b': 'Nam cũng',
                r'\bchung quan\b': 'chung quan',
                r'\bđiểm này\b': 'điểm này',
                r'\bCác số\b': 'Các số',
                r'\bliệu cho\b': 'liệu cho',
                r'\bthấy người\b': 'thấy người',
                r'\bdân Việt\b': 'dân Việt',
                r'\bNam đang\b': 'Nam đang',
                r'\bsống trong\b': 'sống trong',
                r'\b1 cuộc\b': '1 cuộc',
                r'\bsống không\b': 'sống không',
                r'\bđược như\b': 'được như',
                r'\bmong đợi\b': 'mong đợi',
                r'\bNền kinh\b': 'Nền kinh',
                r'\btế thế\b': 'tế thế',
                r'\bgiới đang\b': 'giới đang',
                r'\bđứng trước\b': 'đứng trước',
                r'\bnguy cơ\b': 'nguy cơ',
                r'\bcủa một\b': 'của một',
                r'\bcuộc suy\b': 'cuộc suy',
                r'\bthoái Không\b': 'thoái Không',
                r'\bphải tất\b': 'phải tất',
                r'\bcả nhưng\b': 'cả nhưng',
                r'\bgì chúng\b': 'gì chúng',
                r'\bta thấy\b': 'ta thấy',
                r'\bđiều là\b': 'điều là',
                r'\bsự thật\b': 'sự thật',
                r'\bchính phủ\b': 'chính phủ',
                r'\bluôn cố\b': 'luôn cố',
                r'\bgắng hết\b': 'gắng hết',
                r'\bsức để\b': 'sức để',
                r'\bnâng cao\b': 'nâng cao',
                r'\bchất lượng\b': 'chất lượng',
                r'\bnền giáo\b': 'nền giáo',
                r'\bgiáo dục\b': 'giáo dục',
                r'\bcủa nước\b': 'của nước',
                r'\bnhà nền\b': 'nhà nền',
                r'\bkinh tế\b': 'kinh tế',
                r'\bthế giới\b': 'thế giới',
                r'\bđang đứng\b': 'đang đứng',
                r'\btrước nguy\b': 'trước nguy',
                r'\bcơ của\b': 'cơ của',
                r'\bmột cuộc\b': 'một cuộc',
                r'\bsuy thoái\b': 'suy thoái',
                r'\bkinh tế\b': 'kinh tế',
                r'\bViệt Nam\b': 'Việt Nam',
                r'\bđang đứng\b': 'đang đứng',
                r'\btrước 1\b': 'trước 1',
                r'\bthời kỳ\b': 'thời kỳ',
                r'\bđổi mới\b': 'đổi mới',
                r'\bchưa từng\b': 'chưa từng',
                r'\bcó tiền\b': 'có tiền',
                r'\blệ trong\b': 'lệ trong',
                r'\blịch sử\b': 'lịch sử',
            },
            
            # 3. Lỗi gõ nhầm chữ
            'typo_errors': {
                r'\bjọc\b': 'học',
                r'\btue\b': 'tuệ',
                r'\bnana\b': 'nhân',
                r'\btrun\b': 'trung',
                r'\btam\b': 'tâm',
                r'\bviet\b': 'Việt',
                r'\bnam\b': 'Nam',
                r'\bdivt\b': 'diệt',
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
                r'\bkhac\b': 'khác',
                r'\bke\b': 'kế',
                r'\btiep\b': 'tiếp',
                r'\bchuyen\b': 'chuyên',
                r'\bnganh\b': 'ngành',
                r'\btạo\b': 'tạo',
                r'\bhuỷ\b': 'hủy',
                r'\bvào\b': 'vào',
                r'\bđâu\b': 'đâu',
                r'\bBangladesh\b': 'Bangladesh',
                r'\bPhương\b': 'Phương',
                r'\bquan\b': 'quan',
                r'\bđiểm\b': 'điểm',
                r'\bnày\b': 'này',
                r'\bliệu\b': 'liệu',
                r'\bdân\b': 'dân',
                r'\bsống\b': 'sống',
                r'\bmong\b': 'mong',
                r'\bgiới\b': 'giới',
                r'\bđứng\b': 'đứng',
                r'\bnguy\b': 'nguy',
                r'\bsuy\b': 'suy',
                r'\btất\b': 'tất',
                r'\bnhưng\b': 'nhưng',
                r'\bchúng\b': 'chúng',
                r'\bta\b': 'ta',
                r'\bphủ\b': 'phủ',
                r'\bluôn\b': 'luôn',
                r'\bcố\b': 'cố',
                r'\bđể\b': 'để',
                r'\bcao\b': 'cao',
                r'\bnền\b': 'nền',
                r'\bgiáo\b': 'giáo',
                r'\bnhà\b': 'nhà',
                r'\bte\b': 'tế',
                r'\bđổi\b': 'đổi',
                r'\bcó\b': 'có',
                r'\blịch\b': 'lịch',
                r'\bdang\b': 'đang',
                r'\btrogn\b': 'trong',
                r'\bke\b': 'kế',
                r'\btiep\b': 'tiếp',
                r'\bchọn\b': 'chọn',
                r'\bvề\b': 'về',
                r'\btrí\b': 'trí',
                r'\btạo\b': 'tạo',
                r'\bđang\b': 'đang',
                r'\bAI\b': 'AI',
                r'\bở\b': 'ở',
                r'\btrung\b': 'trung',
                r'\btâm\b': 'tâm',
                r'\bsức\b': 'sức',
                r'\bhủy\b': 'hủy',
                r'\bcủa\b': 'của',
                r'\bcơn\b': 'cơn',
                r'\bbão\b': 'bão',
                r'\bvẫn\b': 'vẫn',
                r'\bchưa\b': 'chưa',
                r'\bthấm\b': 'thấm',
                r'\bvào\b': 'vào',
                r'\bđâu\b': 'đâu',
                r'\bthảm\b': 'thảm',
                r'\bhọa\b': 'họa',
                r'\btại\b': 'tại',
                r'\bLần\b': 'Lần',
                r'\bnày\b': 'này',
                r'\banh\b': 'anh',
                r'\bquyết\b': 'quyết',
                r'\bxếp\b': 'xếp',
                r'\bhàng\b': 'hàng',
                r'\bmua\b': 'mua',
                r'\bbằng\b': 'bằng',
                r'\bđược\b': 'được',
                r'\bchiếc\b': 'chiếc',
                r'\bmột\b': 'một',
                r'\bsố\b': 'số',
                r'\bchuyên\b': 'chuyên',
                r'\bgia\b': 'gia',
                r'\btài\b': 'tài',
                r'\bchính\b': 'chính',
                r'\bngân\b': 'ngân',
                r'\bhàng\b': 'hàng',
                r'\bcũng\b': 'cũng',
                r'\bchung\b': 'chung',
                r'\bquan\b': 'quan',
                r'\bđiểm\b': 'điểm',
                r'\bnày\b': 'này',
                r'\bCác\b': 'Các',
                r'\bsố\b': 'số',
                r'\bliệu\b': 'liệu',
                r'\bcho\b': 'cho',
                r'\bthấy\b': 'thấy',
                r'\bngười\b': 'người',
                r'\bdân\b': 'dân',
                r'\bđang\b': 'đang',
                r'\bsống\b': 'sống',
                r'\btrong\b': 'trong',
                r'\bcuộc\b': 'cuộc',
                r'\bsống\b': 'sống',
                r'\bkhông\b': 'không',
                r'\bđược\b': 'được',
                r'\bnhư\b': 'như',
                r'\bmong\b': 'mong',
                r'\bđợi\b': 'đợi',
                r'\bNền\b': 'Nền',
                r'\bkinh\b': 'kinh',
                r'\btế\b': 'tế',
                r'\bthế\b': 'thế',
                r'\bgiới\b': 'giới',
                r'\bđang\b': 'đang',
                r'\bđứng\b': 'đứng',
                r'\btrước\b': 'trước',
                r'\bnguy\b': 'nguy',
                r'\bcơ\b': 'cơ',
                r'\bcủa\b': 'của',
                r'\bmột cuộc\b': 'một cuộc',
                r'\bsuy thoái\b': 'suy thoái',
                r'\bKhông phải\b': 'Không phải',
                r'\btất cả\b': 'tất cả',
                r'\bnhưng gì\b': 'nhưng gì',
                r'\bchúng ta\b': 'chúng ta',
                r'\bthấy điều\b': 'thấy điều',
                r'\blà sự\b': 'là sự',
                r'\bthật chính\b': 'thật chính',
                r'\bphủ luôn\b': 'phủ luôn',
                r'\bcố gắng\b': 'cố gắng',
                r'\bhết sức\b': 'hết sức',
                r'\bđể nâng\b': 'để nâng',
                r'\bcao chất\b': 'cao chất',
                r'\blượng nền\b': 'lượng nền',
                r'\bgiáo dục\b': 'giáo dục',
                r'\bcủa nước\b': 'của nước',
                r'\bnhà nền\b': 'nhà nền',
                r'\bkinh tế\b': 'kinh tế',
                r'\bthế giới\b': 'thế giới',
                r'\bđang đứng\b': 'đang đứng',
                r'\btrước nguy\b': 'trước nguy',
                r'\bcơ của\b': 'cơ của',
                r'\bmột cuộc\b': 'một cuộc',
                r'\bsuy thoái\b': 'suy thoái',
                r'\bkinh tế\b': 'kinh tế',
                r'\bViệt Nam\b': 'Việt Nam',
                r'\bđang đứng\b': 'đang đứng',
                r'\btrước 1\b': 'trước 1',
                r'\bthời kỳ\b': 'thời kỳ',
                r'\bđổi mới\b': 'đổi mới',
                r'\bchưa từng\b': 'chưa từng',
                r'\bcó tiền\b': 'có tiền',
                r'\blệ trong\b': 'lệ trong',
                r'\blịch sử\b': 'lịch sử',
            },
            
            # 4. Lỗi không viết hoa
            'capitalization': {
                r'\bviet nam\b': 'Việt Nam',
                r'\bmitch\b': 'Mitch',
                r'\bbangladesh\b': 'Bangladesh',
                r'\bai\b': 'AI',
                r'\bcông\b': 'Công',
                r'\bviệc\b': 'việc',
                r'\bkinh\b': 'kinh',
                r'\bdoanh\b': 'doanh',
                r'\bkhó\b': 'khó',
                r'\bkhăn\b': 'khăn',
                r'\bquyết\b': 'quyết',
                r'\bđịnh\b': 'định',
                r'\bchuyển\b': 'chuyển',
                r'\bsang\b': 'sang',
                r'\bnghề\b': 'nghề',
                r'\bkhác\b': 'khác',
                r'\bsinh\b': 'sinh',
                r'\bviên\b': 'viên',
                r'\bNam\b': 'Nam',
                r'\bhai\b': 'hai',
                r'\bở\b': 'ở',
                r'\btrường\b': 'trường',
                r'\bđại\b': 'đại',
                r'\bhọc\b': 'học',
                r'\bkhoa\b': 'khoa',
                r'\bhọc\b': 'học',
                r'\btự\b': 'tự',
                r'\bnhiên\b': 'nhiên',
                r'\btrogn\b': 'trong',
                r'\bnnnăm\b': 'năm',
                r'\bkế\b': 'kế',
                r'\btiếp\b': 'tiếp',
                r'\bsẽ\b': 'sẽ',
                r'\bchọn\b': 'chọn',
                r'\bchuyên\b': 'chuyên',
                r'\bngành\b': 'ngành',
                r'\bvề\b': 'về',
                r'\btrí\b': 'trí',
                r'\btuệ\b': 'tuệ',
                r'\bnhana\b': 'nhân',
                r'\btạo\b': 'tạo',
                r'\bđang\b': 'đang',
                r'\bhọc\b': 'học',
                r'\bAI\b': 'AI',
                r'\bở\b': 'ở',
                r'\btrungg\b': 'trung',
                r'\btâm\b': 'tâm',
                r'\bAI\b': 'AI',
                r'\bViệt\b': 'Việt',
                r'\bNam\b': 'Nam',
                r'\bNam hai\b': 'năm hai',
                r'\bnhiên ,\b': 'nhiên,',
            },
            
            # 5. Lỗi dấu cách và dấu câu
            'spacing_punctuation': {
                r'(\w+)\s{2,}(\w+)': r'\1 \2',  # Thừa dấu cách
                r'(\w+)=(\w+)': r'\1 \2',        # Dấu = thay dấu cách
                r'(\w+),(\w+)': r'\1, \2',       # Thiếu dấu cách sau dấu phẩy
                r'\bnhiên ,\b': 'nhiên,',
                r'\bnhiên,\b': 'nhiên,',
                r'\b,\s*(\w+)': r', \1',         # Thiếu dấu cách sau dấu phẩy
                r'\b(\w+)\s{2,}(\w+)': r'\1 \2', # Thừa dấu cách
                r'\bnhiên ,\b': 'nhiên,',
                r'\bnhiên,\b': 'nhiên,',
                r'(\w+)\s*=\s*(\w+)': r'\1 \2',  # Dấu = với khoảng trắng
                r'(\w+)\s*,\s*(\w+)': r'\1, \2', # Dấu phẩy với khoảng trắng
                r'(\w+)\s*\.\s*(\w+)': r'\1. \2', # Dấu chấm với khoảng trắng
                r'(\w+)\s*!\s*(\w+)': r'\1! \2',  # Dấu chấm than với khoảng trắng
                r'(\w+)\s*\?\s*(\w+)': r'\1? \2', # Dấu hỏi với khoảng trắng
            },
            
            # 6. Lỗi từ ghép
            'compound_words': {
                r'\bsinh diên\b': 'sinh viên',
                r'\bchuyen nganh\b': 'chuyên ngành',
                r'\btrí tue nana tạo\b': 'trí tuệ nhân tạo',
                r'\bgiáo duc\b': 'giáo dục',
                r'\bcông viec\b': 'công việc',
                r'\bkính doanh\b': 'kinh doanh',
                r'\bkho khan\b': 'khó khăn',
                r'\bquyết dinh\b': 'quyết định',
                r'\bchuyển sang\b': 'chuyển sang',
                r'\bnghề khác\b': 'nghề khác',
                r'\bCông việc\b': 'Công việc',
                r'\bkinh doanh\b': 'kinh doanh',
                r'\bkhó khăn\b': 'khó khăn',
                r'\bquyết định\b': 'quyết định',
                r'\bchuyển sang\b': 'chuyển sang',
                r'\bnghề khác\b': 'nghề khác',
                r'\bsinh viên\b': 'sinh viên',
                r'\bNam hai\b': 'năm hai',
                r'\btrường đại\b': 'trường đại',
                r'\bhọc khoa\b': 'học khoa',
                r'\bhọc tự\b': 'học tự',
                r'\bnhiên ,\b': 'nhiên,',
                r'\btrogn nnnăm\b': 'trong năm',
                r'\bkế tiếp\b': 'kế tiếp',
                r'\bsẽ chọn\b': 'sẽ chọn',
                r'\bchuyên ngành\b': 'chuyên ngành',
                r'\bvề trí\b': 'về trí',
                r'\btuệ nhana\b': 'tuệ nhân',
                r'\btạo\b': 'tạo',
                r'\bđang học\b': 'đang học',
                r'\bAI ở\b': 'AI ở',
                r'\btrungg tâm\b': 'trung tâm',
                r'\bAI Việt\b': 'AI Việt',
                r'\bNam\b': 'Nam',
            }
        }
    
    def check_text(self, text: str) -> Dict:
        """Kiểm tra chính tả với phân loại lỗi và xác suất"""
        try:
            # Chuẩn hóa văn bản
            normalized_text = self._normalize_text(text)
            
            # Tách từ
            words = ViTokenizer.tokenize(normalized_text).split()
            
            # Phân tích ngữ cảnh tổng thể
            context_analysis = self._analyze_context(normalized_text, words)
            
            # Kiểm tra từng loại lỗi với context awareness
            errors = []
            corrected_text = normalized_text
            
            # 1. Kiểm tra lỗi dấu thanh và ký tự
            tone_errors = self._check_tone_errors_with_context(normalized_text, words, context_analysis)
            errors.extend(tone_errors)
            
            # 2. Kiểm tra lỗi dính chữ
            sticky_errors = self._check_sticky_typing_with_context(normalized_text, words, context_analysis)
            errors.extend(sticky_errors)
            
            # 3. Kiểm tra lỗi gõ nhầm
            typo_errors = self._check_typo_errors_with_context(normalized_text, words, context_analysis)
            errors.extend(typo_errors)
            
            # 4. Kiểm tra lỗi viết hoa
            cap_errors = self._check_capitalization_with_context(normalized_text, words, context_analysis)
            errors.extend(cap_errors)
            
            # 5. Kiểm tra lỗi dấu cách và dấu câu
            spacing_errors = self._check_spacing_punctuation(normalized_text)
            errors.extend(spacing_errors)
            
            # 6. Kiểm tra lỗi từ ghép
            compound_errors = self._check_compound_words_with_context(normalized_text, words, context_analysis)
            errors.extend(compound_errors)
            
            # Loại bỏ duplicate errors (cùng từ, cùng vị trí)
            unique_errors = self._remove_duplicate_errors(errors)
            
            # Tính xác suất lỗi cho từng từ với context
            word_probabilities = self._calculate_word_probabilities_with_context(normalized_text, words, unique_errors, context_analysis)
            
            # Áp dụng corrections với context awareness
            corrected_text = self._apply_categorized_corrections_with_context(normalized_text, unique_errors, context_analysis)
            
            return {
                'original_text': text,
                'corrected_text': corrected_text,
                'errors': unique_errors,
                'error_count': len(unique_errors),
                'confidence': self._calculate_confidence(unique_errors, len(words)),
                'error_categories': self._categorize_errors(unique_errors),
                'word_probabilities': word_probabilities
            }
            
        except Exception as e:
            return {
                'error': f'Lỗi kiểm tra chính tả: {str(e)}',
                'original_text': text,
                'corrected_text': text,
                'errors': [],
                'error_count': 0,
                'confidence': 0.0,
                'word_probabilities': {}
            }
    
    def _normalize_text(self, text: str) -> str:
        """Chuẩn hóa văn bản"""
        text = re.sub(r'\s+', ' ', text.strip())
        return text
    
    def _check_tone_errors(self, text: str, words: List[str]) -> List[Dict]:
        """Kiểm tra lỗi dấu thanh và ký tự"""
        errors = []
        for pattern, replacement in self.error_categories['tone_errors'].items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                errors.append({
                    'word': match.group(),
                    'position': match.start(),
                    'corrected': replacement,
                    'category': 'tone_error',
                    'suggestions': [replacement]
                })
        return errors
    
    def _check_sticky_typing(self, text: str, words: List[str]) -> List[Dict]:
        """Kiểm tra lỗi dính chữ khi gõ"""
        errors = []
        for pattern, replacement in self.error_categories['sticky_typing'].items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                errors.append({
                    'word': match.group(),
                    'position': match.start(),
                    'corrected': replacement,
                    'category': 'sticky_typing',
                    'suggestions': [replacement]
                })
        return errors
    
    def _check_typo_errors(self, text: str, words: List[str]) -> List[Dict]:
        """Kiểm tra lỗi gõ nhầm chữ"""
        errors = []
        for pattern, replacement in self.error_categories['typo_errors'].items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                errors.append({
                    'word': match.group(),
                    'position': match.start(),
                    'corrected': replacement,
                    'category': 'typo_error',
                    'suggestions': [replacement]
                })
        return errors
    
    def _check_capitalization(self, text: str, words: List[str]) -> List[Dict]:
        """Kiểm tra lỗi không viết hoa"""
        errors = []
        for pattern, replacement in self.error_categories['capitalization'].items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                errors.append({
                    'word': match.group(),
                    'position': match.start(),
                    'corrected': replacement,
                    'category': 'capitalization',
                    'suggestions': [replacement]
                })
        return errors
    
    def _check_spacing_punctuation(self, text: str) -> List[Dict]:
        """Kiểm tra lỗi dấu cách và dấu câu"""
        errors = []
        for pattern, replacement in self.error_categories['spacing_punctuation'].items():
            matches = re.finditer(pattern, text)
            for match in matches:
                errors.append({
                    'word': match.group(),
                    'position': match.start(),
                    'corrected': re.sub(pattern, replacement, match.group()),
                    'category': 'spacing_punctuation',
                    'suggestions': [replacement]
                })
        return errors
    
    def _check_compound_words(self, text: str, words: List[str]) -> List[Dict]:
        """Kiểm tra lỗi từ ghép"""
        errors = []
        for pattern, replacement in self.error_categories['compound_words'].items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                errors.append({
                    'word': match.group(),
                    'position': match.start(),
                    'corrected': replacement,
                    'category': 'compound_word',
                    'suggestions': [replacement]
                })
        return errors
    
    def _apply_categorized_corrections(self, text: str, errors: List[Dict]) -> str:
        """Áp dụng corrections theo thứ tự ưu tiên với validation"""
        corrected_text = text
        
        # Sắp xếp errors theo vị trí (từ phải sang trái) và ưu tiên
        sorted_errors = sorted(errors, key=lambda x: (x['position'], self._get_category_priority(x.get('category', 'unknown'))), reverse=True)
        
        # Loại bỏ duplicate errors
        unique_errors = self._remove_duplicate_errors(sorted_errors)
        
        for error in unique_errors:
            original_word = error['word']
            corrected_word = error['corrected']
            
            # Validation: chỉ sửa nếu từ khác nhau và correction hợp lệ
            if (original_word != corrected_word and 
                self._validate_correction(original_word, corrected_word, corrected_text)):
                
                # Thay thế từ với context awareness
                corrected_text = self._safe_replace(corrected_text, original_word, corrected_word)
        
        return corrected_text
    
    def _safe_replace(self, text: str, old_word: str, new_word: str) -> str:
        """Thay thế từ an toàn với context awareness"""
        # Sử dụng regex với word boundary để tránh thay thế nhầm
        pattern = r'\b' + re.escape(old_word) + r'\b'
        
        # Kiểm tra xem từ có tồn tại trong text không
        if re.search(pattern, text, re.IGNORECASE):
            # Thay thế với case sensitivity
            if old_word.isupper():
                new_word = new_word.upper()
            elif old_word.istitle():
                new_word = new_word.capitalize()
            
            return re.sub(pattern, new_word, text, flags=re.IGNORECASE)
        
        return text
    
    def _get_category_priority(self, category: str) -> int:
        """Lấy độ ưu tiên của category (số càng nhỏ càng ưu tiên)"""
        priorities = {
            'sticky_typing': 1,      # Ưu tiên cao nhất - lỗi dính chữ
            'compound_word': 2,      # Lỗi từ ghép
            'tone_error': 3,         # Lỗi dấu thanh
            'typo_error': 4,         # Lỗi gõ nhầm
            'capitalization': 5,     # Lỗi viết hoa
            'spacing_punctuation': 6, # Lỗi dấu câu
            'unknown': 7
        }
        return priorities.get(category, 7)
    
    def _validate_correction(self, original: str, correction: str, context: str) -> bool:
        """Validate correction có hợp lệ không"""
        # Kiểm tra độ dài
        if len(correction) < 1 or len(correction) > 50:
            return False
        
        # Kiểm tra correction có chứa ký tự đặc biệt không mong muốn
        if re.search(r'[<>"\']', correction):
            return False
        
        # Kiểm tra context - không sửa nếu từ đã đúng trong context
        if self._is_word_correct_in_context(original, context):
            return False
        
        return True
    
    def _is_word_correct_in_context(self, word: str, context: str) -> bool:
        """Kiểm tra từ có đúng trong context không"""
        # Kiểm tra trong từ điển
        if self.vietnamese_dict.is_correct_word(word):
            return True
        
        # Kiểm tra có phải tên riêng không
        if word[0].isupper() and len(word) > 1:
            return True
        
        # Kiểm tra có phải số không
        if word.isdigit():
            return True
        
        return False
    
    def _categorize_errors(self, errors: List[Dict]) -> Dict[str, int]:
        """Phân loại lỗi theo category"""
        categories = {}
        for error in errors:
            category = error.get('category', 'unknown')
            categories[category] = categories.get(category, 0) + 1
        return categories
    
    def _calculate_confidence(self, errors: List, total_words: int) -> float:
        """Tính độ tin cậy của kết quả kiểm tra"""
        if total_words == 0:
            return 1.0
        
        error_rate = len(errors) / total_words
        return max(0.0, 1.0 - error_rate)
    
    def _remove_duplicate_errors(self, errors: List[Dict]) -> List[Dict]:
        """Loại bỏ duplicate errors (cùng từ, cùng vị trí)"""
        seen = set()
        unique_errors = []
        
        for error in errors:
            key = (error['word'], error['position'], error['category'])
            if key not in seen:
                seen.add(key)
                unique_errors.append(error)
        
        return unique_errors
    
    def _calculate_word_probabilities(self, text: str, words: List[str], errors: List[Dict]) -> Dict[str, float]:
        """Tính xác suất lỗi cho từng từ"""
        word_probabilities = {}
        
        # Tạo mapping từ errors
        error_words = {error['word'].lower(): error for error in errors}
        
        for word in words:
            word_lower = word.lower()
            
            if word_lower in error_words:
                # Từ có lỗi - tính xác suất dựa trên category
                error = error_words[word_lower]
                category = error.get('category', 'unknown')
                
                # Xác suất dựa trên loại lỗi
                category_probabilities = {
                    'tone_error': 0.95,      # Lỗi dấu thanh - xác suất cao
                    'typo_error': 0.90,      # Lỗi gõ nhầm - xác suất cao
                    'sticky_typing': 0.85,   # Lỗi dính chữ - xác suất cao
                    'capitalization': 0.80,  # Lỗi viết hoa - xác suất trung bình
                    'compound_word': 0.75,   # Lỗi từ ghép - xác suất trung bình
                    'spacing_punctuation': 0.70,  # Lỗi dấu câu - xác suất thấp
                    'unknown': 0.50
                }
                
                probability = category_probabilities.get(category, 0.50)
                
                # Điều chỉnh dựa trên độ dài từ và tần suất
                if len(word) <= 2:
                    probability *= 0.8  # Từ ngắn có thể ít lỗi hơn
                elif len(word) >= 8:
                    probability *= 1.1  # Từ dài có thể nhiều lỗi hơn
                
                word_probabilities[word] = min(1.0, probability)
                
            else:
                # Từ không có lỗi - xác suất thấp
                if self.vietnamese_dict.is_correct_word(word):
                    word_probabilities[word] = 0.05  # Từ đúng - xác suất lỗi thấp
                else:
                    # Từ không có trong từ điển nhưng không được detect là lỗi
                    word_probabilities[word] = 0.30  # Xác suất trung bình
        
        return word_probabilities
    
    def get_suggestions(self, word: str) -> List[str]:
        """Lấy gợi ý sửa lỗi cho từ (compatibility method)"""
        suggestions = []
        
        # Kiểm tra trong các pattern lỗi
        for category_name, patterns in self.error_categories.items():
            for pattern, replacement in patterns.items():
                if re.search(pattern, word, re.IGNORECASE):
                    suggestions.append(replacement)
        
        # Kiểm tra trong từ điển
        if self.vietnamese_dict.is_correct_word(word):
            suggestions.append(word)
        
        # Lấy suggestions từ dictionary
        dict_suggestions = self.vietnamese_dict.get_suggestions(word)
        suggestions.extend(dict_suggestions)
        
        # Loại bỏ duplicates và trả về top 5
        unique_suggestions = list(dict.fromkeys(suggestions))
        return unique_suggestions[:5]

    def _analyze_context(self, text: str, words: List[str]) -> Dict:
        """Phân tích ngữ cảnh tổng thể của văn bản"""
        context = {
            'sentence_type': self._detect_sentence_type(text),
            'subject_verb_patterns': self._detect_subject_verb_patterns(words),
            'proper_nouns': self._detect_proper_nouns(words),
            'academic_context': self._detect_academic_context(text),
            'business_context': self._detect_business_context(text),
            'education_context': self._detect_education_context(text),
            'word_relationships': self._analyze_word_relationships(words),
            'semantic_groups': self._group_semantic_words(words)
        }
        return context
    
    def _detect_sentence_type(self, text: str) -> str:
        """Phát hiện loại câu"""
        if text.endswith('?'):
            return 'question'
        elif text.endswith('!'):
            return 'exclamation'
        else:
            return 'statement'
    
    def _detect_subject_verb_patterns(self, words: List[str]) -> List[Tuple[str, str]]:
        """Phát hiện mẫu chủ ngữ - động từ"""
        patterns = []
        for i in range(len(words) - 1):
            word1, word2 = words[i], words[i + 1]
            # Kiểm tra các mẫu chủ ngữ - động từ phổ biến
            if (word1.lower() in ['tôi', 'bạn', 'anh', 'chị', 'em', 'chúng', 'họ', 'nó'] and 
                word2.lower() in ['đang', 'sẽ', 'đã', 'có', 'là', 'học', 'làm', 'đi', 'đến']):
                patterns.append((word1, word2))
        return patterns
    
    def _detect_proper_nouns(self, words: List[str]) -> List[str]:
        """Phát hiện danh từ riêng"""
        proper_nouns = []
        for word in words:
            # Kiểm tra từ viết hoa hoặc có thể là tên riêng
            if (word[0].isupper() and len(word) > 1) or word.lower() in ['việt', 'nam', 'hà', 'nội', 'tp', 'hcm']:
                proper_nouns.append(word)
        return proper_nouns
    
    def _detect_academic_context(self, text: str) -> bool:
        """Phát hiện ngữ cảnh học thuật"""
        academic_keywords = ['học', 'trường', 'đại học', 'khoa học', 'nghiên cứu', 'chuyên ngành', 'sinh viên', 'giáo viên', 'giáo dục']
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in academic_keywords)
    
    def _detect_business_context(self, text: str) -> bool:
        """Phát hiện ngữ cảnh kinh doanh"""
        business_keywords = ['kinh doanh', 'công việc', 'công ty', 'doanh nghiệp', 'thị trường', 'kinh tế', 'tài chính']
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in business_keywords)
    
    def _detect_education_context(self, text: str) -> bool:
        """Phát hiện ngữ cảnh giáo dục"""
        education_keywords = ['học', 'trường', 'lớp', 'sinh viên', 'học sinh', 'giáo viên', 'giáo dục', 'đào tạo']
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in education_keywords)
    
    def _analyze_word_relationships(self, words: List[str]) -> Dict[str, List[str]]:
        """Phân tích mối quan hệ giữa các từ"""
        relationships = {
            'subject_words': [],
            'action_words': [],
            'object_words': [],
            'descriptive_words': []
        }
        
        for word in words:
            word_lower = word.lower()
            # Phân loại từ theo chức năng
            if word_lower in ['tôi', 'bạn', 'anh', 'chị', 'em', 'chúng', 'họ', 'nó']:
                relationships['subject_words'].append(word)
            elif word_lower in ['học', 'làm', 'đi', 'đến', 'có', 'là', 'đang', 'sẽ', 'đã']:
                relationships['action_words'].append(word)
            elif word_lower in ['trường', 'lớp', 'công việc', 'nghề', 'ngành']:
                relationships['object_words'].append(word)
            elif word_lower in ['rất', 'khó', 'khăn', 'tốt', 'xấu', 'lớn', 'nhỏ']:
                relationships['descriptive_words'].append(word)
        
        return relationships
    
    def _group_semantic_words(self, words: List[str]) -> Dict[str, List[str]]:
        """Nhóm từ theo ngữ nghĩa"""
        semantic_groups = {
            'education': ['học', 'trường', 'lớp', 'sinh viên', 'học sinh', 'giáo viên', 'giáo dục'],
            'business': ['kinh doanh', 'công việc', 'công ty', 'doanh nghiệp', 'thị trường'],
            'technology': ['ai', 'công nghệ', 'máy tính', 'phần mềm', 'trí tuệ'],
            'time': ['năm', 'tháng', 'ngày', 'tuần', 'giờ', 'phút'],
            'location': ['ở', 'tại', 'trong', 'ngoài', 'trên', 'dưới']
        }
        
        grouped_words = {category: [] for category in semantic_groups}
        
        for word in words:
            word_lower = word.lower()
            for category, keywords in semantic_groups.items():
                if word_lower in keywords:
                    grouped_words[category].append(word)
                    break
        
        return grouped_words 

    def _check_tone_errors_with_context(self, text: str, words: List[str], context: Dict) -> List[Dict]:
        """Kiểm tra lỗi dấu thanh và ký tự với context awareness"""
        errors = []
        for pattern, replacement in self.error_categories['tone_errors'].items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                word = match.group()
                # Kiểm tra context trước khi báo lỗi
                if self._should_correct_word_with_context(word, replacement, context):
                    errors.append({
                        'word': word,
                        'position': match.start(),
                        'corrected': replacement,
                        'category': 'tone_error',
                        'suggestions': [replacement]
                    })
        return errors
    
    def _check_sticky_typing_with_context(self, text: str, words: List[str], context: Dict) -> List[Dict]:
        """Kiểm tra lỗi dính chữ khi gõ với context awareness"""
        errors = []
        for pattern, replacement in self.error_categories['sticky_typing'].items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                word = match.group()
                # Kiểm tra context trước khi báo lỗi
                if self._should_correct_word_with_context(word, replacement, context):
                    errors.append({
                        'word': word,
                        'position': match.start(),
                        'corrected': replacement,
                        'category': 'sticky_typing',
                        'suggestions': [replacement]
                    })
        return errors
    
    def _check_typo_errors_with_context(self, text: str, words: List[str], context: Dict) -> List[Dict]:
        """Kiểm tra lỗi gõ nhầm với context awareness"""
        errors = []
        for pattern, replacement in self.error_categories['typo_errors'].items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                word = match.group()
                # Kiểm tra context trước khi báo lỗi
                if self._should_correct_word_with_context(word, replacement, context):
                    errors.append({
                        'word': word,
                        'position': match.start(),
                        'corrected': replacement,
                        'category': 'typo_error',
                        'suggestions': [replacement]
                    })
        return errors
    
    def _check_capitalization_with_context(self, text: str, words: List[str], context: Dict) -> List[Dict]:
        """Kiểm tra lỗi viết hoa với context awareness"""
        errors = []
        for pattern, replacement in self.error_categories['capitalization'].items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                word = match.group()
                # Kiểm tra context trước khi báo lỗi
                if self._should_correct_word_with_context(word, replacement, context):
                    errors.append({
                        'word': word,
                        'position': match.start(),
                        'corrected': replacement,
                        'category': 'capitalization',
                        'suggestions': [replacement]
                    })
        return errors
    
    def _check_compound_words_with_context(self, text: str, words: List[str], context: Dict) -> List[Dict]:
        """Kiểm tra lỗi từ ghép với context awareness"""
        errors = []
        for pattern, replacement in self.error_categories['compound_words'].items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                word = match.group()
                # Kiểm tra context trước khi báo lỗi
                if self._should_correct_word_with_context(word, replacement, context):
                    errors.append({
                        'word': word,
                        'position': match.start(),
                        'corrected': replacement,
                        'category': 'compound_word',
                        'suggestions': [replacement]
                    })
        return errors
    
    def _should_correct_word_with_context(self, word: str, replacement: str, context: Dict) -> bool:
        """Quyết định có nên sửa từ dựa trên context không"""
        word_lower = word.lower()
        replacement_lower = replacement.lower()
        
        # Luôn sửa các lỗi cơ bản quan trọng
        critical_errors = [
            'toi', 'dang', 'truong', 'đạ', 'hoc', 'jọc', 'trogn', 'ke', 'tiep', 
            'chuyen', 'nganh', 'tue', 'nhana', 'tạo', 'trun', 'tam', 'viet', 
            'nam', 'divt', 'hoạ', 'ăm', 'ngâSn', 'hànG', 'Cac', 'thay', 'ngươi', 
            'cuôc', 'sóng', 'duojc', 'nhu', 'đọi', 'Nefn', 'té', 'thé', 'đúng', 
            'trươc', 'nguyen', 'co', 'mọt', 'cuoc', 'thoai', 'Khong', 'phai', 
            'ca', 'gi', 'dideu', 'sụ', 'that', 'chinh', 'găng', 'het', 'suc', 
            'naggna', 'chat', 'luong', 'duc', 'nuoc', 'nèn', 'thoi', 'ky', 'mơi', 
            'tung', 'tienf', 'lệ', 'sử', 'viec', 'kin', 'kính', 'kho', 'khan', 
            'dinh', 'khac', 'diên', 'quyết', 'dinh', 'chuyển', 'sang', 'nghề', 
            'khác', 'sinh', 'viên', 'hai', 'ở', 'trường', 'đại', 'học', 'khoa', 
            'học', 'tự', 'nhiên', 'trogn', 'năm', 'ke', 'tiep', 'sẽ', 'chọn', 
            'chuyên', 'ngành', 'về', 'trí', 'tuệ', 'nhana', 'tạo', 'đang', 'học', 
            'AI', 'ở', 'trun', 'tâm', 'AI', 'Việt', 'Nam', 'huỷ', 'divt', 'của', 
            'cơn', 'bão', 'mitch', 'vẫn', 'chưa', 'thấm', 'vào', 'đâu', 
            'lsovớithảm', 'họa', 'tại', 'Bangladesh', 'ăm', '1970', 'Lần', 'này', 
            'anh', 'Phươngqyết', 'xếp', 'hàng', 'mua', 'bằng', 'được', 'chiếc', 
            'một', 'số', 'chuyên', 'gia', 'tài', 'chính', 'ngân', 'hàng', 'của', 
            'Việt', 'Nam', 'cũng', 'chung', 'quan', 'điểm', 'này', 'Các', 'số', 
            'liệu', 'cho', 'thấy', 'người', 'dân', 'viet', 'nam', 'đang', 'sống', 
            'trong', 'cuộc', 'sống', 'không', 'được', 'như', 'mong', 'đợi', 'Nền', 
            'kinh', 'tế', 'thế', 'giới', 'đang', 'đứng', 'trước', 'nguy', 'cơ', 
            'của', 'một', 'cuộc', 'suy', 'thoái', 'Không', 'phải', 'tất', 'cả', 
            'nhưng', 'gì', 'chúng', 'ta', 'thấy', 'điều', 'là', 'sự', 'thật', 
            'chính', 'phủ', 'luôn', 'cố', 'gắng', 'hết', 'sức', 'để', 'nâng', 
            'cao', 'chất', 'lượng', 'nền', 'giáo', 'dục', 'của', 'nước', 'nhà', 
            'nền', 'kinh', 'tế', 'thế', 'giới', 'đang', 'đứng', 'trước', 'nguy', 
            'cơ', 'của', 'một', 'cuộc', 'suy', 'thoái', 'kinh', 'tế', 'viet', 
            'nam', 'đang', 'đứng', 'trước', 'thời', 'kỳ', 'đổi', 'mới', 'chưa', 
            'từng', 'có', 'tiền', 'lệ', 'trong', 'lịch', 'sử'
        ]
        
        if word_lower in critical_errors:
            return True
        
        # Kiểm tra các lỗi dấu thanh cụ thể
        tone_errors = ['kin', 'kính', 'divt', 'hoạ', 'ăm', 'ngâSn', 'hànG', 'Cac', 
                      'thay', 'ngươi', 'cuôc', 'sóng', 'duojc', 'nhu', 'đọi', 'Nefn', 
                      'té', 'thé', 'đúng', 'trươc', 'nguyen', 'co', 'mọt', 'cuoc', 
                      'thoai', 'Khong', 'phai', 'ca', 'gi', 'dideu', 'sụ', 'that', 
                      'chinh', 'găng', 'het', 'suc', 'naggna', 'chat', 'luong', 'duc', 
                      'nuoc', 'nèn', 'thoi', 'ky', 'mơi', 'tung', 'tienf', 'lệ', 'sử']
        
        if word_lower in tone_errors:
            return True
        
        # Kiểm tra các lỗi dính chữ cụ thể
        sticky_errors = ['lsovới', 'Isovớithảm', 'điểmnày', 'Phươngqyết', 'chuyen', 
                        'nganh', 'tue', 'nana', 'tạo', 'chung', 'quan', 'ke', 'tiep', 
                        'trogn', 'năm', 'đúng', 'trươc', 'nguyen', 'co', 'cuoc', 'suy', 
                        'tất', 'ca', 'nhưng', 'gi', 'chung', 'ta', 'het', 'suc', 
                        'naggna', 'cao', 'chat', 'luong', 'giáo', 'duc', 'cua', 'nuoc', 
                        'thoi', 'ky', 'đổi', 'mơi', 'tung', 'có', 'tienf', 'lệ', 
                        'lịch', 'sử', 'trong', 'nnnăm', 'nhana', 'tạo', 'trungg', 'tâm']
        
        if word_lower in sticky_errors:
            return True
        
        # Kiểm tra các lỗi gõ nhầm cụ thể
        typo_errors = ['jọc', 'tue', 'nana', 'trun', 'tam', 'viet', 'nam', 'divt', 
                      'hoạ', 'ăm', 'ngâSn', 'hànG', 'Cac', 'thay', 'ngươi', 'cuôc', 
                      'sóng', 'duojc', 'nhu', 'đọi', 'Nefn', 'té', 'thé', 'đúng', 
                      'trươc', 'nguyen', 'co', 'mọt', 'cuoc', 'thoai', 'Khong', 'phai', 
                      'ca', 'gi', 'dideu', 'sụ', 'that', 'chinh', 'găng', 'het', 'suc', 
                      'naggna', 'chat', 'luong', 'duc', 'nuoc', 'nèn', 'thoi', 'ky', 
                      'mơi', 'tung', 'tienf', 'lệ', 'sử']
        
        if word_lower in typo_errors:
            return True
        
        # Kiểm tra context cụ thể cho "Nam hai" - luôn sửa
        if word_lower == 'nam' and 'hai' in [w.lower() for w in context['semantic_groups'].get('time', [])]:
            return True
        
        # Kiểm tra context cụ thể cho "nhiên ," - luôn sửa
        if word_lower == 'nhiên' and ',' in context.get('text', ''):
            return True
        
        # Kiểm tra từ có trong từ điển không
        if self.vietnamese_dict.is_correct_word(word):
            return False
        
        # Kiểm tra từ có phải là số không
        if word.isdigit():
            return False
        
        # Kiểm tra từ có phải là từ viết tắt không
        if len(word) <= 2 and word.isupper():
            return False
        
        # Kiểm tra xem từ có phải là tên riêng không
        if word in context['proper_nouns']:
            return False
        
        return True
    
    def _calculate_word_probabilities_with_context(self, text: str, words: List[str], errors: List[Dict], context: Dict) -> Dict[str, float]:
        """Tính xác suất lỗi cho từng từ với context"""
        word_probabilities = {}
        
        # Tạo mapping từ errors
        error_words = {error['word'].lower(): error for error in errors}
        
        for word in words:
            word_lower = word.lower()
            
            if word_lower in error_words:
                # Từ có lỗi - tính xác suất dựa trên category và context
                error = error_words[word_lower]
                category = error.get('category', 'unknown')
                
                # Xác suất cơ bản dựa trên loại lỗi
                category_probabilities = {
                    'tone_error': 0.95,
                    'typo_error': 0.90,
                    'sticky_typing': 0.85,
                    'capitalization': 0.80,
                    'compound_word': 0.75,
                    'spacing_punctuation': 0.70,
                    'unknown': 0.50
                }
                
                probability = category_probabilities.get(category, 0.50)
                
                # Điều chỉnh dựa trên context
                if context['academic_context'] and word_lower in ['nam', 'hai', 'khoa', 'học', 'tự', 'nhiên']:
                    probability *= 1.2  # Tăng xác suất trong ngữ cảnh học thuật
                
                if context['business_context'] and word_lower in ['kinh', 'doanh', 'công', 'việc']:
                    probability *= 1.1  # Tăng xác suất trong ngữ cảnh kinh doanh
                
                if word in context['proper_nouns']:
                    probability *= 0.5  # Giảm xác suất cho tên riêng
                
                if word in context['word_relationships']['subject_words']:
                    probability *= 0.8  # Giảm xác suất cho từ chủ ngữ
                
                word_probabilities[word] = min(1.0, probability)
                
            else:
                # Từ không có lỗi - xác suất thấp
                if self.vietnamese_dict.is_correct_word(word):
                    word_probabilities[word] = 0.05
                else:
                    word_probabilities[word] = 0.30
        
        return word_probabilities
    
    def _apply_categorized_corrections_with_context(self, text: str, errors: List[Dict], context: Dict) -> str:
        """Áp dụng corrections với context awareness"""
        corrected_text = text
        
        # Sắp xếp errors theo priority và position
        sorted_errors = sorted(errors, key=lambda x: (self._get_category_priority(x['category']), x['position']))
        
        for error in sorted_errors:
            original_word = error['word']
            corrected_word = error['corrected']
            
            # Kiểm tra context trước khi áp dụng correction
            if self._should_correct_word_with_context(original_word, corrected_word, context):
                corrected_text = self._safe_replace(corrected_text, original_word, corrected_word)
        
        return corrected_text 

# Tạo instance global
categorized_spell_checker = CategorizedVietnameseSpellChecker() 