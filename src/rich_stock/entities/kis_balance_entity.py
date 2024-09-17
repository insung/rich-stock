from enum import Enum
from fastapi import Header
from pydantic import BaseModel, ConfigDict, Field, field_serializer

from ..models.enums import CurrencyCode
from ..entities.kis_base_entity import KISBaseResponse


class KISBalanceRequestHeader(BaseModel):
    authorization: str = Header(description="발급한 Access token")
    appkey: str = Header(description="한국투자증권 홈페이지에서 발급받은 appkey")
    appsecret: str = Header(description="한국투자증권 홈페이지에서 발급받은 appsecret")
    tr_id: str = Header(description="거래ID")
    custtype: str = Header(description="고객타입 (P: 개인 / B: 법인)", default="P")


class KISBalanceRequestBase(BaseModel):
    account_number: str = Field(
        max_length=8,
        min_length=8,
        description="종합계좌번호. 계좌번호 체계(8-2)의 앞 8자리",
        serialization_alias="CANO",
    )
    account_code: str = Field(
        max_length=2,
        min_length=2,
        description="계좌상품코드. 계좌번호 체계(8-2)의 뒤 2자리",
        serialization_alias="ACNT_PRDT_CD",
    )


class KISDomesticBalanceRequest(KISBalanceRequestBase):
    is_outside_trading_single_price: bool = Field(
        default=False,
        description="시간외단일가여부",
        serialization_alias="AFHR_FLPR_YN",
    )
    is_offline: bool = Field(
        default=False, description="오프라인여부", serialization_alias="OFL_YN"
    )
    inquire_type: int = Field(
        default=1,
        ge=1,
        le=2,
        description="조회구분 (1 : 대출일별, 2 : 종목별)",
        serialization_alias="INQR_DVSN",
    )
    price_type: str = Field(
        default="01", description="단가구분 (Fixed)", serialization_alias="UNPR_DVSN"
    )
    include_fund_payment: bool = Field(
        default=True,
        description="펀드결제분포함여부",
        serialization_alias="FUND_STTL_ICLD_YN",
    )
    auto_repayment_enabled: bool = Field(
        default=False,
        description="융자금액자동상환여부",
        serialization_alias="FNCG_AMT_AUTO_RDPT_YN",
    )
    include_previous_day_trades: bool = Field(
        default=True,
        description="전일매매포함",
        serialization_alias="PRCS_DVSN",
    )
    sequential_search_params: str = Field(
        default="",
        description="연속조회검색조건100 최초 조회시 공란, 이전 조회 Output CTX_AREA_FK100 값",
        serialization_alias="CTX_AREA_FK100",
    )
    sequential_search_key: str = Field(
        default="",
        description="연속조회키100 최초 조회시 공란, 이전 조회 Output CTX_AREA_NK100 값",
        serialization_alias="CTX_AREA_NK100",
    )

    @field_serializer(
        "is_outside_trading_single_price",
        "include_fund_payment",
        "auto_repayment_enabled",
    )
    def serialize_bool_to_str(value):
        return "Y" if value is True else "N"

    @field_serializer(
        "include_previous_day_trades",
    )
    def serialize_bool_to_specific_value(value):
        return "00" if value is True else "01"

    @field_serializer("is_offline")
    def serialize_bool_to_str_with_none(value):
        return None if value is None else "Y" if value is True else "N"

    @field_serializer("inquire_type")
    def serialize_inquire_type(value):
        return f"0{value}"


class KISDomesticBalanceOutput1Response(BaseModel):
    pdno: int = Field(description="상품번호 (종목번호(뒷 6자리))")
    prdt_name: str = Field(description="상품명")
    trad_dvsn_name: int = Field(description="매매구분명 (매수매도구분)")
    bfdy_buy_qty: int = Field(description="전일매수수량")
    bfdy_sll_qty: int = Field(description="전일매도수량")
    thdt_buyqty: int = Field(description="금일매수수량")
    thdt_sll_qty: int = Field(description="금일매도수량")
    hldg_qty: int = Field(description="보유수량")
    ord_psbl_qty: int = Field(description="주문가능수량")
    pchs_avg_pric: int = Field(description="매입평균가격 (매입금액 / 보유수량)")
    pchs_amt: int = Field(description="매입금액")
    prpr: int = Field(description="현재가")
    evlu_amt: int = Field(description="평가금액")
    evlu_pfls_amt: int = Field(description="평가손익금액")
    evlu_pfls_rt: int = Field(description="평가손익율")
    evlu_erng_rt: int = Field(description="평가수익율")
    loan_dt: int = Field(
        description="대출일자 (INQR_DVSN(조회구분)을 01(대출일별)로 설정해야 값이 나옴)"
    )
    loan_amt: int = Field(description="대출금액")
    stln_slng_chgs: int = Field(description="대주매각대금")
    expd_dt: int = Field(description="만기일자")
    fltt_rt: int = Field(description="등락율")
    bfdy_cprs_icdc: int = Field(description="전일대비증감")
    item_mgna_rt_name: int = Field(description="종목증거금율명")
    grta_rt_name: int = Field(description="보증금율명")
    sbst_pric: int = Field(
        description="대용가격 (증권매매의 위탁보증금으로서 현금 대신에 사용되는 유가증권 가격)"
    )
    stck_loan_unpr: int = Field(description="주식대출단가")


class KISDomesticBalanceOutput2Response(BaseModel):
    dnca_tot_amt: int = Field(description="예수금총금액 (예수금)")
    nxdy_excc_amt: int = Field(description="익일정산금액 (예수금+1)")
    prvs_rcdl_excc_amt: int = Field(description="가수도정산금액 (예수금+2)")
    cma_evlu_amt: int = Field(description="CMA평가금액")
    bfdy_buy_amt: int = Field(description="전일매수금액")
    thdt_buy_amt: int = Field(description="금일매수금액")
    nxdy_auto_rdpt_amt: int = Field(description="익일자동상환금액")
    bfdy_sll_amt: int = Field(description="전일매도금액")
    thdt_sll_amt: int = Field(description="금일매도금액")
    d2_auto_rdpt_amt: int = Field(description="D+2자동상환금액")
    bfdy_tlex_amt: int = Field(description="전일제비용금액")
    thdt_tlex_amt: int = Field(description="금일제비용금액")
    tot_loan_amt: int = Field(description="총대출금액")
    scts_evlu_amt: int = Field(description="유가평가금액")
    tot_evlu_amt: int = Field(
        description="총평가금액 (유가증권 평가금액 합계금액 + D+2 예수금)"
    )
    nass_amt: int = Field(description="순자산금액")
    fncg_gld_auto_rdpt_yn: str | None = Field(
        description="융자금자동상환여부", default=None
    )
    pchs_amt_smtl_amt: int = Field(description="매입금액합계금액")
    evlu_amt_smtl_amt: int = Field(
        description="평가금액합계금액 (유가증권 평가금액 합계금액)"
    )
    evlu_pfls_smtl_amt: int = Field(description="평가손익합계금액")
    tot_stln_slng_chgs: int = Field(description="총대주매각대금")
    bfdy_tot_asst_evlu_amt: int = Field(description="전일총자산평가금액")
    asst_icdc_amt: int = Field(description="자산증감액")
    asst_icdc_erng_rt: float = Field(description="자산증감수익율")


class KISDomesticBalanceResponse(KISBaseResponse):
    output1: list[KISDomesticBalanceOutput1Response | None] = Field(
        description="응답상세1"
    )
    output2: list[KISDomesticBalanceOutput2Response | None] = Field(
        description="응답상세2"
    )
    ctx_area_fk100: str = Field(description="연속조회검색조건100")
    ctx_area_nk100: str = Field(description="연속조회키100")


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


class KISOverseasBalanceRequest(KISBalanceRequestBase):
    market_code: OverseasMarketCode = Field(
        default=OverseasMarketCode.Nasdaq,
        description="해외거래소코드",
        serialization_alias="OVRS_EXCG_CD",
    )
    currency: CurrencyCode = Field(
        default=CurrencyCode.USD,
        description="거래통화코드",
        serialization_alias="TR_CRCY_CD",
    )
    sequential_search_params: str = Field(
        default="",
        description="연속조회검색조건200. 최초 조회시 공란, 이전 조회 Output CTX_AREA_FK200 값",
        serialization_alias="CTX_AREA_FK200",
    )
    sequential_search_key: str = Field(
        default="",
        description="연속조회키200. 최초 조회시 공란, 이전 조회 Output CTX_AREA_NK200 값",
        serialization_alias="CTX_AREA_NK200",
    )

    model_config = ConfigDict(use_enum_values=True, validate_default=True)


class KISOverseasOutput1Response(BaseModel):
    cano: str = Field(description="종합계좌번호")
    acnt_prdt_cd: str = Field(description="계좌상품코드")
    prdt_type_cd: str = Field(description="상품유형코드")
    ovrs_pdno: str = Field(description="해외상품번호")
    ovrs_item_name: str = Field(description="해외종목명")
    frcr_evlu_pfls_amt: str = Field(description="외화평가손익금액")
    evlu_pfls_rt: str = Field(description="평가손익율")
    pchs_avg_pric: str = Field(description="매입평균가격")
    ovrs_cblc_qty: str = Field(description="해외잔고수량")
    ord_psbl_qty: str = Field(description="주문가능수량")
    frcr_pchs_amt1: str = Field(description="외화매입금액1")
    ovrs_stck_evlu_amt: str = Field(description="해외주식평가금액")
    now_pric2: str = Field(description="현재가격2")
    tr_crcy_cd: str = Field(description="거래통화코드")
    ovrs_excg_cd: str = Field(description="해외거래소코드")
    loan_type_cd: str = Field(description="대출유형코드")
    loan_dt: str = Field(description="대출일자")
    expd_dt: str = Field(description="만기일자")


class KISOverseasOutput2Response(BaseModel):
    frcr_pchs_amt1: float = Field(description="외화매입금액1")
    ovrs_rlzt_pfls_amt: float = Field(description="해외실현손익금액")
    ovrs_tot_pfls: float = Field(description="해외총손익")
    rlzt_erng_rt: float = Field(description="실현수익율")
    tot_evlu_pfls_amt: float = Field(description="총평가손익금액")
    tot_pftrt: float = Field(description="총수익률")
    frcr_buy_amt_smtl1: float = Field(description="외화매수금액합계1")
    ovrs_rlzt_pfls_amt2: float = Field(description="해외실현손익금액2")
    frcr_buy_amt_smtl2: float = Field(description="외화매수금액합계2")


class KISOverseasBalanceResponse(KISBaseResponse):
    output1: list[KISOverseasOutput1Response | None] = Field(description="응답상세1")
    output2: KISOverseasOutput2Response | None = Field(
        default=None, description="응답상세2"
    )
    ctx_area_fk200: str = Field(default="", description="연속조회검색조건200")
    ctx_area_nk200: str = Field(default="", description="연속조회키200")
