from enum import Enum


class CountryCode(str, Enum):
    Korea = "KOR"  # 한국
    USA = "USA"  # 미국
    # HKG = "HKG" # 홍콩
    # China = "CHN"  # 중국
    # Japan = "JPN"  # 일본
    # VND = "VND" # 베트남


class CurrencyCode(str, Enum):
    USD = "USD"  # 미국달러
    HKD = "HKD"  # 홍콩달러
    CNY = "CNY"  # 중국위안화
    JPY = "JPY"  # 일본엔화
    VND = "VND"  # 베트남동
