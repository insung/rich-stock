from pydantic import BaseModel, ConfigDict, Field, field_serializer

from ..models.enums import OverseasMarketCode
from ..entities.kis_base_entity import KISRequestBase, KISResponseBase


class KISDomesticDailyHistoryRequest(KISRequestBase):
    begin_date: str = Field(
        description="조회시작일자",
        min_length=8,
        max_length=8,
        examples=["20240420"],
        serialization_alias="INQR_STRT_DT",
    )
    end_date: str = Field(
        description="조회종료일자",
        min_length=8,
        max_length=8,
        examples=["20240520"],
        serialization_alias="INQR_END_DT",
    )
    inquire_type: str = Field(
        default="00",
        description="매도매수구분코드 (00: 전체, 01: 매도, 02: 매수)",
        ge=0,
        le=2,
        serialization_alias="SLL_BUY_DVSN_CD",
    )
    inquiry_division: str = Field(
        default="01",
        description="조회구분 (00: 역순, 01: 정순)",
        serialization_alias="INQR_DVSN",
    )
    ticker: str = Field(
        default="",
        description="상품번호 (종목번호(6자리), 공란: 전체 조회)",
        serialization_alias="PDNO",
    )
    trade_type: str = Field(
        default="00",
        description="체결구분 (00: 전체, 01: 체결, 02: 미체결)",
        serialization_alias="CCLD_DVSN",
    )
    order_specific_no: str = Field(
        default="", description="주문채번지점번호", serialization_alias="ORD_GNO_BRNO"
    )
    order_no: str = Field(
        default="",
        description="주문번호 (조회기간이 2일 이상인 경우, 공란 입력)",
        serialization_alias="ODNO",
    )
    inquiry_division1: str = Field(
        default="",
        description="조회구분1 (공란: 전체, 1: ELW, 2: 프리보드)",
        serialization_alias="INQR_DVSN_1",
    )
    inquiry_division3: str = Field(
        default="",
        description="조회구분3 (00: 전체, 01: 현금, 02: 융자, 03: 대출, 04: 대주)",
        serialization_alias="INQR_DVSN_3",
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


class KISDomesticDailyHistoryOutput1(BaseModel):
    ord_dt: str = Field(description="주문일자")
    ord_gno_brno: str = Field(
        description="주문채번지점번호 (주문시 한국투자증권 시스템에서 지정된 영업점코드)"
    )
    odno: str = Field(
        description="주문번호 (주문시 한국투자증권 시스템에서 채번된 주문번호, 지점별 일자별로 채번됨)"
    )
    orgn_odno: str = Field(description="원주문번호")
    ord_dvsn_name: str = Field(description="주문구분명")
    sll_buy_dvsn_cd: str = Field(description="매도매수구분코드 (01: 매도, 02: 매수)")
    sll_buy_dvsn_cd_name: str = Field(
        description="매도매수구분코드명 (반대매매 인경우 '임의매도'로 표시됨 정정취소여부가 Y이면 *이 붙음)"
    )
    pdno: str = Field(description="상품번호. 종목번호(6자리)")
    prdt_name: str = Field(description="상품명 (종목명)")
    ord_qty: int = Field(description="주문수량")
    ord_unpr: float = Field(description="주문단가")
    ord_tmd: str = Field(description="주문시각")
    tot_ccld_qty: str = Field(description="총체결수량")
    avg_prvs: str = Field(description="평균가 (체결평균가 ( 총체결금액 / 총체결수량 ))")
    cncl_yn: str = Field(description="취소여부")
    tot_ccld_amt: str = Field(description="총체결금액")
    loan_dt: str = Field(description="대출일자")
    ord_dvsn_cd: str = Field(description="주문구분코드")
    cncl_cfrm_qty: str = Field(description="취소확인수량")
    rmn_qty: str = Field(description="잔여수량")
    rjct_qty: str = Field(description="거부수량")
    ccld_cndt_name: str = Field(description="체결조건명")
    infm_tmd: str = Field(
        description="통보시각 (실전투자계좌로는 해당값이 제공되지 않습니다.)"
    )
    ctac_tlno: str = Field(description="연락전화번호")
    prdt_type_cd: str = Field(description="상품유형코드")
    excg_dvsn_cd: str = Field(
        description="거래소구분코드 (01: 한국증권, 02: 증권거래소, 03: 코스닥..., 81 : 시간외단일가시장)"
    )


class KISDomesticDailyHistoryOutput2(BaseModel):
    tot_ord_qty: int = Field(
        description="총주문수량. 미체결주문수량 + 체결수량 (취소주문제외)"
    )
    tot_ccld_qty: int = Field(description="총체결수량")
    tot_ccld_amt: float = Field(description="매입평균가격. 총체결금액 / 총체결수량")
    prsm_tlex_smtl: float = Field(description="총체결금액")
    pchs_avg_pric: float = Field(description="추정제비용합계. 제세 + 주문수수료")


class KISDomesticDailyHistoryResponse(KISResponseBase):
    ctx_area_fk100: str | None = Field(default="", description="연속조회검색조건100")
    ctx_area_nk100: str | None = Field(default="", description="연속조회키100")
    output1: list[KISDomesticDailyHistoryOutput1] | None = Field(
        default=None, description="응답상세1"
    )
    output2: KISDomesticDailyHistoryOutput2 | None = Field(
        default=None, description="응답상세2"
    )


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
    sll_buy_dvsn_cd: int = Field(description="매도매수구분코드")
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
