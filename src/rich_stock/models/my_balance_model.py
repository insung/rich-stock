from pydantic import BaseModel, Field


class MyBalanceResponse(BaseModel):
    deposit: int = Field(description="예수금", default=0)
    deposit_next_day: int = Field(description="예수금 +1", default=0)
    deposit_day_after_next: int = Field(description="예수금 +2", default=0)
