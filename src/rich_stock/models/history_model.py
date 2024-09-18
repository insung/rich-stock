from pydantic import BaseModel, Field

from ..models.enums import CurrencyCode, SellBuyType


class DailyHistoryDetailResponse(BaseModel):
    trade_day: str = Field(description="매매 일자")
    sell_buy_type: SellBuyType = Field(description="매매 구분")
    ticker: str = Field(description="종목코드")
    ticker_name: str = Field(description="종목명")
    trade_quantity: int = Field(description="체결 수량")
    trade_quantity_decimal: float = Field(description="소수점 체결수량")
    trade_price_unit: float = Field(description="체결 단가")
    trade_price: float = Field(description="거래 금액")
    trade_fee: float = Field(description="수수료")
    currency: CurrencyCode = Field(description="통화코드")


class DailyHistoryResponse(BaseModel):
    items: list[DailyHistoryDetailResponse] | None = Field(description="거래내역")
    total_buy_amount: float = Field(description="총 매수금액")
    total_sell_amount: float = Field(description="총 매도금액")
