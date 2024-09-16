from pydantic import BaseModel, Field


class KISBaseResponse(BaseModel):
    rt_cd: int = Field(description="성공 실패 여부 (0: 성공)")
    msg_cd: str = Field(description="응답코드")

    def isSuccess(self) -> bool:
        return self.rt_cd == 0
