from enum import Enum, IntEnum


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


class OverseasMarketCode(str, Enum):
    Nasdaq = "NASD"  # 나스닥
    NYSE = "NYSE"  # 뉴욕
    AMEX = "AMEX"  # 아멕스
    # NAS = "NAS"  # 나스닥 (실전 투자용 나스닥 Only)
    # SEHK = "SEHK"  # 홍콩
    # SHAA = "중국상해"
    # SZAA = "중국심천"
    # TKSE = "일본"
    # HASE = "베트남 하노이"
    # VNSE = "베트남 호치민"


class SellBuyType(IntEnum):
    ALL = 0
    SELL = 1
    BUY = 2
