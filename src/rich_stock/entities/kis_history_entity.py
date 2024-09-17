from pydantic import BaseModel, ConfigDict, Field, field_serializer

from ..models.enums import OverseasMarketCode
from ..entities.kis_base_entity import KISRequestBase, KISResponseBase


class KISOverseasDailyHistoryRequest(KISRequestBase):
    begin_date: str = Field(
        description="등록시작일자",
        min_length=8,
        max_length=8,
        examples=["20240420"],
        serialization_alias="ERLM_STRT_DT",
    )
    end_date: str = Field(
        description="등록종료일자",
        min_length=8,
        max_length=8,
        examples=["20240520"],
        serialization_alias="ERLM_END_DT",
    )
    market_code: OverseasMarketCode = Field(
        default=OverseasMarketCode.Nasdaq,
        description="해외거래소코드",
        min_length=1,
        max_length=4,
        serialization_alias="OVRS_EXCG_CD",
    )
    ticker: str = Field(
        default="",
        description="상품번호 (공백 (전체조회), 개별종목 조회는 상품번호입력)",
        serialization_alias="PDNO",
    )
    inquire_type: int = Field(
        default=0,
        description="매도매수구분코드 (00: 전체, 01: 매도, 02: 매수)",
        ge=0,
        le=2,
        serialization_alias="SLL_BUY_DVSN_CD",
    )
    loan_type: str = Field(
        default="", description="대출구분코드", serialization_alias="LOAN_DVSN_CD"
    )
    sequential_search_params: str = Field(
        default="",
        description="연속조회검색조건100",
        serialization_alias="CTX_AREA_FK100",
    )
    sequential_search_key: str = Field(
        default="", description="연속조회키100", serialization_alias="CTX_AREA_NK100"
    )

    @field_serializer("inquire_type")
    def serialize_inquire_type(value):
        return f"0{value}"

    model_config = ConfigDict(use_enum_values=True, validate_default=True)


class KISOverseasDailyHistoryOutput1(BaseModel):
    trad_dt: str = Field(description="매매일자")
    sttl_dt: str = Field(description="결제일자")
    sll_buy_dvsn_cd: str = Field(description="매도매수구분코드")
    sll_buy_dvsn_name: str = Field(description="매도매수구분명")
    pdno: str = Field(description="상품번호")
    ovrs_item_name: str = Field(description="해외종목명")
    ccld_qty: str = Field(description="체결수량")
    amt_unit_ccld_qty: float = Field(description="금액단위체결수량")
    ft_ccld_unpr2: float = Field(description="FT체결단가2")
    ovrs_stck_ccld_unpr: float = Field(description="해외주식체결단가")
    tr_frcr_amt2: float = Field(description="거래외화금액2")
    tr_amt: float = Field(description="거래금액")
    frcr_excc_amt_1: float = Field(description="외화정산금액1")
    wcrc_excc_amt: float = Field(description="원화정산금액")
    dmst_frcr_fee1: float = Field(description="국내외화수수료1")
    frcr_fee1: float = Field(description="외화수수료1")
    dmst_wcrc_fee: float = Field(description="국내원화수수료")
    ovrs_wcrc_fee: float = Field(description="해외원화수수료")
    crcy_cd: str = Field(description="통화코드")
    std_pdno: str = Field(description="표준상품번호")
    erlm_exrt: str = Field(description="등록환율")
    loan_dvsn_cd: str = Field(description="대출구분코드")
    loan_dvsn_name: str = Field(description="대출구분명")


class KISOverseasDailyHistoryOutput2(BaseModel):
    frcr_buy_amt_smtl: float = Field(description="외화매수금액합계")
    frcr_sll_amt_smtl: float = Field(description="외화매도금액합계")
    dmst_fee_smtl: float = Field(description="국내수수료합계")
    ovrs_fee_smtl: float = Field(description="해외수수료합계")


class KISOverseasDailyHistoryResponse(KISResponseBase):
    ctx_area_fk100: str | None = Field(default="", description="연속조회검색조건100")
    ctx_area_nk100: str | None = Field(default="", description="연속조회키100")
    output1: list[KISOverseasDailyHistoryOutput1] | None = Field(
        default=None, description="응답상세1"
    )
    output2: KISOverseasDailyHistoryOutput2 | None = Field(
        default=None, description="응답상세2"
    )
