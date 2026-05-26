from pydantic import BaseModel, Field


class ExchangeResponse(BaseModel):
    sell: float
    buy: float
    date: str
    id_account: str = Field(..., alias="id-account")

    model_config = {"populate_by_name": True}
