# -*- coding: utf-8 -*-
"""
===================================
美股指数与股票代码工具
===================================

提供：
1. 美股指数代码映射（如 SPX -> ^GSPC）
2. 美股股票代码识别（AAPL、TSLA 等）

美股指数在 Yahoo Finance 中需使用 ^ 前缀，与股票代码不同。
"""

import re

# 美股代码正则：1-5 个大写字母，可选 .X 后缀（如 BRK.B）
_US_STOCK_PATTERN = re.compile(r'^[A-Z]{1,5}(\.[A-Z])?$')


# 用户输入 -> (Yahoo Finance 符号, 中文名称)
US_INDEX_MAPPING = {
    # 标普 500
    'SPX': ('^GSPC', '标普500指数'),
    '^GSPC': ('^GSPC', '标普500指数'),
    'GSPC': ('^GSPC', '标普500指数'),
    # 道琼斯工业平均指数
    'DJI': ('^DJI', '道琼斯工业指数'),
    '^DJI': ('^DJI', '道琼斯工业指数'),
    'DJIA': ('^DJI', '道琼斯工业指数'),
    # 纳斯达克综合指数
    'IXIC': ('^IXIC', '纳斯达克综合指数'),
    '^IXIC': ('^IXIC', '纳斯达克综合指数'),
    'NASDAQ': ('^IXIC', '纳斯达克综合指数'),
    # 纳斯达克 100
    'NDX': ('^NDX', '纳斯达克100指数'),
    '^NDX': ('^NDX', '纳斯达克100指数'),
    # VIX 波动率指数
    'VIX': ('^VIX', 'VIX恐慌指数'),
    '^VIX': ('^VIX', 'VIX恐慌指数'),
    # 罗素 2000
    'RUT': ('^RUT', '罗素2000指数'),
    '^RUT': ('^RUT', '罗素2000指数'),
}


def is_us_index_code(code: str) -> bool:
    """
    判断代码是否为美股指数符号。

    Args:
        code: 股票/指数代码，如 'SPX', 'DJI'

    Returns:
        True 表示是已知美股指数符号，否则 False

    Examples:
        >>> is_us_index_code('SPX')
        True
        >>> is_us_index_code('AAPL')
        False
    """
    return (code or '').strip().upper() in US_INDEX_MAPPING


def is_us_stock_code(code: str) -> bool:
    """
    判断代码是否为美股股票符号（排除美股指数）。

    美股股票代码为 1-5 个大写字母，可选 .X 后缀如 BRK.B。
    美股指数（SPX、DJI 等）明确排除。

    Args:
        code: 股票代码，如 'AAPL', 'TSLA', 'BRK.B'

    Returns:
        True 表示是美股股票符号，否则 False

    Examples:
        >>> is_us_stock_code('AAPL')
        True
        >>> is_us_stock_code('TSLA')
        True
        >>> is_us_stock_code('BRK.B')
        True
        >>> is_us_stock_code('SPX')
        False
        >>> is_us_stock_code('600519')
        False
    """
    normalized = (code or '').strip().upper()
    # 美股指数不是股票
    if normalized in US_INDEX_MAPPING:
        return False
    return bool(_US_STOCK_PATTERN.match(normalized))


def get_us_index_yf_symbol(code: str) -> tuple:
    """
    获取美股指数的 Yahoo Finance 符号与中文名称。

    Args:
        code: 用户输入，如 'SPX', '^GSPC', 'DJI'

    Returns:
        (yf_symbol, chinese_name) 元组，未找到时返回 (None, None)。

    Examples:
        >>> get_us_index_yf_symbol('SPX')
        ('^GSPC', '标普500指数')
        >>> get_us_index_yf_symbol('AAPL')
        (None, None)
    """
    normalized = (code or '').strip().upper()
    return US_INDEX_MAPPING.get(normalized, (None, None))


# ===================================
# 日股 (TSE) 支持
# ===================================

# 日股个股代码正则：
# - 4 位数字（如 7203）
# - 4 位数字 + .T（如 7203.T）
# - JP 前缀 + 4 位数字（如 JP7203）
_JP_STOCK_PATTERN = re.compile(r'^(JP\d{4}|\d{4}(\.T)?)$', re.IGNORECASE)

# 日股主要指数映射（用户输入 -> (Yahoo Finance 符号, 中文名称)）
JP_INDEX_MAPPING = {
    'N225':    ('^N225', '日经225指数'),
    '^N225':   ('^N225', '日经225指数'),
    'NIKKEI':  ('^N225', '日经225指数'),
    'TOPIX':   ('^TOPX', '东证指数'),
    '^TOPX':   ('^TOPX', '东证指数'),
}


def is_jp_stock_code(code: str) -> bool:
    """
    判断代码是否为日股个股。

    Args:
        code: 股票代码，如 'JP7203', '7203', '7203.T'

    Returns:
        True 表示是日股个股代码，否则 False

    Examples:
        >>> is_jp_stock_code('JP7203')
        True
        >>> is_jp_stock_code('AAPL')
        False
        >>> is_jp_stock_code('N225')
        False
    """
    return bool(_JP_STOCK_PATTERN.match((code or '').strip().upper()))


def get_jp_stock_yf_symbol(code: str) -> tuple:
    """
    获取日股个股的 Yahoo Finance 符号与名称占位（名称留空）。

    Args:
        code: 用户输入，如 '7203', '7203.T', 'JP7203'

    Returns:
        (yf_symbol, None) 元组，未匹配时返回 (None, None)。
    """
    normalized = (code or '').strip().upper()
    if normalized.startswith("JP") and len(normalized) == 6 and normalized[2:].isdigit():
        return f"{normalized[2:]}.T", None
    if normalized.endswith(".T") and normalized[:-2].isdigit() and len(normalized[:-2]) == 4:
        return normalized, None
    if normalized.isdigit() and len(normalized) == 4:
        return f"{normalized}.T", None
    return None, None


def is_jp_index_code(code: str) -> bool:
    """
    判断代码是否为日股指数符号。

    Args:
        code: 指数代码，如 'N225', 'TOPIX'

    Returns:
        True 表示是已知日股指数符号，否则 False
    """
    return (code or '').strip().upper() in JP_INDEX_MAPPING


def get_jp_index_yf_symbol(code: str) -> tuple:
    """
    获取日股指数的 Yahoo Finance 符号与中文名称。

    Args:
        code: 用户输入，如 'N225', 'TOPIX'

    Returns:
        (yf_symbol, chinese_name) 元组，未找到时返回 (None, None)。

    Examples:
        >>> get_jp_index_yf_symbol('N225')
        ('^N225', '日经225指数')
        >>> get_jp_index_yf_symbol('JP7203')
        (None, None)
    """
    return JP_INDEX_MAPPING.get((code or '').strip().upper(), (None, None))
